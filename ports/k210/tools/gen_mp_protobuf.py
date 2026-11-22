#!/usr/bin/env python3
# Generates MicroPython modules for protobuf.py from a descriptor set:
#
#   protoc -I<dir> --include_imports --descriptor_set_out=x.desc <files>
#   python3 gen_mp_protobuf.py x.desc <out dir> [--only meshtastic/]
#       [--map meshtastic/=meshtastic/protobuf/]
#
# Each .proto file becomes <name>_pb2.py (as protoc --python_out names it):
# a class per message (nested messages and enums inside it), an Enum class
# per enum with its values as attributes (and, as in Google's modules, as
# module constants or attributes of the message holding it), and each
# message's fields as _F: (number, name, kind, flags, type, oneof), in
# number order. Needs google.protobuf (only here, not on the device).

import argparse
import keyword
import os
import sys

from google.protobuf import descriptor_pb2

FD = descriptor_pb2.FieldDescriptorProto
KIND = {
    FD.TYPE_INT32: 0, FD.TYPE_INT64: 1, FD.TYPE_UINT32: 2, FD.TYPE_UINT64: 3,
    FD.TYPE_SINT32: 4, FD.TYPE_SINT64: 5, FD.TYPE_BOOL: 6, FD.TYPE_ENUM: 7,
    FD.TYPE_FIXED32: 8, FD.TYPE_SFIXED32: 9, FD.TYPE_FLOAT: 10,
    FD.TYPE_FIXED64: 11, FD.TYPE_SFIXED64: 12, FD.TYPE_DOUBLE: 13,
    FD.TYPE_STRING: 14, FD.TYPE_BYTES: 15, FD.TYPE_MESSAGE: 16,
}
STRING, MESSAGE = 14, 16
REPEATED, PACKED, PRESENCE = 1, 2, 4


def module_of(proto_name, mapping):
    path = proto_name[:-len(".proto")] + "_pb2"
    for a, b in mapping:
        if path.startswith(a):
            path = b + path[len(a):]
    return path.replace("/", ".")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("descriptor_set")
    ap.add_argument("out")
    ap.add_argument("--only", action="append", default=[])
    ap.add_argument("--map", action="append", default=[])
    a = ap.parse_args()
    mapping = [m.split("=", 1) for m in a.map]
    fds = descriptor_pb2.FileDescriptorSet()
    fds.ParseFromString(open(a.descriptor_set, "rb").read())
    wanted = [f for f in fds.file if not a.only or any(f.name.startswith(o) for o in a.only)]

    # Every message's and enum's full name -> (module, Python path in it)
    where = {}

    def index(prefix, pypath, module, msgs, enums):
        for e in enums:
            where[prefix + e.name] = (module, pypath + e.name)
        for m in msgs:
            where[prefix + m.name] = (module, pypath + m.name)
            index(prefix + m.name + ".", pypath + m.name + ".", module, m.nested_type, m.enum_type)

    for f in fds.file:
        index("." + f.package + "." if f.package else ".", "", module_of(f.name, mapping), f.message_type, f.enum_type)

    for f in wanted:
        if not f.message_type and not f.enum_type:
            continue
        mod = module_of(f.name, mapping)
        out = ["# Generated from %s by gen_mp_protobuf.py, for protobuf.py: do not edit." % f.name,
               "from protobuf import Message, Enum"]
        deps = sorted({module_of(d, mapping) for d in f.dependency if any(d.startswith(o) for o in a.only) or not a.only})
        deps = [d for d in deps if d != mod]
        for d in deps:
            pkg, _, name = d.rpartition(".")
            out.append("from %s import %s" % (pkg, name) if pkg else "import %s" % name)
        out.append("")
        late = []  # lines after all the classes: _F, and keyword-named values

        def ref(type_name):
            m, p = where[type_name]
            return p if m == mod else m.rpartition(".")[2] + "." + p

        def enum_lines(e, indent, path, holder):
            lines = ["%sclass %s(Enum):" % (indent, e.name)]
            lines.append("%s    _V = (%s)" % (indent, "".join("(%r, %d), " % (v.name, v.number) for v in e.value)))
            for v in e.value:
                if keyword.iskeyword(v.name):
                    late.append("setattr(%s, %r, %d)" % (path, v.name, v.number))
                else:
                    lines.append("%s    %s = %d" % (indent, v.name, v.number))
            # The values also on what holds the enum, as Google's modules have them
            for v in e.value:
                if keyword.iskeyword(v.name):
                    late.append("setattr(%s, %r, %d)" % (holder or "sys.modules[__name__]", v.name, v.number))
                else:
                    (lines if holder else late).append(("%s%s = %d" % (indent, v.name, v.number)) if holder else "%s = %d" % (v.name, v.number))
            return lines

        proto3 = f.syntax == "proto3"

        def message_lines(m, indent, path):
            lines = ["%sclass %s(Message):" % (indent, m.name)]
            body = []
            for e in m.enum_type:
                body += enum_lines(e, indent + "    ", path + "." + e.name, path)
            for n in m.nested_type:
                if n.options.map_entry:
                    sys.exit("%s: map fields aren't supported" % path)
                body += message_lines(n, indent + "    ", path + "." + n.name)
            lines += body or [indent + "    pass"]
            fields = []
            for fld in sorted(m.field, key=lambda x: x.number):
                kind = KIND.get(fld.type)
                if kind is None:
                    sys.exit("%s.%s: field type %d not supported" % (path, fld.name, fld.type))
                flags = 0
                oneof = None
                # proto3 packs repeated numbers unless told not to, and
                # gives other scalars presence only when optional; proto2
                # packs only when told to, and gives every one presence
                if fld.label == FD.LABEL_REPEATED:
                    flags |= REPEATED
                    packed = fld.options.packed if fld.options.HasField("packed") else proto3
                    if kind < STRING and packed:
                        flags |= PACKED
                elif fld.proto3_optional or kind == MESSAGE or not proto3:
                    flags |= PRESENCE
                elif fld.HasField("oneof_index"):
                    flags |= PRESENCE
                    oneof = m.oneof_decl[fld.oneof_index].name
                typ = ref(fld.type_name) if kind == MESSAGE else "None"
                fields.append("(%d, %r, %d, %d, %s, %r)" % (fld.number, fld.name, kind, flags, typ, oneof))
                if fld.HasField("oneof_index") and not fld.proto3_optional and kind == MESSAGE:
                    fields[-1] = "(%d, %r, %d, %d, %s, %r)" % (fld.number, fld.name, kind, flags,
                                                             typ, m.oneof_decl[fld.oneof_index].name)
            late.append("%s._F = (%s)" % (path, "".join(x + ", " for x in fields)))
            return lines

        for e in f.enum_type:
            out += enum_lines(e, "", e.name, None)
            out.append("")
        for m in f.message_type:
            out += message_lines(m, "", m.name)
            out.append("")
        if any(l.startswith("setattr(sys") for l in late):
            out.insert(1, "import sys")
        out += late
        path = os.path.join(a.out, *mod.split(".")) + ".py"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w").write("\n".join(out) + "\n")
        print(path, len(f.message_type), "messages,", len(f.enum_type), "enums")
    # The packages' __init__.py
    for f in wanted:
        parts = module_of(f.name, mapping).split(".")[:-1]
        for i in range(1, len(parts) + 1):
            init = os.path.join(a.out, *parts[:i], "__init__.py")
            if not os.path.exists(init):
                open(init, "w").close()


main()
