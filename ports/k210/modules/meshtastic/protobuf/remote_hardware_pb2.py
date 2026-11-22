# Generated from meshtastic/remote_hardware.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class HardwareMessage(Message):
    class Type(Enum):
        _V = (('UNSET', 0), ('WRITE_GPIOS', 1), ('WATCH_GPIOS', 2), ('GPIOS_CHANGED', 3), ('READ_GPIOS', 4), ('READ_GPIOS_REPLY', 5), )
        UNSET = 0
        WRITE_GPIOS = 1
        WATCH_GPIOS = 2
        GPIOS_CHANGED = 3
        READ_GPIOS = 4
        READ_GPIOS_REPLY = 5
    UNSET = 0
    WRITE_GPIOS = 1
    WATCH_GPIOS = 2
    GPIOS_CHANGED = 3
    READ_GPIOS = 4
    READ_GPIOS_REPLY = 5

HardwareMessage._F = ((1, 'type', 7, 0, None, None), (2, 'gpio_mask', 3, 0, None, None), (3, 'gpio_value', 3, 0, None, None), )
