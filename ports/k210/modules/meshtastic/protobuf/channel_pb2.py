# Generated from meshtastic/channel.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class ChannelSettings(Message):
    pass

class ModuleSettings(Message):
    pass

class Channel(Message):
    class Role(Enum):
        _V = (('DISABLED', 0), ('PRIMARY', 1), ('SECONDARY', 2), )
        DISABLED = 0
        PRIMARY = 1
        SECONDARY = 2
    DISABLED = 0
    PRIMARY = 1
    SECONDARY = 2

ChannelSettings._F = ((1, 'channel_num', 2, 0, None, None), (2, 'psk', 15, 0, None, None), (3, 'name', 14, 0, None, None), (4, 'id', 8, 0, None, None), (5, 'uplink_enabled', 6, 0, None, None), (6, 'downlink_enabled', 6, 0, None, None), (7, 'module_settings', 16, 4, ModuleSettings, None), (8, 'use_aead', 6, 0, None, None), )
ModuleSettings._F = ((1, 'position_precision', 2, 0, None, None), (2, 'is_muted', 6, 0, None, None), )
Channel._F = ((1, 'index', 0, 0, None, None), (2, 'settings', 16, 4, ChannelSettings, None), (3, 'role', 7, 0, None, None), )
