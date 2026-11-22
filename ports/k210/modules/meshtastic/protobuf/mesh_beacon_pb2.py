# Generated from meshtastic/mesh_beacon.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import channel_pb2
from meshtastic.protobuf import config_pb2

class MeshBeacon(Message):
    pass

MeshBeacon._F = ((1, 'message', 14, 0, None, None), (2, 'offer_channel', 16, 4, channel_pb2.ChannelSettings, None), (3, 'offer_region', 7, 0, None, None), (4, 'offer_preset', 7, 4, None, None), (5, 'offer_frequency_slot', 2, 4, None, None), )
