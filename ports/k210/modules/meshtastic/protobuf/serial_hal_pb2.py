# Generated from meshtastic/serial_hal.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class SerialHalCommand(Message):
    class Type(Enum):
        _V = (('UNSET', 0), ('PIN_MODE', 1), ('DIGITAL_WRITE', 2), ('DIGITAL_READ', 3), ('ATTACH_INTERRUPT', 4), ('DETACH_INTERRUPT', 5), ('SPI_TRANSFER', 6), ('NOOP', 7), ('SPI_TRANSACTION', 8), )
        UNSET = 0
        PIN_MODE = 1
        DIGITAL_WRITE = 2
        DIGITAL_READ = 3
        ATTACH_INTERRUPT = 4
        DETACH_INTERRUPT = 5
        SPI_TRANSFER = 6
        NOOP = 7
        SPI_TRANSACTION = 8
    UNSET = 0
    PIN_MODE = 1
    DIGITAL_WRITE = 2
    DIGITAL_READ = 3
    ATTACH_INTERRUPT = 4
    DETACH_INTERRUPT = 5
    SPI_TRANSFER = 6
    NOOP = 7
    SPI_TRANSACTION = 8

class SerialHalResponse(Message):
    class Result(Enum):
        _V = (('OK', 0), ('ERROR', 1), ('BAD_REQUEST', 2), ('UNSUPPORTED', 3), )
        OK = 0
        ERROR = 1
        BAD_REQUEST = 2
        UNSUPPORTED = 3
    OK = 0
    ERROR = 1
    BAD_REQUEST = 2
    UNSUPPORTED = 3

SerialHalCommand._F = ((1, 'transaction_id', 2, 0, None, None), (2, 'type', 7, 0, None, None), (3, 'pin', 2, 0, None, None), (4, 'value', 2, 0, None, None), (5, 'mode', 2, 0, None, None), (6, 'data', 15, 0, None, None), )
SerialHalResponse._F = ((1, 'transaction_id', 2, 0, None, None), (2, 'result', 7, 0, None, None), (3, 'value', 2, 0, None, None), (4, 'data', 15, 0, None, None), (5, 'error', 14, 0, None, None), )
