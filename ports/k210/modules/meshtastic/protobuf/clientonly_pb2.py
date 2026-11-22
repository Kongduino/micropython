# Generated from meshtastic/clientonly.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import localonly_pb2
from meshtastic.protobuf import mesh_pb2

class DeviceProfile(Message):
    pass

DeviceProfile._F = ((1, 'long_name', 14, 4, None, None), (2, 'short_name', 14, 4, None, None), (3, 'channel_url', 14, 4, None, None), (4, 'config', 16, 4, localonly_pb2.LocalConfig, None), (5, 'module_config', 16, 4, localonly_pb2.LocalModuleConfig, None), (6, 'fixed_position', 16, 4, mesh_pb2.Position, None), (7, 'ringtone', 14, 4, None, None), (8, 'canned_messages', 14, 4, None, None), (9, 'is_unmessagable', 6, 4, None, None), (10, 'is_licensed', 6, 4, None, None), )
