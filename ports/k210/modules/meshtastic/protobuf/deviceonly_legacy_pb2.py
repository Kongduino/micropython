# Generated from meshtastic/deviceonly_legacy.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import deviceonly_pb2
from meshtastic.protobuf import telemetry_pb2

class NodeInfoLite_Legacy(Message):
    pass

class NodeDatabase_Legacy(Message):
    pass

NodeInfoLite_Legacy._F = ((1, 'num', 2, 0, None, None), (2, 'user', 16, 4, deviceonly_pb2.UserLite, None), (3, 'position', 16, 4, deviceonly_pb2.PositionLite, None), (4, 'snr', 10, 0, None, None), (5, 'last_heard', 8, 0, None, None), (6, 'device_metrics', 16, 4, telemetry_pb2.DeviceMetrics, None), (7, 'channel', 2, 0, None, None), (8, 'via_mqtt', 6, 0, None, None), (9, 'hops_away', 2, 4, None, None), (10, 'is_favorite', 6, 0, None, None), (11, 'is_ignored', 6, 0, None, None), (12, 'next_hop', 2, 0, None, None), (13, 'bitfield', 2, 0, None, None), )
NodeDatabase_Legacy._F = ((1, 'version', 2, 0, None, None), (2, 'nodes', 16, 1, NodeInfoLite_Legacy, None), )
