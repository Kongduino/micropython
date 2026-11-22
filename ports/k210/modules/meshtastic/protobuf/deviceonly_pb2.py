# Generated from meshtastic/deviceonly.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import channel_pb2
from meshtastic.protobuf import config_pb2
from meshtastic.protobuf import localonly_pb2
from meshtastic.protobuf import mesh_pb2
from meshtastic.protobuf import telemetry_pb2

class PositionLite(Message):
    pass

class UserLite(Message):
    pass

class NodeInfoLite(Message):
    pass

class DeviceState(Message):
    pass

class NodePositionEntry(Message):
    pass

class NodeTelemetryEntry(Message):
    pass

class NodeEnvironmentEntry(Message):
    pass

class NodeStatusEntry(Message):
    pass

class NodeDatabase(Message):
    pass

class ChannelFile(Message):
    pass

class BackupPreferences(Message):
    pass

PositionLite._F = ((1, 'latitude_i', 9, 0, None, None), (2, 'longitude_i', 9, 0, None, None), (3, 'altitude', 0, 0, None, None), (4, 'time', 8, 0, None, None), (5, 'location_source', 7, 0, None, None), (6, 'precision_bits', 2, 0, None, None), )
UserLite._F = ((1, 'macaddr', 15, 0, None, None), (2, 'long_name', 14, 0, None, None), (3, 'short_name', 14, 0, None, None), (4, 'hw_model', 7, 0, None, None), (5, 'is_licensed', 6, 0, None, None), (6, 'role', 7, 0, None, None), (7, 'public_key', 15, 0, None, None), (9, 'is_unmessagable', 6, 4, None, None), )
NodeInfoLite._F = ((1, 'num', 2, 0, None, None), (4, 'snr', 10, 0, None, None), (5, 'last_heard', 8, 0, None, None), (7, 'channel', 2, 0, None, None), (9, 'hops_away', 2, 4, None, None), (12, 'next_hop', 2, 0, None, None), (13, 'bitfield', 2, 0, None, None), (14, 'long_name', 14, 0, None, None), (15, 'short_name', 14, 0, None, None), (16, 'hw_model', 7, 0, None, None), (17, 'role', 7, 0, None, None), (18, 'public_key', 15, 0, None, None), (19, 'snr_q4', 4, 0, None, None), )
DeviceState._F = ((2, 'my_node', 16, 4, mesh_pb2.MyNodeInfo, None), (3, 'owner', 16, 4, mesh_pb2.User, None), (5, 'receive_queue', 16, 1, mesh_pb2.MeshPacket, None), (7, 'rx_text_message', 16, 4, mesh_pb2.MeshPacket, None), (8, 'version', 2, 0, None, None), (9, 'no_save', 6, 0, None, None), (11, 'did_gps_reset', 6, 0, None, None), (12, 'rx_waypoint', 16, 4, mesh_pb2.MeshPacket, None), (13, 'node_remote_hardware_pins', 16, 1, mesh_pb2.NodeRemoteHardwarePin, None), )
NodePositionEntry._F = ((1, 'num', 2, 0, None, None), (2, 'position', 16, 4, PositionLite, None), )
NodeTelemetryEntry._F = ((1, 'num', 2, 0, None, None), (2, 'device_metrics', 16, 4, telemetry_pb2.DeviceMetrics, None), )
NodeEnvironmentEntry._F = ((1, 'num', 2, 0, None, None), (2, 'environment_metrics', 16, 4, telemetry_pb2.EnvironmentMetrics, None), )
NodeStatusEntry._F = ((1, 'num', 2, 0, None, None), (2, 'status', 16, 4, mesh_pb2.StatusMessage, None), )
NodeDatabase._F = ((1, 'version', 2, 0, None, None), (2, 'nodes', 16, 1, NodeInfoLite, None), (3, 'positions', 16, 1, NodePositionEntry, None), (4, 'telemetry', 16, 1, NodeTelemetryEntry, None), (5, 'status', 16, 1, NodeStatusEntry, None), (6, 'environment', 16, 1, NodeEnvironmentEntry, None), )
ChannelFile._F = ((1, 'channels', 16, 1, channel_pb2.Channel, None), (2, 'version', 2, 0, None, None), )
BackupPreferences._F = ((1, 'version', 2, 0, None, None), (2, 'timestamp', 8, 0, None, None), (3, 'config', 16, 4, localonly_pb2.LocalConfig, None), (4, 'module_config', 16, 4, localonly_pb2.LocalModuleConfig, None), (5, 'channels', 16, 4, ChannelFile, None), (6, 'owner', 16, 4, mesh_pb2.User, None), )
