# Generated from meshtastic/interdevice.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class InterdeviceVersion(Enum):
    _V = (('INTERDEVICE_VERSION_UNSPECIFIED', 0), ('INTERDEVICE_VERSION_CURRENT', 2), )
    INTERDEVICE_VERSION_UNSPECIFIED = 0
    INTERDEVICE_VERSION_CURRENT = 2

class FileOperation(Enum):
    _V = (('GET', 0), ('POST', 1), ('PUT', 2), ('DELETE', 3), )
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3

class FileStatus(Enum):
    _V = (('FILE_UNSPECIFIED', 0), ('FILE_OK', 1), ('FILE_BUSY', 2), ('FILE_NO_CARD', 3), ('FILE_NOT_FOUND', 4), ('FILE_OFFSET_CONFLICT', 5), ('FILE_IO_ERROR', 6), ('FILE_NOT_A_FILE', 7), )
    FILE_UNSPECIFIED = 0
    FILE_OK = 1
    FILE_BUSY = 2
    FILE_NO_CARD = 3
    FILE_NOT_FOUND = 4
    FILE_OFFSET_CONFLICT = 5
    FILE_IO_ERROR = 6
    FILE_NOT_A_FILE = 7

class SdCommand(Enum):
    _V = (('SD_COMMAND_UNSPECIFIED', 0), ('SD_MOUNT', 1), ('SD_EJECT', 2), ('SD_FORMAT', 3), )
    SD_COMMAND_UNSPECIFIED = 0
    SD_MOUNT = 1
    SD_EJECT = 2
    SD_FORMAT = 3

class FileTransfer(Message):
    pass

class DirectoryListing(Message):
    pass

class I2CTransaction(Message):
    pass

class SdCardInfo(Message):
    class CardType(Enum):
        _V = (('NONE', 0), ('MMC', 1), ('SD', 2), ('SDHC', 3), ('SDXC', 4), ('UNKNOWN_CARD', 5), )
        NONE = 0
        MMC = 1
        SD = 2
        SDHC = 3
        SDXC = 4
        UNKNOWN_CARD = 5
    NONE = 0
    MMC = 1
    SD = 2
    SDHC = 3
    SDXC = 4
    UNKNOWN_CARD = 5
    class FatType(Enum):
        _V = (('UNKNOWN_FAT', 0), ('FAT16', 1), ('FAT32', 2), ('EXFAT', 3), )
        UNKNOWN_FAT = 0
        FAT16 = 1
        FAT32 = 2
        EXFAT = 3
    UNKNOWN_FAT = 0
    FAT16 = 1
    FAT32 = 2
    EXFAT = 3

class I2CResult(Message):
    class Status(Enum):
        _V = (('UNSPECIFIED', 0), ('OK', 1), ('NACK_ADDRESS', 2), ('NACK_DATA', 3), ('ERROR', 4), )
        UNSPECIFIED = 0
        OK = 1
        NACK_ADDRESS = 2
        NACK_DATA = 3
        ERROR = 4
    UNSPECIFIED = 0
    OK = 1
    NACK_ADDRESS = 2
    NACK_DATA = 3
    ERROR = 4

class InterdeviceMessage(Message):
    pass

INTERDEVICE_VERSION_UNSPECIFIED = 0
INTERDEVICE_VERSION_CURRENT = 2
GET = 0
POST = 1
PUT = 2
DELETE = 3
FILE_UNSPECIFIED = 0
FILE_OK = 1
FILE_BUSY = 2
FILE_NO_CARD = 3
FILE_NOT_FOUND = 4
FILE_OFFSET_CONFLICT = 5
FILE_IO_ERROR = 6
FILE_NOT_A_FILE = 7
SD_COMMAND_UNSPECIFIED = 0
SD_MOUNT = 1
SD_EJECT = 2
SD_FORMAT = 3
FileTransfer._F = ((1, 'operation', 7, 0, None, None), (2, 'filepath', 14, 0, None, None), (3, 'filedata', 15, 0, None, None), (4, 'status', 7, 0, None, None), (5, 'message', 14, 0, None, None), (6, 'offset', 3, 0, None, None), (7, 'length', 2, 0, None, None), (8, 'file_size', 3, 0, None, None), )
DirectoryListing._F = ((1, 'directory', 14, 0, None, None), (2, 'filenames', 14, 1, None, None), (3, 'status', 7, 0, None, None), (4, 'message', 14, 0, None, None), (5, 'offset', 2, 0, None, None), (6, 'total_count', 2, 0, None, None), )
I2CTransaction._F = ((1, 'address', 2, 0, None, None), (2, 'write_data', 15, 0, None, None), (3, 'read_len', 2, 0, None, None), )
SdCardInfo._F = ((1, 'present', 6, 0, None, None), (2, 'card_type', 7, 0, None, None), (3, 'fat_type', 7, 0, None, None), (4, 'card_size', 3, 0, None, None), (5, 'used_bytes', 3, 0, None, None), (6, 'free_bytes', 3, 0, None, None), (7, 'stats_valid', 6, 0, None, None), (8, 'busy', 6, 0, None, None), (9, 'unformatted', 6, 0, None, None), )
I2CResult._F = ((1, 'status', 7, 0, None, None), (2, 'read_data', 15, 0, None, None), )
InterdeviceMessage._F = ((1, 'nmea', 14, 4, None, 'data'), (2, 'beep', 2, 4, None, 'data'), (3, 'i2c_transaction', 16, 4, I2CTransaction, 'data'), (4, 'i2c_result', 16, 4, I2CResult, 'data'), (5, 'i2c_scan', 6, 4, None, 'data'), (6, 'i2c_scan_result', 15, 4, None, 'data'), (7, 'file_transfer', 16, 4, FileTransfer, 'data'), (8, 'directory_listing', 16, 4, DirectoryListing, 'data'), (9, 'get_sd_info', 6, 4, None, 'data'), (10, 'sd_info', 16, 4, SdCardInfo, 'data'), (11, 'ping', 7, 4, None, 'data'), (12, 'pong', 7, 4, None, 'data'), (13, 'nack', 6, 4, None, 'data'), (14, 'sd_command', 7, 4, None, 'data'), (15, 'id', 2, 0, None, None), )
