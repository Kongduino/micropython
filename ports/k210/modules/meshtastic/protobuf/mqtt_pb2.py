# Generated from meshtastic/mqtt.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import config_pb2
from meshtastic.protobuf import mesh_pb2

class ServiceEnvelope(Message):
    pass

class MapReport(Message):
    pass

ServiceEnvelope._F = ((1, 'packet', 16, 4, mesh_pb2.MeshPacket, None), (2, 'channel_id', 14, 0, None, None), (3, 'gateway_id', 14, 0, None, None), )
MapReport._F = ((1, 'long_name', 14, 0, None, None), (2, 'short_name', 14, 0, None, None), (3, 'role', 7, 0, None, None), (4, 'hw_model', 7, 0, None, None), (5, 'firmware_version', 14, 0, None, None), (6, 'region', 7, 0, None, None), (7, 'modem_preset', 7, 0, None, None), (8, 'has_default_channel', 6, 0, None, None), (9, 'latitude_i', 9, 0, None, None), (10, 'longitude_i', 9, 0, None, None), (11, 'altitude', 0, 0, None, None), (12, 'position_precision', 2, 0, None, None), (13, 'num_online_local_nodes', 2, 0, None, None), (14, 'has_opted_report_location', 6, 0, None, None), )
