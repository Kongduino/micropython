# Protocol Buffers for MicroPython: the runtime for the modules
# gen_mp_protobuf.py generates from .proto files (proto3), with the part of
# Google's Python API (google.protobuf) that most code uses:
#
#   from meshtastic.protobuf import mesh_pb2
#   p = mesh_pb2.MeshPacket(to=0xFFFFFFFF, channel=0)
#   p.decoded.portnum = portnums_pb2.TEXT_MESSAGE_APP
#   p.decoded.payload = b"hello"
#   b = p.SerializeToString()
#   q = mesh_pb2.MeshPacket.FromString(b)
#   q.WhichOneof("payload_variant")   # 'decoded'
#   getattr(q, "from")                # a field named with a keyword
#
# Messages serialize as Google's do (fields in number order, proto3's
# defaults left out unless the field has explicit presence, repeated numbers
# packed), so the bytes are the same. Unknown fields are skipped when
# parsing. Reading a message field that isn't set gives an empty message
# which becomes set (in its parent) when one of its fields is set, as in
# Google's API.
#
# Runs on CPython too (for tests against google.protobuf).

import struct

# Field kinds
INT32 = 0
INT64 = 1
UINT32 = 2
UINT64 = 3
SINT32 = 4
SINT64 = 5
BOOL = 6
ENUM = 7
FIXED32 = 8
SFIXED32 = 9
FLOAT = 10
FIXED64 = 11
SFIXED64 = 12
DOUBLE = 13
STRING = 14
BYTES = 15
MESSAGE = 16

# Field flags
REPEATED = 1
PACKED = 2
PRESENCE = 4  # explicit presence: proto3 optional, a oneof member, a message

_WIRE = (0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 1, 1, 1, 2, 2, 2)
_DEFAULT = (0, 0, 0, 0, 0, 0, False, 0, 0, 0, 0.0, 0, 0, 0.0, "", b"", None)
_FMT = {FIXED32: "<I", SFIXED32: "<i", FLOAT: "<f", FIXED64: "<Q", SFIXED64: "<q", DOUBLE: "<d"}
_M64 = (1 << 64) - 1


class DecodeError(ValueError):
    pass


_metas = {}


def _meta(cls):
    # A message class's fields by number and by name, and its oneofs, made
    # at first use from its _F: (number, name, kind, flags, type, oneof)
    m = _metas.get(cls)
    if m is None:
        by_num, by_name, oneofs = {}, {}, {}
        for f in cls._F:
            by_num[f[0]] = f
            by_name[f[1]] = f
            if f[5] is not None:
                oneofs.setdefault(f[5], []).append(f[1])
        m = (by_num, by_name, oneofs)
        _metas[cls] = m
    return m


class Repeated(list):
    # A repeated field: a list, with add() for messages
    def __init__(self, cls=None, items=()):
        list.__init__(self, items)
        self._cls = cls

    def add(self, **kw):
        m = self._cls(**kw)
        self.append(m)
        return m

    def MergeFrom(self, other):
        self.extend(other)


class Enum:
    # A generated enum: its values as class attributes, and _V
    # ((name, value), ...)
    @classmethod
    def Name(cls, value):
        for n, v in cls._V:
            if v == value:
                return n
        raise ValueError("unknown %s value %r" % (cls.__name__, value))

    @classmethod
    def Value(cls, name):
        for n, v in cls._V:
            if n == name:
                return v
        raise ValueError("unknown %s name %r" % (cls.__name__, name))

    @classmethod
    def keys(cls):
        return [n for n, v in cls._V]

    @classmethod
    def values(cls):
        return [v for n, v in cls._V]

    @classmethod
    def items(cls):
        return list(cls._V)


class Message:
    _F = ()

    def __init__(self, **kw):
        object.__setattr__(self, "_d", {})
        object.__setattr__(self, "_parent", None)
        for k, v in kw.items():
            setattr(self, k, v)

    def __getattr__(self, name):
        # Fields live in _d, not as attributes, so every read comes here
        d = self._d
        if name in d:
            return d[name]
        f = _meta(type(self))[1].get(name)
        if f is None:
            raise AttributeError(name)
        if f[3] & REPEATED:
            v = Repeated(f[4] if f[2] == MESSAGE else None)
            d[name] = v
            return v
        if f[2] == MESSAGE:
            # Not set: an empty one, set in this one when it's written to
            v = f[4]()
            object.__setattr__(v, "_parent", (self, name))
            return v
        return _DEFAULT[f[2]]

    def __setattr__(self, name, value):
        cls = type(self)
        f = _meta(cls)[1].get(name)
        if f is None:
            raise AttributeError("%s has no field %s" % (cls.__name__, name))
        d = self._d
        if f[5] is not None:
            for other in _meta(cls)[2][f[5]]:
                if other != name and other in d:
                    del d[other]
        if f[3] & REPEATED:
            value = Repeated(f[4] if f[2] == MESSAGE else None, value)
        d[name] = value
        self._set()

    def _set(self):
        # Written to: set in the parent it came from, if any
        p = self._parent
        if p is not None:
            object.__setattr__(self, "_parent", None)
            setattr(p[0], p[1], self)

    def HasField(self, name):
        if name in _meta(type(self))[2]:
            return self.WhichOneof(name) is not None
        return name in self._d

    def ClearField(self, name):
        oneofs = _meta(type(self))[2]
        for n in oneofs.get(name, (name,)):
            self._d.pop(n, None)

    def WhichOneof(self, oneof):
        for n in _meta(type(self))[2][oneof]:
            if n in self._d:
                return n
        return None

    def Clear(self):
        self._d.clear()

    def ListFields(self):
        out = []
        for f in type(self)._F:
            v = self._d.get(f[1])
            if v is not None and (v or f[3] & PRESENCE and not f[3] & REPEATED):
                out.append((f, v))
        return out

    def SerializeToString(self):
        out = bytearray()
        _encode(self, out)
        return bytes(out)

    def ParseFromString(self, data):
        self._d.clear()
        return self.MergeFromString(data)

    def MergeFromString(self, data):
        mv = memoryview(data)
        _decode(self, mv, 0, len(mv))
        self._set()
        return len(mv)

    @classmethod
    def FromString(cls, data):
        m = cls()
        m.MergeFromString(data)
        return m

    def CopyFrom(self, other):
        self.ParseFromString(other.SerializeToString())

    def MergeFrom(self, other):
        self.MergeFromString(other.SerializeToString())

    def ByteSize(self):
        return len(self.SerializeToString())

    def __eq__(self, other):
        return type(self) is type(other) and self.SerializeToString() == other.SerializeToString()

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, ", ".join("%s=%r" % (f[1], v) for f, v in self.ListFields()))


# Encoding


def _varint(out, v):
    while v > 0x7F:
        out.append((v & 0x7F) | 0x80)
        v >>= 7
    out.append(v)


def _scalar(out, kind, v):
    # A scalar's value (not its key)
    if kind <= ENUM:
        if kind == SINT32:
            v = (v << 1) ^ (v >> 31)
        elif kind == SINT64:
            v = (v << 1) ^ (v >> 63)
        elif kind == BOOL:
            v = 1 if v else 0
        elif v < 0:
            v &= _M64
        _varint(out, v)
    elif kind <= DOUBLE:
        out.extend(struct.pack(_FMT[kind], v))
    else:
        if kind == STRING:
            v = v.encode()
        _varint(out, len(v))
        out.extend(v)


def _field(out, num, kind, v):
    _varint(out, (num << 3) | _WIRE[kind])
    if kind == MESSAGE:
        sub = bytearray()
        _encode(v, sub)
        _varint(out, len(sub))
        out.extend(sub)
    else:
        _scalar(out, kind, v)


def _encode(msg, out):
    d = msg._d
    for f in type(msg)._F:
        name = f[1]
        if name not in d:
            continue
        v = d[name]
        num, kind, flags = f[0], f[2], f[3]
        if flags & REPEATED:
            if not v:
                continue
            if flags & PACKED:
                run = bytearray()
                for x in v:
                    _scalar(run, kind, x)
                _varint(out, (num << 3) | 2)
                _varint(out, len(run))
                out.extend(run)
            else:
                for x in v:
                    _field(out, num, kind, x)
        elif flags & PRESENCE or v != _DEFAULT[kind]:
            _field(out, num, kind, v)


# Decoding


def _rvarint(mv, pos):
    v = 0
    shift = 0
    while True:
        b = mv[pos]
        pos += 1
        v |= (b & 0x7F) << shift
        if b < 0x80:
            return v, pos
        shift += 7
        if shift > 63:
            raise DecodeError("varint too long")


def _rscalar(mv, pos, kind):
    if kind <= ENUM:
        v, pos = _rvarint(mv, pos)
        if kind == UINT32:
            v &= 0xFFFFFFFF
        elif kind == SINT32 or kind == SINT64:
            v = (v >> 1) ^ -(v & 1)
        elif kind == BOOL:
            v = v != 0
        elif kind != UINT64 and v > 0x7FFFFFFFFFFFFFFF:
            v -= 1 << 64
        return v, pos
    size = 4 if kind <= FLOAT else 8
    return struct.unpack(_FMT[kind], mv[pos:pos + size])[0], pos + size


def _skip(mv, pos, wt):
    if wt == 0:
        return _rvarint(mv, pos)[1]
    if wt == 1:
        return pos + 8
    if wt == 5:
        return pos + 4
    if wt == 2:
        n, pos = _rvarint(mv, pos)
        return pos + n
    raise DecodeError("wire type %d" % wt)


def _decode(msg, mv, pos, end):
    cls = type(msg)
    by_num, _, oneofs = _meta(cls)
    d = msg._d
    while pos < end:
        key, pos = _rvarint(mv, pos)
        f = by_num.get(key >> 3)
        wt = key & 7
        if f is None:
            pos = _skip(mv, pos, wt)
            continue
        name, kind, flags = f[1], f[2], f[3]
        if flags & REPEATED:
            lst = d.get(name)
            if lst is None:
                lst = d[name] = Repeated(f[4] if kind == MESSAGE else None)
            if wt == 2 and kind < STRING:
                n, pos = _rvarint(mv, pos)
                run_end = pos + n
                while pos < run_end:
                    v, pos = _rscalar(mv, pos, kind)
                    lst.append(v)
                continue
        if wt == 2 and kind >= STRING:
            n, pos = _rvarint(mv, pos)
            if kind == MESSAGE:
                v = f[4]()
                _decode(v, mv, pos, pos + n)
            elif kind == STRING:
                v = str(bytes(mv[pos:pos + n]), "utf-8")
            else:
                v = bytes(mv[pos:pos + n])
            pos += n
        else:
            v, pos = _rscalar(mv, pos, kind)
        if flags & REPEATED:
            lst.append(v)
        else:
            if f[5] is not None:
                for other in oneofs[f[5]]:
                    if other != name and other in d:
                        del d[other]
            d[name] = v
    if pos != end:
        raise DecodeError("truncated message")
