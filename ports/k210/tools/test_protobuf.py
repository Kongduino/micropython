# Checks protobuf.py and the generated modules against google.protobuf: for
# every message type, random messages (every field type, nested messages,
# repeated fields, oneofs) serialized by Google's modules must decode and
# re-encode to the same bytes, and built field by field must encode to them.
# Runs on the host (CPython, google.protobuf installed). From a work
# directory holding refpb/ (protoc --python_out's modules, their package
# renamed from meshtastic to refpb):
#
#   protoc -I<protobufs> --python_out=ref <protobufs>/meshtastic/*.proto <protobufs>/nanopb.proto
#   cp -r ref/meshtastic refpb; cp ref/nanopb_pb2.py refpb/; touch refpb/__init__.py
#   sed -i '' 's/from meshtastic import/from refpb import/; s/^import nanopb_pb2/from refpb import nanopb_pb2/' refpb/*.py
#   python3 <port>/tools/test_protobuf.py <port>/modules
import importlib, random, struct, sys, glob, os
sys.path[:0] = [sys.argv[1] if len(sys.argv) > 1 else 'modules', '.']
import protobuf
from google.protobuf.descriptor import FieldDescriptor as FD

R = random.Random(1234)
ints = {FD.TYPE_INT32: (-2**31, 2**31 - 1), FD.TYPE_SINT32: (-2**31, 2**31 - 1), FD.TYPE_SFIXED32: (-2**31, 2**31 - 1),
        FD.TYPE_INT64: (-2**63, 2**63 - 1), FD.TYPE_SINT64: (-2**63, 2**63 - 1), FD.TYPE_SFIXED64: (-2**63, 2**63 - 1),
        FD.TYPE_UINT32: (0, 2**32 - 1), FD.TYPE_FIXED32: (0, 2**32 - 1), FD.TYPE_UINT64: (0, 2**64 - 1), FD.TYPE_FIXED64: (0, 2**64 - 1)}

def rint(lo, hi):
    c = R.random()
    if c < 0.2: return R.choice([0, 1, lo, hi, -1 if lo < 0 else 2])
    if c < 0.6: return R.randint(max(lo, -300), min(hi, 300))
    return R.randint(lo, hi)

def rval(fd, depth):
    t = fd.type
    if t in ints: return rint(*ints[t])
    if t == FD.TYPE_BOOL: return R.random() < 0.5
    if t == FD.TYPE_ENUM: return R.choice(fd.enum_type.values).number
    if t == FD.TYPE_FLOAT: return struct.unpack('<f', struct.pack('<f', R.uniform(-1e6, 1e6)))[0]
    if t == FD.TYPE_DOUBLE: return R.uniform(-1e12, 1e12)
    if t == FD.TYPE_STRING: return ''.join(R.choice('abcxyz éü€😀 \n') for _ in range(R.randint(0, 12)))
    if t == FD.TYPE_BYTES: return bytes(R.randrange(256) for _ in range(R.randint(0, 20)))
    raise TypeError(t)

def fill(msg, depth=0):
    d = msg.DESCRIPTOR
    chosen = {}
    for o in d.oneofs:
        if R.random() < 0.7:
            chosen[o.name] = R.choice(o.fields).name
    for fd in d.fields:
        o = fd.containing_oneof
        if o is not None and o.name in chosen and chosen[o.name] != fd.name:
            continue
        if o is not None and o.name not in chosen:
            continue
        if R.random() < 0.35 and o is None:
            continue
        is_rep = fd.is_repeated if hasattr(fd, 'is_repeated') else fd.label == FD.LABEL_REPEATED
        if fd.type == FD.TYPE_MESSAGE:
            if depth >= 3: continue
            if is_rep:
                for _ in range(R.randint(0, 3)):
                    fill(getattr(msg, fd.name).add(), depth + 1)
            else:
                sub = getattr(msg, fd.name)
                sub.SetInParent()
                fill(sub, depth + 1)
        elif is_rep:
            getattr(msg, fd.name).extend(rval(fd, depth) for _ in range(R.randint(0, 3)))
        else:
            setattr(msg, fd.name, rval(fd, depth))

def ours_class(gcls):
    d = gcls.DESCRIPTOR
    modname = 'meshtastic.protobuf.' + os.path.basename(d.file.name)[:-6] + '_pb2'
    m = importlib.import_module(modname)
    obj = m
    for part in d.full_name.split('.')[1:]:
        obj = getattr(obj, part)
    return obj

def build(g, ocls):
    # ours, set field by field from Google's
    o = ocls()
    for fd, v in g.ListFields():
        is_rep = fd.is_repeated if hasattr(fd, 'is_repeated') else fd.label == FD.LABEL_REPEATED
        if fd.type == FD.TYPE_MESSAGE:
            sub_cls = ours_class(type(v[0]) if is_rep else type(v))
            if is_rep:
                rep = getattr(o, fd.name)
                for x in v:
                    rep.append(build(x, sub_cls))
            else:
                setattr(o, fd.name, build(v, sub_cls))
        elif is_rep:
            getattr(o, fd.name).extend(list(v))
        else:
            setattr(o, fd.name, v)
    return o

def all_classes():
    for path in sorted(glob.glob('refpb/*_pb2.py')):
        name = os.path.basename(path)[:-3]
        if name in ('nanopb_pb2',): continue
        m = importlib.import_module('refpb.' + name)
        stack = [getattr(m, n) for n in m.DESCRIPTOR.message_types_by_name]
        while stack:
            c = stack.pop()
            yield c
            stack += [getattr(c, n.name) for n in c.DESCRIPTOR.nested_types if not n.GetOptions().map_entry]

total = fails = 0
classes = list(all_classes())
for gcls in classes:
    ocls = ours_class(gcls)
    for i in range(40):
        g = gcls()
        fill(g)
        gb = g.SerializeToString()
        total += 1
        try:
            o = ocls.FromString(gb)
            ob = o.SerializeToString()
            assert ob == gb, 'decode+encode differs'
            b2 = build(g, ocls).SerializeToString()
            assert b2 == gb, 'build+encode differs'
            assert gcls.FromString(ob) == g
        except Exception as e:
            fails += 1
            if fails <= 8:
                print('FAIL', gcls.DESCRIPTOR.full_name, type(e).__name__, e)
                print('  google', gb.hex()[:160])
                try: print('  ours  ', ob.hex()[:160])
                except Exception: pass
print('%d message types, %d random messages, %d failures' % (len(classes), total, fails))
