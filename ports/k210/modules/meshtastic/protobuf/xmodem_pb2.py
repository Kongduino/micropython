# Generated from meshtastic/xmodem.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class XModem(Message):
    class Control(Enum):
        _V = (('NUL', 0), ('SOH', 1), ('STX', 2), ('EOT', 4), ('ACK', 6), ('NAK', 21), ('CAN', 24), ('CTRLZ', 26), )
        NUL = 0
        SOH = 1
        STX = 2
        EOT = 4
        ACK = 6
        NAK = 21
        CAN = 24
        CTRLZ = 26
    NUL = 0
    SOH = 1
    STX = 2
    EOT = 4
    ACK = 6
    NAK = 21
    CAN = 24
    CTRLZ = 26

XModem._F = ((1, 'control', 7, 0, None, None), (2, 'seq', 2, 0, None, None), (3, 'crc16', 2, 0, None, None), (4, 'buffer', 15, 0, None, None), )
