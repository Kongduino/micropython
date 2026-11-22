# Generated from meshtastic/apponly.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import channel_pb2
from meshtastic.protobuf import config_pb2

class ChannelSet(Message):
    pass

ChannelSet._F = ((1, 'settings', 16, 1, channel_pb2.ChannelSettings, None), (2, 'lora_config', 16, 4, config_pb2.Config.LoRaConfig, None), )
