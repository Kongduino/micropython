# Generated from meshtastic/mesh.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import channel_pb2
from meshtastic.protobuf import config_pb2
from meshtastic.protobuf import device_ui_pb2
from meshtastic.protobuf import field_metadata_pb2
from meshtastic.protobuf import module_config_pb2
from meshtastic.protobuf import portnums_pb2
from meshtastic.protobuf import telemetry_pb2
from meshtastic.protobuf import xmodem_pb2

class HardwareModel(Enum):
    _V = (('UNSET', 0), ('TLORA_V2', 1), ('TLORA_V1', 2), ('TLORA_V2_1_1P6', 3), ('TBEAM', 4), ('HELTEC_V2_0', 5), ('TBEAM_V0P7', 6), ('T_ECHO', 7), ('TLORA_V1_1P3', 8), ('RAK4631', 9), ('HELTEC_V2_1', 10), ('HELTEC_V1', 11), ('LILYGO_TBEAM_S3_CORE', 12), ('RAK11200', 13), ('NANO_G1', 14), ('TLORA_V2_1_1P8', 15), ('TLORA_T3_S3', 16), ('NANO_G1_EXPLORER', 17), ('NANO_G2_ULTRA', 18), ('LORA_TYPE', 19), ('WIPHONE', 20), ('WIO_WM1110', 21), ('RAK2560', 22), ('HELTEC_HRU_3601', 23), ('HELTEC_WIRELESS_BRIDGE', 24), ('STATION_G1', 25), ('RAK11310', 26), ('MAKERFABS_TRACKER', 27), ('MAKERFABS_RESERVED', 28), ('CANARYONE', 29), ('RP2040_LORA', 30), ('STATION_G2', 31), ('LORA_RELAY_V1', 32), ('T_ECHO_PLUS', 33), ('PPR', 34), ('GENIEBLOCKS', 35), ('NRF52_UNKNOWN', 36), ('PORTDUINO', 37), ('ANDROID_SIM', 38), ('DIY_V1', 39), ('NRF52840_PCA10059', 40), ('DR_DEV', 41), ('M5STACK', 42), ('HELTEC_V3', 43), ('HELTEC_WSL_V3', 44), ('BETAFPV_2400_TX', 45), ('BETAFPV_900_NANO_TX', 46), ('RPI_PICO', 47), ('HELTEC_WIRELESS_TRACKER', 48), ('HELTEC_WIRELESS_PAPER', 49), ('T_DECK', 50), ('T_WATCH_S3', 51), ('PICOMPUTER_S3', 52), ('HELTEC_HT62', 53), ('EBYTE_ESP32_S3', 54), ('ESP32_S3_PICO', 55), ('CHATTER_2', 56), ('HELTEC_WIRELESS_PAPER_V1_0', 57), ('HELTEC_WIRELESS_TRACKER_V1_0', 58), ('UNPHONE', 59), ('TD_LORAC', 60), ('CDEBYTE_EORA_S3', 61), ('TWC_MESH_V4', 62), ('NRF52_PROMICRO_DIY', 63), ('RADIOMASTER_900_BANDIT_NANO', 64), ('HELTEC_CAPSULE_SENSOR_V3', 65), ('HELTEC_VISION_MASTER_T190', 66), ('HELTEC_VISION_MASTER_E213', 67), ('HELTEC_VISION_MASTER_E290', 68), ('HELTEC_MESH_NODE_T114', 69), ('SENSECAP_INDICATOR', 70), ('TRACKER_T1000_E', 71), ('RAK3172', 72), ('WIO_E5', 73), ('RADIOMASTER_900_BANDIT', 74), ('ME25LS01_4Y10TD', 75), ('RP2040_FEATHER_RFM95', 76), ('M5STACK_COREBASIC', 77), ('M5STACK_CORE2', 78), ('RPI_PICO2', 79), ('M5STACK_CORES3', 80), ('SEEED_XIAO_S3', 81), ('MS24SF1', 82), ('TLORA_C6', 83), ('WISMESH_TAP', 84), ('ROUTASTIC', 85), ('MESH_TAB', 86), ('MESHLINK', 87), ('XIAO_NRF52_KIT', 88), ('THINKNODE_M1', 89), ('THINKNODE_M2', 90), ('T_ETH_ELITE', 91), ('HELTEC_SENSOR_HUB', 92), ('MUZI_BASE', 93), ('HELTEC_MESH_POCKET', 94), ('SEEED_SOLAR_NODE', 95), ('NOMADSTAR_METEOR_PRO', 96), ('CROWPANEL', 97), ('LINK_32', 98), ('SEEED_WIO_TRACKER_L1', 99), ('SEEED_WIO_TRACKER_L1_EINK', 100), ('MUZI_R1_NEO', 101), ('T_DECK_PRO', 102), ('T_LORA_PAGER', 103), ('M5STACK_RESERVED', 104), ('WISMESH_TAG', 105), ('RAK3312', 106), ('THINKNODE_M5', 107), ('HELTEC_MESH_SOLAR', 108), ('T_ECHO_LITE', 109), ('HELTEC_V4', 110), ('M5STACK_C6L', 111), ('M5STACK_CARDPUTER_ADV', 112), ('HELTEC_WIRELESS_TRACKER_V2', 113), ('T_WATCH_ULTRA', 114), ('THINKNODE_M3', 115), ('WISMESH_TAP_V2', 116), ('RAK3401', 117), ('RAK6421', 118), ('THINKNODE_M4', 119), ('THINKNODE_M6', 120), ('MESHSTICK_1262', 121), ('TBEAM_1_WATT', 122), ('T5_S3_EPAPER_PRO', 123), ('TBEAM_BPF', 124), ('MINI_EPAPER_S3', 125), ('TDISPLAY_S3_PRO', 126), ('HELTEC_MESH_NODE_T096', 127), ('MESH_TRACKER_X1', 128), ('THINKNODE_M7', 129), ('THINKNODE_M8', 130), ('THINKNODE_M9', 131), ('HELTEC_V4_R8', 132), ('HELTEC_MESH_NODE_T1', 133), ('STATION_G3', 134), ('T_IMPULSE_PLUS', 135), ('T_ECHO_CARD', 136), ('SEEED_WIO_TRACKER_L2', 137), ('CROWPANEL_P4', 138), ('HELTEC_MESH_TOWER_V2', 139), ('MESHNOLOGY_W10', 140), ('HELTEC_RC32', 141), ('HELTEC_RC52', 142), ('HELTEC_RCC6', 143), ('SEEED_WIO_TRACKER_L1_PRO_1W', 144), ('MESHNOLOGY_W12', 145), ('MESHPAGER_X2', 146), ('T_CONNECT_PRO', 147), ('AXIOMETA_GENESIS_MINI', 148), ('MAKERFABS_NOMAD_TERMINAL', 149), ('THINKNODE_MX', 150), ('NODARA', 151), ('HELTEC_MESH_POCKET_V2', 152), ('PRIVATE_HW', 255), )
    UNSET = 0
    TLORA_V2 = 1
    TLORA_V1 = 2
    TLORA_V2_1_1P6 = 3
    TBEAM = 4
    HELTEC_V2_0 = 5
    TBEAM_V0P7 = 6
    T_ECHO = 7
    TLORA_V1_1P3 = 8
    RAK4631 = 9
    HELTEC_V2_1 = 10
    HELTEC_V1 = 11
    LILYGO_TBEAM_S3_CORE = 12
    RAK11200 = 13
    NANO_G1 = 14
    TLORA_V2_1_1P8 = 15
    TLORA_T3_S3 = 16
    NANO_G1_EXPLORER = 17
    NANO_G2_ULTRA = 18
    LORA_TYPE = 19
    WIPHONE = 20
    WIO_WM1110 = 21
    RAK2560 = 22
    HELTEC_HRU_3601 = 23
    HELTEC_WIRELESS_BRIDGE = 24
    STATION_G1 = 25
    RAK11310 = 26
    MAKERFABS_TRACKER = 27
    MAKERFABS_RESERVED = 28
    CANARYONE = 29
    RP2040_LORA = 30
    STATION_G2 = 31
    LORA_RELAY_V1 = 32
    T_ECHO_PLUS = 33
    PPR = 34
    GENIEBLOCKS = 35
    NRF52_UNKNOWN = 36
    PORTDUINO = 37
    ANDROID_SIM = 38
    DIY_V1 = 39
    NRF52840_PCA10059 = 40
    DR_DEV = 41
    M5STACK = 42
    HELTEC_V3 = 43
    HELTEC_WSL_V3 = 44
    BETAFPV_2400_TX = 45
    BETAFPV_900_NANO_TX = 46
    RPI_PICO = 47
    HELTEC_WIRELESS_TRACKER = 48
    HELTEC_WIRELESS_PAPER = 49
    T_DECK = 50
    T_WATCH_S3 = 51
    PICOMPUTER_S3 = 52
    HELTEC_HT62 = 53
    EBYTE_ESP32_S3 = 54
    ESP32_S3_PICO = 55
    CHATTER_2 = 56
    HELTEC_WIRELESS_PAPER_V1_0 = 57
    HELTEC_WIRELESS_TRACKER_V1_0 = 58
    UNPHONE = 59
    TD_LORAC = 60
    CDEBYTE_EORA_S3 = 61
    TWC_MESH_V4 = 62
    NRF52_PROMICRO_DIY = 63
    RADIOMASTER_900_BANDIT_NANO = 64
    HELTEC_CAPSULE_SENSOR_V3 = 65
    HELTEC_VISION_MASTER_T190 = 66
    HELTEC_VISION_MASTER_E213 = 67
    HELTEC_VISION_MASTER_E290 = 68
    HELTEC_MESH_NODE_T114 = 69
    SENSECAP_INDICATOR = 70
    TRACKER_T1000_E = 71
    RAK3172 = 72
    WIO_E5 = 73
    RADIOMASTER_900_BANDIT = 74
    ME25LS01_4Y10TD = 75
    RP2040_FEATHER_RFM95 = 76
    M5STACK_COREBASIC = 77
    M5STACK_CORE2 = 78
    RPI_PICO2 = 79
    M5STACK_CORES3 = 80
    SEEED_XIAO_S3 = 81
    MS24SF1 = 82
    TLORA_C6 = 83
    WISMESH_TAP = 84
    ROUTASTIC = 85
    MESH_TAB = 86
    MESHLINK = 87
    XIAO_NRF52_KIT = 88
    THINKNODE_M1 = 89
    THINKNODE_M2 = 90
    T_ETH_ELITE = 91
    HELTEC_SENSOR_HUB = 92
    MUZI_BASE = 93
    HELTEC_MESH_POCKET = 94
    SEEED_SOLAR_NODE = 95
    NOMADSTAR_METEOR_PRO = 96
    CROWPANEL = 97
    LINK_32 = 98
    SEEED_WIO_TRACKER_L1 = 99
    SEEED_WIO_TRACKER_L1_EINK = 100
    MUZI_R1_NEO = 101
    T_DECK_PRO = 102
    T_LORA_PAGER = 103
    M5STACK_RESERVED = 104
    WISMESH_TAG = 105
    RAK3312 = 106
    THINKNODE_M5 = 107
    HELTEC_MESH_SOLAR = 108
    T_ECHO_LITE = 109
    HELTEC_V4 = 110
    M5STACK_C6L = 111
    M5STACK_CARDPUTER_ADV = 112
    HELTEC_WIRELESS_TRACKER_V2 = 113
    T_WATCH_ULTRA = 114
    THINKNODE_M3 = 115
    WISMESH_TAP_V2 = 116
    RAK3401 = 117
    RAK6421 = 118
    THINKNODE_M4 = 119
    THINKNODE_M6 = 120
    MESHSTICK_1262 = 121
    TBEAM_1_WATT = 122
    T5_S3_EPAPER_PRO = 123
    TBEAM_BPF = 124
    MINI_EPAPER_S3 = 125
    TDISPLAY_S3_PRO = 126
    HELTEC_MESH_NODE_T096 = 127
    MESH_TRACKER_X1 = 128
    THINKNODE_M7 = 129
    THINKNODE_M8 = 130
    THINKNODE_M9 = 131
    HELTEC_V4_R8 = 132
    HELTEC_MESH_NODE_T1 = 133
    STATION_G3 = 134
    T_IMPULSE_PLUS = 135
    T_ECHO_CARD = 136
    SEEED_WIO_TRACKER_L2 = 137
    CROWPANEL_P4 = 138
    HELTEC_MESH_TOWER_V2 = 139
    MESHNOLOGY_W10 = 140
    HELTEC_RC32 = 141
    HELTEC_RC52 = 142
    HELTEC_RCC6 = 143
    SEEED_WIO_TRACKER_L1_PRO_1W = 144
    MESHNOLOGY_W12 = 145
    MESHPAGER_X2 = 146
    T_CONNECT_PRO = 147
    AXIOMETA_GENESIS_MINI = 148
    MAKERFABS_NOMAD_TERMINAL = 149
    THINKNODE_MX = 150
    NODARA = 151
    HELTEC_MESH_POCKET_V2 = 152
    PRIVATE_HW = 255

class Constants(Enum):
    _V = (('ZERO', 0), ('DATA_PAYLOAD_LEN', 233), )
    ZERO = 0
    DATA_PAYLOAD_LEN = 233

class CriticalErrorCode(Enum):
    _V = (('NONE', 0), ('TX_WATCHDOG', 1), ('SLEEP_ENTER_WAIT', 2), ('NO_RADIO', 3), ('UNSPECIFIED', 4), ('UBLOX_UNIT_FAILED', 5), ('NO_AXP192', 6), ('INVALID_RADIO_SETTING', 7), ('TRANSMIT_FAILED', 8), ('BROWNOUT', 9), ('SX1262_FAILURE', 10), ('RADIO_SPI_BUG', 11), ('FLASH_CORRUPTION_RECOVERABLE', 12), ('FLASH_CORRUPTION_UNRECOVERABLE', 13), )
    NONE = 0
    TX_WATCHDOG = 1
    SLEEP_ENTER_WAIT = 2
    NO_RADIO = 3
    UNSPECIFIED = 4
    UBLOX_UNIT_FAILED = 5
    NO_AXP192 = 6
    INVALID_RADIO_SETTING = 7
    TRANSMIT_FAILED = 8
    BROWNOUT = 9
    SX1262_FAILURE = 10
    RADIO_SPI_BUG = 11
    FLASH_CORRUPTION_RECOVERABLE = 12
    FLASH_CORRUPTION_UNRECOVERABLE = 13

class FirmwareEdition(Enum):
    _V = (('VANILLA', 0), ('SMART_CITIZEN', 1), ('OPEN_SAUCE', 16), ('DEFCON', 17), ('BURNING_MAN', 18), ('HAMVENTION', 19), ('FAB', 20), ('DRAGON_CON', 21), ('CCC', 22), ('DIY_EDITION', 127), )
    VANILLA = 0
    SMART_CITIZEN = 1
    OPEN_SAUCE = 16
    DEFCON = 17
    BURNING_MAN = 18
    HAMVENTION = 19
    FAB = 20
    DRAGON_CON = 21
    CCC = 22
    DIY_EDITION = 127

class ExcludedModules(Enum):
    _V = (('EXCLUDED_NONE', 0), ('MQTT_CONFIG', 1), ('SERIAL_CONFIG', 2), ('EXTNOTIF_CONFIG', 4), ('STOREFORWARD_CONFIG', 8), ('RANGETEST_CONFIG', 16), ('TELEMETRY_CONFIG', 32), ('CANNEDMSG_CONFIG', 64), ('AUDIO_CONFIG', 128), ('REMOTEHARDWARE_CONFIG', 256), ('NEIGHBORINFO_CONFIG', 512), ('AMBIENTLIGHTING_CONFIG', 1024), ('DETECTIONSENSOR_CONFIG', 2048), ('PAXCOUNTER_CONFIG', 4096), ('BLUETOOTH_CONFIG', 8192), ('NETWORK_CONFIG', 16384), ('STATUSMESSAGE_CONFIG', 32768), ('TRAFFICMANAGEMENT_CONFIG', 65536), ('TAK_CONFIG', 131072), ('MESHBEACON_CONFIG', 262144), )
    EXCLUDED_NONE = 0
    MQTT_CONFIG = 1
    SERIAL_CONFIG = 2
    EXTNOTIF_CONFIG = 4
    STOREFORWARD_CONFIG = 8
    RANGETEST_CONFIG = 16
    TELEMETRY_CONFIG = 32
    CANNEDMSG_CONFIG = 64
    AUDIO_CONFIG = 128
    REMOTEHARDWARE_CONFIG = 256
    NEIGHBORINFO_CONFIG = 512
    AMBIENTLIGHTING_CONFIG = 1024
    DETECTIONSENSOR_CONFIG = 2048
    PAXCOUNTER_CONFIG = 4096
    BLUETOOTH_CONFIG = 8192
    NETWORK_CONFIG = 16384
    STATUSMESSAGE_CONFIG = 32768
    TRAFFICMANAGEMENT_CONFIG = 65536
    TAK_CONFIG = 131072
    MESHBEACON_CONFIG = 262144

class Position(Message):
    class LocSource(Enum):
        _V = (('LOC_UNSET', 0), ('LOC_MANUAL', 1), ('LOC_INTERNAL', 2), ('LOC_EXTERNAL', 3), )
        LOC_UNSET = 0
        LOC_MANUAL = 1
        LOC_INTERNAL = 2
        LOC_EXTERNAL = 3
    LOC_UNSET = 0
    LOC_MANUAL = 1
    LOC_INTERNAL = 2
    LOC_EXTERNAL = 3
    class AltSource(Enum):
        _V = (('ALT_UNSET', 0), ('ALT_MANUAL', 1), ('ALT_INTERNAL', 2), ('ALT_EXTERNAL', 3), ('ALT_BAROMETRIC', 4), )
        ALT_UNSET = 0
        ALT_MANUAL = 1
        ALT_INTERNAL = 2
        ALT_EXTERNAL = 3
        ALT_BAROMETRIC = 4
    ALT_UNSET = 0
    ALT_MANUAL = 1
    ALT_INTERNAL = 2
    ALT_EXTERNAL = 3
    ALT_BAROMETRIC = 4

class User(Message):
    pass

class RouteDiscovery(Message):
    pass

class Routing(Message):
    class Error(Enum):
        _V = (('NONE', 0), ('NO_ROUTE', 1), ('GOT_NAK', 2), ('TIMEOUT', 3), ('NO_INTERFACE', 4), ('MAX_RETRANSMIT', 5), ('NO_CHANNEL', 6), ('TOO_LARGE', 7), ('NO_RESPONSE', 8), ('DUTY_CYCLE_LIMIT', 9), ('BAD_REQUEST', 32), ('NOT_AUTHORIZED', 33), ('PKI_FAILED', 34), ('PKI_UNKNOWN_PUBKEY', 35), ('ADMIN_BAD_SESSION_KEY', 36), ('ADMIN_PUBLIC_KEY_UNAUTHORIZED', 37), ('RATE_LIMIT_EXCEEDED', 38), ('PKI_SEND_FAIL_PUBLIC_KEY', 39), )
        NONE = 0
        NO_ROUTE = 1
        GOT_NAK = 2
        TIMEOUT = 3
        NO_INTERFACE = 4
        MAX_RETRANSMIT = 5
        NO_CHANNEL = 6
        TOO_LARGE = 7
        NO_RESPONSE = 8
        DUTY_CYCLE_LIMIT = 9
        BAD_REQUEST = 32
        NOT_AUTHORIZED = 33
        PKI_FAILED = 34
        PKI_UNKNOWN_PUBKEY = 35
        ADMIN_BAD_SESSION_KEY = 36
        ADMIN_PUBLIC_KEY_UNAUTHORIZED = 37
        RATE_LIMIT_EXCEEDED = 38
        PKI_SEND_FAIL_PUBLIC_KEY = 39
    NONE = 0
    NO_ROUTE = 1
    GOT_NAK = 2
    TIMEOUT = 3
    NO_INTERFACE = 4
    MAX_RETRANSMIT = 5
    NO_CHANNEL = 6
    TOO_LARGE = 7
    NO_RESPONSE = 8
    DUTY_CYCLE_LIMIT = 9
    BAD_REQUEST = 32
    NOT_AUTHORIZED = 33
    PKI_FAILED = 34
    PKI_UNKNOWN_PUBKEY = 35
    ADMIN_BAD_SESSION_KEY = 36
    ADMIN_PUBLIC_KEY_UNAUTHORIZED = 37
    RATE_LIMIT_EXCEEDED = 38
    PKI_SEND_FAIL_PUBLIC_KEY = 39

class Data(Message):
    pass

class KeyVerification(Message):
    pass

class StoreForwardPlusPlus(Message):
    class SFPP_message_type(Enum):
        _V = (('CANON_ANNOUNCE', 0), ('CHAIN_QUERY', 1), ('LINK_REQUEST', 3), ('LINK_PROVIDE', 4), ('LINK_PROVIDE_FIRSTHALF', 5), ('LINK_PROVIDE_SECONDHALF', 6), )
        CANON_ANNOUNCE = 0
        CHAIN_QUERY = 1
        LINK_REQUEST = 3
        LINK_PROVIDE = 4
        LINK_PROVIDE_FIRSTHALF = 5
        LINK_PROVIDE_SECONDHALF = 6
    CANON_ANNOUNCE = 0
    CHAIN_QUERY = 1
    LINK_REQUEST = 3
    LINK_PROVIDE = 4
    LINK_PROVIDE_FIRSTHALF = 5
    LINK_PROVIDE_SECONDHALF = 6

class RemoteShell(Message):
    class OpCode(Enum):
        _V = (('OP_UNSET', 0), ('OPEN', 1), ('INPUT', 2), ('RESIZE', 3), ('CLOSE', 4), ('PING', 5), ('ACK', 6), ('OPEN_OK', 64), ('OUTPUT', 65), ('CLOSED', 66), ('ERROR', 67), ('PONG', 68), )
        OP_UNSET = 0
        OPEN = 1
        INPUT = 2
        RESIZE = 3
        CLOSE = 4
        PING = 5
        ACK = 6
        OPEN_OK = 64
        OUTPUT = 65
        CLOSED = 66
        ERROR = 67
        PONG = 68
    OP_UNSET = 0
    OPEN = 1
    INPUT = 2
    RESIZE = 3
    CLOSE = 4
    PING = 5
    ACK = 6
    OPEN_OK = 64
    OUTPUT = 65
    CLOSED = 66
    ERROR = 67
    PONG = 68

class BoundingBox(Message):
    pass

class Waypoint(Message):
    pass

class StatusMessage(Message):
    pass

class MqttClientProxyMessage(Message):
    pass

class MeshPacket(Message):
    class Priority(Enum):
        _V = (('UNSET', 0), ('MIN', 1), ('BACKGROUND', 10), ('DEFAULT', 64), ('RELIABLE', 70), ('RESPONSE', 80), ('HIGH', 100), ('ALERT', 110), ('ACK', 120), ('MAX', 127), )
        UNSET = 0
        MIN = 1
        BACKGROUND = 10
        DEFAULT = 64
        RELIABLE = 70
        RESPONSE = 80
        HIGH = 100
        ALERT = 110
        ACK = 120
        MAX = 127
    UNSET = 0
    MIN = 1
    BACKGROUND = 10
    DEFAULT = 64
    RELIABLE = 70
    RESPONSE = 80
    HIGH = 100
    ALERT = 110
    ACK = 120
    MAX = 127
    class Delayed(Enum):
        _V = (('NO_DELAY', 0), ('DELAYED_BROADCAST', 1), ('DELAYED_DIRECT', 2), )
        NO_DELAY = 0
        DELAYED_BROADCAST = 1
        DELAYED_DIRECT = 2
    NO_DELAY = 0
    DELAYED_BROADCAST = 1
    DELAYED_DIRECT = 2
    class TransportMechanism(Enum):
        _V = (('TRANSPORT_INTERNAL', 0), ('TRANSPORT_LORA', 1), ('TRANSPORT_LORA_ALT1', 2), ('TRANSPORT_LORA_ALT2', 3), ('TRANSPORT_LORA_ALT3', 4), ('TRANSPORT_MQTT', 5), ('TRANSPORT_MULTICAST_UDP', 6), ('TRANSPORT_API', 7), ('TRANSPORT_UNICAST_UDP', 8), )
        TRANSPORT_INTERNAL = 0
        TRANSPORT_LORA = 1
        TRANSPORT_LORA_ALT1 = 2
        TRANSPORT_LORA_ALT2 = 3
        TRANSPORT_LORA_ALT3 = 4
        TRANSPORT_MQTT = 5
        TRANSPORT_MULTICAST_UDP = 6
        TRANSPORT_API = 7
        TRANSPORT_UNICAST_UDP = 8
    TRANSPORT_INTERNAL = 0
    TRANSPORT_LORA = 1
    TRANSPORT_LORA_ALT1 = 2
    TRANSPORT_LORA_ALT2 = 3
    TRANSPORT_LORA_ALT3 = 4
    TRANSPORT_MQTT = 5
    TRANSPORT_MULTICAST_UDP = 6
    TRANSPORT_API = 7
    TRANSPORT_UNICAST_UDP = 8
    class AckProofStatus(Enum):
        _V = (('ACK_PROOF_ABSENT', 0), ('ACK_PROOF_VALID', 1), ('ACK_PROOF_INVALID', 2), ('ACK_PROOF_NO_KEY', 3), )
        ACK_PROOF_ABSENT = 0
        ACK_PROOF_VALID = 1
        ACK_PROOF_INVALID = 2
        ACK_PROOF_NO_KEY = 3
    ACK_PROOF_ABSENT = 0
    ACK_PROOF_VALID = 1
    ACK_PROOF_INVALID = 2
    ACK_PROOF_NO_KEY = 3
    class SlotParity(Enum):
        _V = (('SLOT_PARITY_UNSET', 0), ('SLOT_PARITY_EVEN', 1), ('SLOT_PARITY_ODD', 2), )
        SLOT_PARITY_UNSET = 0
        SLOT_PARITY_EVEN = 1
        SLOT_PARITY_ODD = 2
    SLOT_PARITY_UNSET = 0
    SLOT_PARITY_EVEN = 1
    SLOT_PARITY_ODD = 2

class NodeInfo(Message):
    pass

class MyNodeInfo(Message):
    pass

class LogRecord(Message):
    class Level(Enum):
        _V = (('UNSET', 0), ('CRITICAL', 50), ('ERROR', 40), ('WARNING', 30), ('INFO', 20), ('DEBUG', 10), ('TRACE', 5), )
        UNSET = 0
        CRITICAL = 50
        ERROR = 40
        WARNING = 30
        INFO = 20
        DEBUG = 10
        TRACE = 5
    UNSET = 0
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    TRACE = 5

class QueueStatus(Message):
    pass

class FromRadio(Message):
    pass

class DisplayFrame(Message):
    class Format(Enum):
        _V = (('FORMAT_UNSPECIFIED', 0), ('MONO_VLSB', 1), ('RGB565', 2), )
        FORMAT_UNSPECIFIED = 0
        MONO_VLSB = 1
        RGB565 = 2
    FORMAT_UNSPECIFIED = 0
    MONO_VLSB = 1
    RGB565 = 2

class DisplayPalette(Message):
    class ColorRegion(Message):
        pass

class LockdownStatus(Message):
    class State(Enum):
        _V = (('STATE_UNSPECIFIED', 0), ('NEEDS_PROVISION', 1), ('LOCKED', 2), ('UNLOCKED', 3), ('UNLOCK_FAILED', 4), ('DISABLED', 5), )
        STATE_UNSPECIFIED = 0
        NEEDS_PROVISION = 1
        LOCKED = 2
        UNLOCKED = 3
        UNLOCK_FAILED = 4
        DISABLED = 5
    STATE_UNSPECIFIED = 0
    NEEDS_PROVISION = 1
    LOCKED = 2
    UNLOCKED = 3
    UNLOCK_FAILED = 4
    DISABLED = 5

class ClientNotification(Message):
    class NotificationType(Enum):
        _V = (('UNSET', 0), ('POSITION_SHARING_DISABLED', 1), ('TRACEROUTE_RATE_LIMITED', 2), ('TRACEROUTE_BROADCAST_REJECTED', 3), ('DUTY_CYCLE_LIMIT_EXCEEDED', 4), ('POSITION_SENT_SLEEPING', 5), ('TELEMETRY_SENT_SLEEPING', 6), ('KEY_VERIFICATION_NUMBER_INFORM', 7), ('KEY_VERIFICATION_NUMBER_REQUEST', 8), ('KEY_VERIFICATION_FINAL_INCOMING', 9), ('KEY_VERIFICATION_FINAL_OUTGOING', 10), ('KEY_VERIFICATION_LICENSED_UNAVAILABLE', 11), ('DUPLICATED_PUBLIC_KEY', 12), ('LOW_ENTROPY_KEY_REGENERATED', 13), ('LOW_ENTROPY_KEY_RESTORE_REJECTED', 14), ('LICENSED_MODE_ACTIVATED', 15), ('LICENSED_IDENTITY_WILL_CHANGE', 16), ('LICENSED_IDENTITY_CHANGED', 17), ('PROTECTED_NODE_LIMIT_REACHED', 18), ('ROUTER_REBROADCAST_NONE_REJECTED', 19), ('PACKET_SIGNATURE_POLICY_UNAVAILABLE', 20), ('MANAGED_MODE_REQUIRES_ADMIN_KEY', 21), ('PUBLIC_CHANNEL_POSITION_PRECISION_REDUCED', 22), ('CHANNEL_BLANK_PSK', 23), ('CHANNEL_NAME_PRESET_MISTYPE', 24), ('CHANNEL_NAME_PRESET_MISTYPE_CLEAR_NAME', 42), ('CHANNEL_PRESET_NON_DEFAULT_KEY', 25), ('CHANNEL_NAME_MATCHES_OLD_PRESET', 26), ('CHANNEL_NAME_WONT_AUTO_RESOLVE', 27), ('CHANNEL_NAME_ISSUES', 28), ('CHANNEL_PSK_ISSUES', 29), ('CHANNEL_NAME_AND_PSK_ISSUES', 30), ('LORA_REGION_UNRECOGNIZED', 31), ('LORA_REGION_REQUIRES_LICENSE', 32), ('LORA_REGION_UNSUPPORTED_BY_RADIO', 33), ('LORA_PRESET_REGION_SWAP', 34), ('LORA_PRESET_INVALID_FOR_REGION', 35), ('LORA_BANDWIDTH_EXCEEDS_REGION', 36), ('LORA_CHANNEL_NUM_INVALID', 37), ('SERIAL_CONSOLE_OVERRIDE_INVALID', 38), ('MQTT_SERVER_UNREACHABLE', 39), ('MQTT_PROXY_TO_CLIENT_REQUIRED', 40), ('MQTT_DEFAULT_SERVER_PORT_INVALID', 41), ('OTA_INVALID_HASH', 43), ('OTA_LOADER_PARTITION_MISSING', 44), ('OTA_LOADER_INVALID', 45), ('OTA_MODE_UNSUPPORTED', 46), ('OTA_REBOOTING', 47), ('OTA_PARTITION_SWITCH_FAILED', 48), ('UNSIGNED_IDENTITY_UPDATE_IGNORED', 49), )
        UNSET = 0
        POSITION_SHARING_DISABLED = 1
        TRACEROUTE_RATE_LIMITED = 2
        TRACEROUTE_BROADCAST_REJECTED = 3
        DUTY_CYCLE_LIMIT_EXCEEDED = 4
        POSITION_SENT_SLEEPING = 5
        TELEMETRY_SENT_SLEEPING = 6
        KEY_VERIFICATION_NUMBER_INFORM = 7
        KEY_VERIFICATION_NUMBER_REQUEST = 8
        KEY_VERIFICATION_FINAL_INCOMING = 9
        KEY_VERIFICATION_FINAL_OUTGOING = 10
        KEY_VERIFICATION_LICENSED_UNAVAILABLE = 11
        DUPLICATED_PUBLIC_KEY = 12
        LOW_ENTROPY_KEY_REGENERATED = 13
        LOW_ENTROPY_KEY_RESTORE_REJECTED = 14
        LICENSED_MODE_ACTIVATED = 15
        LICENSED_IDENTITY_WILL_CHANGE = 16
        LICENSED_IDENTITY_CHANGED = 17
        PROTECTED_NODE_LIMIT_REACHED = 18
        ROUTER_REBROADCAST_NONE_REJECTED = 19
        PACKET_SIGNATURE_POLICY_UNAVAILABLE = 20
        MANAGED_MODE_REQUIRES_ADMIN_KEY = 21
        PUBLIC_CHANNEL_POSITION_PRECISION_REDUCED = 22
        CHANNEL_BLANK_PSK = 23
        CHANNEL_NAME_PRESET_MISTYPE = 24
        CHANNEL_NAME_PRESET_MISTYPE_CLEAR_NAME = 42
        CHANNEL_PRESET_NON_DEFAULT_KEY = 25
        CHANNEL_NAME_MATCHES_OLD_PRESET = 26
        CHANNEL_NAME_WONT_AUTO_RESOLVE = 27
        CHANNEL_NAME_ISSUES = 28
        CHANNEL_PSK_ISSUES = 29
        CHANNEL_NAME_AND_PSK_ISSUES = 30
        LORA_REGION_UNRECOGNIZED = 31
        LORA_REGION_REQUIRES_LICENSE = 32
        LORA_REGION_UNSUPPORTED_BY_RADIO = 33
        LORA_PRESET_REGION_SWAP = 34
        LORA_PRESET_INVALID_FOR_REGION = 35
        LORA_BANDWIDTH_EXCEEDS_REGION = 36
        LORA_CHANNEL_NUM_INVALID = 37
        SERIAL_CONSOLE_OVERRIDE_INVALID = 38
        MQTT_SERVER_UNREACHABLE = 39
        MQTT_PROXY_TO_CLIENT_REQUIRED = 40
        MQTT_DEFAULT_SERVER_PORT_INVALID = 41
        OTA_INVALID_HASH = 43
        OTA_LOADER_PARTITION_MISSING = 44
        OTA_LOADER_INVALID = 45
        OTA_MODE_UNSUPPORTED = 46
        OTA_REBOOTING = 47
        OTA_PARTITION_SWITCH_FAILED = 48
        UNSIGNED_IDENTITY_UPDATE_IGNORED = 49
    UNSET = 0
    POSITION_SHARING_DISABLED = 1
    TRACEROUTE_RATE_LIMITED = 2
    TRACEROUTE_BROADCAST_REJECTED = 3
    DUTY_CYCLE_LIMIT_EXCEEDED = 4
    POSITION_SENT_SLEEPING = 5
    TELEMETRY_SENT_SLEEPING = 6
    KEY_VERIFICATION_NUMBER_INFORM = 7
    KEY_VERIFICATION_NUMBER_REQUEST = 8
    KEY_VERIFICATION_FINAL_INCOMING = 9
    KEY_VERIFICATION_FINAL_OUTGOING = 10
    KEY_VERIFICATION_LICENSED_UNAVAILABLE = 11
    DUPLICATED_PUBLIC_KEY = 12
    LOW_ENTROPY_KEY_REGENERATED = 13
    LOW_ENTROPY_KEY_RESTORE_REJECTED = 14
    LICENSED_MODE_ACTIVATED = 15
    LICENSED_IDENTITY_WILL_CHANGE = 16
    LICENSED_IDENTITY_CHANGED = 17
    PROTECTED_NODE_LIMIT_REACHED = 18
    ROUTER_REBROADCAST_NONE_REJECTED = 19
    PACKET_SIGNATURE_POLICY_UNAVAILABLE = 20
    MANAGED_MODE_REQUIRES_ADMIN_KEY = 21
    PUBLIC_CHANNEL_POSITION_PRECISION_REDUCED = 22
    CHANNEL_BLANK_PSK = 23
    CHANNEL_NAME_PRESET_MISTYPE = 24
    CHANNEL_NAME_PRESET_MISTYPE_CLEAR_NAME = 42
    CHANNEL_PRESET_NON_DEFAULT_KEY = 25
    CHANNEL_NAME_MATCHES_OLD_PRESET = 26
    CHANNEL_NAME_WONT_AUTO_RESOLVE = 27
    CHANNEL_NAME_ISSUES = 28
    CHANNEL_PSK_ISSUES = 29
    CHANNEL_NAME_AND_PSK_ISSUES = 30
    LORA_REGION_UNRECOGNIZED = 31
    LORA_REGION_REQUIRES_LICENSE = 32
    LORA_REGION_UNSUPPORTED_BY_RADIO = 33
    LORA_PRESET_REGION_SWAP = 34
    LORA_PRESET_INVALID_FOR_REGION = 35
    LORA_BANDWIDTH_EXCEEDS_REGION = 36
    LORA_CHANNEL_NUM_INVALID = 37
    SERIAL_CONSOLE_OVERRIDE_INVALID = 38
    MQTT_SERVER_UNREACHABLE = 39
    MQTT_PROXY_TO_CLIENT_REQUIRED = 40
    MQTT_DEFAULT_SERVER_PORT_INVALID = 41
    OTA_INVALID_HASH = 43
    OTA_LOADER_PARTITION_MISSING = 44
    OTA_LOADER_INVALID = 45
    OTA_MODE_UNSUPPORTED = 46
    OTA_REBOOTING = 47
    OTA_PARTITION_SWITCH_FAILED = 48
    UNSIGNED_IDENTITY_UPDATE_IGNORED = 49

class KeyVerificationNumberInform(Message):
    pass

class KeyVerificationNumberRequest(Message):
    pass

class KeyVerificationFinal(Message):
    pass

class DuplicatedPublicKey(Message):
    pass

class LowEntropyKey(Message):
    pass

class FileInfo(Message):
    pass

class ToRadio(Message):
    pass

class Compressed(Message):
    pass

class NeighborInfo(Message):
    pass

class Neighbor(Message):
    pass

class DeviceMetadata(Message):
    pass

class DisplayInfo(Message):
    class PanelClass(Enum):
        _V = (('PANEL_CLASS_UNSPECIFIED', 0), ('OLED', 1), ('LCD', 2), ('TFT', 3), ('EINK', 4), ('HUB75', 5), )
        PANEL_CLASS_UNSPECIFIED = 0
        OLED = 1
        LCD = 2
        TFT = 3
        EINK = 4
        HUB75 = 5
    PANEL_CLASS_UNSPECIFIED = 0
    OLED = 1
    LCD = 2
    TFT = 3
    EINK = 4
    HUB75 = 5

class LoRaPresetGroup(Message):
    pass

class LoRaRegionPresets(Message):
    pass

class LoRaRegionPresetMap(Message):
    pass

class Heartbeat(Message):
    pass

class NodeRemoteHardwarePin(Message):
    pass

class ChunkedPayload(Message):
    pass

class resend_chunks(Message):
    pass

class ChunkedPayloadResponse(Message):
    pass

UNSET = 0
TLORA_V2 = 1
TLORA_V1 = 2
TLORA_V2_1_1P6 = 3
TBEAM = 4
HELTEC_V2_0 = 5
TBEAM_V0P7 = 6
T_ECHO = 7
TLORA_V1_1P3 = 8
RAK4631 = 9
HELTEC_V2_1 = 10
HELTEC_V1 = 11
LILYGO_TBEAM_S3_CORE = 12
RAK11200 = 13
NANO_G1 = 14
TLORA_V2_1_1P8 = 15
TLORA_T3_S3 = 16
NANO_G1_EXPLORER = 17
NANO_G2_ULTRA = 18
LORA_TYPE = 19
WIPHONE = 20
WIO_WM1110 = 21
RAK2560 = 22
HELTEC_HRU_3601 = 23
HELTEC_WIRELESS_BRIDGE = 24
STATION_G1 = 25
RAK11310 = 26
MAKERFABS_TRACKER = 27
MAKERFABS_RESERVED = 28
CANARYONE = 29
RP2040_LORA = 30
STATION_G2 = 31
LORA_RELAY_V1 = 32
T_ECHO_PLUS = 33
PPR = 34
GENIEBLOCKS = 35
NRF52_UNKNOWN = 36
PORTDUINO = 37
ANDROID_SIM = 38
DIY_V1 = 39
NRF52840_PCA10059 = 40
DR_DEV = 41
M5STACK = 42
HELTEC_V3 = 43
HELTEC_WSL_V3 = 44
BETAFPV_2400_TX = 45
BETAFPV_900_NANO_TX = 46
RPI_PICO = 47
HELTEC_WIRELESS_TRACKER = 48
HELTEC_WIRELESS_PAPER = 49
T_DECK = 50
T_WATCH_S3 = 51
PICOMPUTER_S3 = 52
HELTEC_HT62 = 53
EBYTE_ESP32_S3 = 54
ESP32_S3_PICO = 55
CHATTER_2 = 56
HELTEC_WIRELESS_PAPER_V1_0 = 57
HELTEC_WIRELESS_TRACKER_V1_0 = 58
UNPHONE = 59
TD_LORAC = 60
CDEBYTE_EORA_S3 = 61
TWC_MESH_V4 = 62
NRF52_PROMICRO_DIY = 63
RADIOMASTER_900_BANDIT_NANO = 64
HELTEC_CAPSULE_SENSOR_V3 = 65
HELTEC_VISION_MASTER_T190 = 66
HELTEC_VISION_MASTER_E213 = 67
HELTEC_VISION_MASTER_E290 = 68
HELTEC_MESH_NODE_T114 = 69
SENSECAP_INDICATOR = 70
TRACKER_T1000_E = 71
RAK3172 = 72
WIO_E5 = 73
RADIOMASTER_900_BANDIT = 74
ME25LS01_4Y10TD = 75
RP2040_FEATHER_RFM95 = 76
M5STACK_COREBASIC = 77
M5STACK_CORE2 = 78
RPI_PICO2 = 79
M5STACK_CORES3 = 80
SEEED_XIAO_S3 = 81
MS24SF1 = 82
TLORA_C6 = 83
WISMESH_TAP = 84
ROUTASTIC = 85
MESH_TAB = 86
MESHLINK = 87
XIAO_NRF52_KIT = 88
THINKNODE_M1 = 89
THINKNODE_M2 = 90
T_ETH_ELITE = 91
HELTEC_SENSOR_HUB = 92
MUZI_BASE = 93
HELTEC_MESH_POCKET = 94
SEEED_SOLAR_NODE = 95
NOMADSTAR_METEOR_PRO = 96
CROWPANEL = 97
LINK_32 = 98
SEEED_WIO_TRACKER_L1 = 99
SEEED_WIO_TRACKER_L1_EINK = 100
MUZI_R1_NEO = 101
T_DECK_PRO = 102
T_LORA_PAGER = 103
M5STACK_RESERVED = 104
WISMESH_TAG = 105
RAK3312 = 106
THINKNODE_M5 = 107
HELTEC_MESH_SOLAR = 108
T_ECHO_LITE = 109
HELTEC_V4 = 110
M5STACK_C6L = 111
M5STACK_CARDPUTER_ADV = 112
HELTEC_WIRELESS_TRACKER_V2 = 113
T_WATCH_ULTRA = 114
THINKNODE_M3 = 115
WISMESH_TAP_V2 = 116
RAK3401 = 117
RAK6421 = 118
THINKNODE_M4 = 119
THINKNODE_M6 = 120
MESHSTICK_1262 = 121
TBEAM_1_WATT = 122
T5_S3_EPAPER_PRO = 123
TBEAM_BPF = 124
MINI_EPAPER_S3 = 125
TDISPLAY_S3_PRO = 126
HELTEC_MESH_NODE_T096 = 127
MESH_TRACKER_X1 = 128
THINKNODE_M7 = 129
THINKNODE_M8 = 130
THINKNODE_M9 = 131
HELTEC_V4_R8 = 132
HELTEC_MESH_NODE_T1 = 133
STATION_G3 = 134
T_IMPULSE_PLUS = 135
T_ECHO_CARD = 136
SEEED_WIO_TRACKER_L2 = 137
CROWPANEL_P4 = 138
HELTEC_MESH_TOWER_V2 = 139
MESHNOLOGY_W10 = 140
HELTEC_RC32 = 141
HELTEC_RC52 = 142
HELTEC_RCC6 = 143
SEEED_WIO_TRACKER_L1_PRO_1W = 144
MESHNOLOGY_W12 = 145
MESHPAGER_X2 = 146
T_CONNECT_PRO = 147
AXIOMETA_GENESIS_MINI = 148
MAKERFABS_NOMAD_TERMINAL = 149
THINKNODE_MX = 150
NODARA = 151
HELTEC_MESH_POCKET_V2 = 152
PRIVATE_HW = 255
ZERO = 0
DATA_PAYLOAD_LEN = 233
NONE = 0
TX_WATCHDOG = 1
SLEEP_ENTER_WAIT = 2
NO_RADIO = 3
UNSPECIFIED = 4
UBLOX_UNIT_FAILED = 5
NO_AXP192 = 6
INVALID_RADIO_SETTING = 7
TRANSMIT_FAILED = 8
BROWNOUT = 9
SX1262_FAILURE = 10
RADIO_SPI_BUG = 11
FLASH_CORRUPTION_RECOVERABLE = 12
FLASH_CORRUPTION_UNRECOVERABLE = 13
VANILLA = 0
SMART_CITIZEN = 1
OPEN_SAUCE = 16
DEFCON = 17
BURNING_MAN = 18
HAMVENTION = 19
FAB = 20
DRAGON_CON = 21
CCC = 22
DIY_EDITION = 127
EXCLUDED_NONE = 0
MQTT_CONFIG = 1
SERIAL_CONFIG = 2
EXTNOTIF_CONFIG = 4
STOREFORWARD_CONFIG = 8
RANGETEST_CONFIG = 16
TELEMETRY_CONFIG = 32
CANNEDMSG_CONFIG = 64
AUDIO_CONFIG = 128
REMOTEHARDWARE_CONFIG = 256
NEIGHBORINFO_CONFIG = 512
AMBIENTLIGHTING_CONFIG = 1024
DETECTIONSENSOR_CONFIG = 2048
PAXCOUNTER_CONFIG = 4096
BLUETOOTH_CONFIG = 8192
NETWORK_CONFIG = 16384
STATUSMESSAGE_CONFIG = 32768
TRAFFICMANAGEMENT_CONFIG = 65536
TAK_CONFIG = 131072
MESHBEACON_CONFIG = 262144
Position._F = ((1, 'latitude_i', 9, 4, None, None), (2, 'longitude_i', 9, 4, None, None), (3, 'altitude', 0, 4, None, None), (4, 'time', 8, 0, None, None), (5, 'location_source', 7, 0, None, None), (6, 'altitude_source', 7, 0, None, None), (7, 'timestamp', 8, 0, None, None), (8, 'timestamp_millis_adjust', 0, 0, None, None), (9, 'altitude_hae', 4, 4, None, None), (10, 'altitude_geoidal_separation', 4, 4, None, None), (11, 'PDOP', 2, 0, None, None), (12, 'HDOP', 2, 0, None, None), (13, 'VDOP', 2, 0, None, None), (14, 'gps_accuracy', 2, 0, None, None), (15, 'ground_speed', 2, 4, None, None), (16, 'ground_track', 2, 4, None, None), (17, 'fix_quality', 2, 0, None, None), (18, 'fix_type', 2, 0, None, None), (19, 'sats_in_view', 2, 0, None, None), (20, 'sensor_id', 2, 0, None, None), (21, 'next_update', 2, 0, None, None), (22, 'seq_number', 2, 0, None, None), (23, 'precision_bits', 2, 0, None, None), )
User._F = ((1, 'id', 14, 0, None, None), (2, 'long_name', 14, 0, None, None), (3, 'short_name', 14, 0, None, None), (4, 'macaddr', 15, 0, None, None), (5, 'hw_model', 7, 0, None, None), (6, 'is_licensed', 6, 0, None, None), (7, 'role', 7, 0, None, None), (8, 'public_key', 15, 0, None, None), (9, 'is_unmessagable', 6, 4, None, None), )
RouteDiscovery._F = ((1, 'route', 8, 3, None, None), (2, 'snr_towards', 0, 3, None, None), (3, 'route_back', 8, 3, None, None), (4, 'snr_back', 0, 3, None, None), )
Routing._F = ((1, 'route_request', 16, 4, RouteDiscovery, 'variant'), (2, 'route_reply', 16, 4, RouteDiscovery, 'variant'), (3, 'error_reason', 7, 4, None, 'variant'), (4, 'ack_proof', 15, 0, None, None), )
Data._F = ((1, 'portnum', 7, 0, None, None), (2, 'payload', 15, 0, None, None), (3, 'want_response', 6, 0, None, None), (4, 'dest', 8, 0, None, None), (5, 'source', 8, 0, None, None), (6, 'request_id', 8, 0, None, None), (7, 'reply_id', 8, 0, None, None), (8, 'emoji', 8, 0, None, None), (9, 'bitfield', 2, 4, None, None), (10, 'xeddsa_signature', 15, 0, None, None), )
KeyVerification._F = ((1, 'nonce', 3, 0, None, None), (2, 'hash1', 15, 0, None, None), (3, 'hash2', 15, 0, None, None), )
StoreForwardPlusPlus._F = ((1, 'sfpp_message_type', 7, 0, None, None), (2, 'message_hash', 15, 0, None, None), (3, 'commit_hash', 15, 0, None, None), (4, 'root_hash', 15, 0, None, None), (5, 'message', 15, 0, None, None), (6, 'encapsulated_id', 2, 0, None, None), (7, 'encapsulated_to', 2, 0, None, None), (8, 'encapsulated_from', 2, 0, None, None), (9, 'encapsulated_rxtime', 2, 0, None, None), (10, 'chain_count', 2, 0, None, None), )
RemoteShell._F = ((1, 'op', 7, 0, None, None), (2, 'session_id', 2, 0, None, None), (3, 'seq', 2, 0, None, None), (4, 'ack_seq', 2, 0, None, None), (5, 'payload', 15, 0, None, None), (6, 'cols', 2, 0, None, None), (7, 'rows', 2, 0, None, None), (8, 'flags', 2, 0, None, None), (9, 'last_tx_seq', 2, 0, None, None), (10, 'last_rx_seq', 2, 0, None, None), )
BoundingBox._F = ((1, 'longitude_west_i', 9, 0, None, None), (2, 'latitude_south_i', 9, 0, None, None), (3, 'longitude_east_i', 9, 0, None, None), (4, 'latitude_north_i', 9, 0, None, None), )
Waypoint._F = ((1, 'id', 2, 0, None, None), (2, 'latitude_i', 9, 4, None, None), (3, 'longitude_i', 9, 4, None, None), (4, 'expire', 2, 0, None, None), (5, 'locked_to', 2, 0, None, None), (6, 'name', 14, 0, None, None), (7, 'description', 14, 0, None, None), (8, 'icon', 8, 0, None, None), (9, 'geofence_radius', 2, 0, None, None), (10, 'bounding_box', 16, 4, BoundingBox, None), (11, 'notify_on_enter', 6, 0, None, None), (12, 'notify_on_exit', 6, 0, None, None), (13, 'notify_favorites_only', 6, 0, None, None), )
StatusMessage._F = ((1, 'status', 14, 0, None, None), )
MqttClientProxyMessage._F = ((1, 'topic', 14, 0, None, None), (2, 'data', 15, 4, None, 'payload_variant'), (3, 'text', 14, 4, None, 'payload_variant'), (4, 'retained', 6, 0, None, None), )
MeshPacket._F = ((1, 'from', 8, 0, None, None), (2, 'to', 8, 0, None, None), (3, 'channel', 2, 0, None, None), (4, 'decoded', 16, 4, Data, 'payload_variant'), (5, 'encrypted', 15, 4, None, 'payload_variant'), (6, 'id', 8, 0, None, None), (7, 'rx_time', 8, 4, None, None), (8, 'rx_snr', 10, 0, None, None), (9, 'hop_limit', 2, 0, None, None), (10, 'want_ack', 6, 0, None, None), (11, 'priority', 7, 0, None, None), (12, 'rx_rssi', 0, 4, None, None), (13, 'delayed', 7, 0, None, None), (14, 'via_mqtt', 6, 0, None, None), (15, 'hop_start', 2, 0, None, None), (16, 'public_key', 15, 0, None, None), (17, 'pki_encrypted', 6, 0, None, None), (18, 'next_hop', 2, 0, None, None), (19, 'relay_node', 2, 0, None, None), (20, 'tx_after', 2, 0, None, None), (21, 'transport_mechanism', 7, 0, None, None), (22, 'xeddsa_signed', 6, 0, None, None), (23, 'ack_proof_status', 7, 0, None, None), (24, 'slot_parity', 7, 0, None, None), )
NodeInfo._F = ((1, 'num', 2, 0, None, None), (2, 'user', 16, 4, User, None), (3, 'position', 16, 4, Position, None), (4, 'snr', 10, 0, None, None), (5, 'last_heard', 8, 0, None, None), (6, 'device_metrics', 16, 4, telemetry_pb2.DeviceMetrics, None), (7, 'channel', 2, 0, None, None), (8, 'via_mqtt', 6, 0, None, None), (9, 'hops_away', 2, 4, None, None), (10, 'is_favorite', 6, 0, None, None), (11, 'is_ignored', 6, 0, None, None), (12, 'is_key_manually_verified', 6, 0, None, None), (13, 'is_muted', 6, 0, None, None), (14, 'has_xeddsa_signed', 6, 0, None, None), (15, 'heard_on_current_lora', 6, 0, None, None), )
MyNodeInfo._F = ((1, 'my_node_num', 2, 0, None, None), (8, 'reboot_count', 2, 0, None, None), (11, 'min_app_version', 2, 0, None, None), (12, 'device_id', 15, 0, None, None), (13, 'pio_env', 14, 0, None, None), (14, 'firmware_edition', 7, 0, None, None), (15, 'nodedb_count', 2, 0, None, None), )
LogRecord._F = ((1, 'message', 14, 0, None, None), (2, 'time', 8, 0, None, None), (3, 'source', 14, 0, None, None), (4, 'level', 7, 0, None, None), )
QueueStatus._F = ((1, 'res', 0, 0, None, None), (2, 'free', 2, 0, None, None), (3, 'maxlen', 2, 0, None, None), (4, 'mesh_packet_id', 2, 0, None, None), )
FromRadio._F = ((1, 'id', 2, 0, None, None), (2, 'packet', 16, 4, MeshPacket, 'payload_variant'), (3, 'my_info', 16, 4, MyNodeInfo, 'payload_variant'), (4, 'node_info', 16, 4, NodeInfo, 'payload_variant'), (5, 'config', 16, 4, config_pb2.Config, 'payload_variant'), (6, 'log_record', 16, 4, LogRecord, 'payload_variant'), (7, 'config_complete_id', 2, 4, None, 'payload_variant'), (8, 'rebooted', 6, 4, None, 'payload_variant'), (9, 'moduleConfig', 16, 4, module_config_pb2.ModuleConfig, 'payload_variant'), (10, 'channel', 16, 4, channel_pb2.Channel, 'payload_variant'), (11, 'queueStatus', 16, 4, QueueStatus, 'payload_variant'), (12, 'xmodemPacket', 16, 4, xmodem_pb2.XModem, 'payload_variant'), (13, 'metadata', 16, 4, DeviceMetadata, 'payload_variant'), (14, 'mqttClientProxyMessage', 16, 4, MqttClientProxyMessage, 'payload_variant'), (15, 'fileInfo', 16, 4, FileInfo, 'payload_variant'), (16, 'clientNotification', 16, 4, ClientNotification, 'payload_variant'), (17, 'deviceuiConfig', 16, 4, device_ui_pb2.DeviceUIConfig, 'payload_variant'), (18, 'lockdown_status', 16, 4, LockdownStatus, 'payload_variant'), (19, 'region_presets', 16, 4, LoRaRegionPresetMap, 'payload_variant'), (21, 'display_frame', 16, 4, DisplayFrame, 'payload_variant'), (22, 'display_palette', 16, 4, DisplayPalette, 'payload_variant'), )
DisplayFrame._F = ((1, 'width', 2, 0, None, None), (2, 'height', 2, 0, None, None), (3, 'format', 7, 0, None, None), (4, 'frame_id', 2, 0, None, None), (5, 'offset', 2, 0, None, None), (6, 'total_size', 2, 0, None, None), (7, 'data', 15, 0, None, None), (8, 'rect_x', 2, 0, None, None), (9, 'rect_y', 2, 0, None, None), (10, 'rect_width', 2, 0, None, None), (11, 'rect_height', 2, 0, None, None), (12, 'palette_signature', 2, 0, None, None), )
DisplayPalette.ColorRegion._F = ((1, 'x', 2, 0, None, None), (2, 'y', 2, 0, None, None), (3, 'width', 2, 0, None, None), (4, 'height', 2, 0, None, None), (5, 'on_color', 2, 0, None, None), (6, 'off_color', 2, 0, None, None), )
DisplayPalette._F = ((1, 'signature', 2, 0, None, None), (2, 'default_on_color', 2, 0, None, None), (3, 'default_off_color', 2, 0, None, None), (4, 'region_offset', 2, 0, None, None), (5, 'region_total', 2, 0, None, None), (6, 'regions', 16, 1, DisplayPalette.ColorRegion, None), )
LockdownStatus._F = ((1, 'state', 7, 0, None, None), (2, 'lock_reason', 14, 0, None, None), (3, 'boots_remaining', 2, 0, None, None), (4, 'valid_until_epoch', 2, 0, None, None), (5, 'backoff_seconds', 2, 0, None, None), )
ClientNotification._F = ((1, 'reply_id', 2, 4, None, None), (2, 'time', 8, 0, None, None), (3, 'level', 7, 0, None, None), (4, 'message', 14, 0, None, None), (5, 'type', 7, 0, None, None), (11, 'key_verification_number_inform', 16, 4, KeyVerificationNumberInform, 'payload_variant'), (12, 'key_verification_number_request', 16, 4, KeyVerificationNumberRequest, 'payload_variant'), (13, 'key_verification_final', 16, 4, KeyVerificationFinal, 'payload_variant'), (14, 'duplicated_public_key', 16, 4, DuplicatedPublicKey, 'payload_variant'), (15, 'low_entropy_key', 16, 4, LowEntropyKey, 'payload_variant'), )
KeyVerificationNumberInform._F = ((1, 'nonce', 3, 0, None, None), (2, 'remote_longname', 14, 0, None, None), (3, 'security_number', 2, 0, None, None), )
KeyVerificationNumberRequest._F = ((1, 'nonce', 3, 0, None, None), (2, 'remote_longname', 14, 0, None, None), )
KeyVerificationFinal._F = ((1, 'nonce', 3, 0, None, None), (2, 'remote_longname', 14, 0, None, None), (3, 'isSender', 6, 0, None, None), (4, 'verification_characters', 14, 0, None, None), )
DuplicatedPublicKey._F = ()
LowEntropyKey._F = ()
FileInfo._F = ((1, 'file_name', 14, 0, None, None), (2, 'size_bytes', 2, 0, None, None), )
ToRadio._F = ((1, 'packet', 16, 4, MeshPacket, 'payload_variant'), (3, 'want_config_id', 2, 4, None, 'payload_variant'), (4, 'disconnect', 6, 4, None, 'payload_variant'), (5, 'xmodemPacket', 16, 4, xmodem_pb2.XModem, 'payload_variant'), (6, 'mqttClientProxyMessage', 16, 4, MqttClientProxyMessage, 'payload_variant'), (7, 'heartbeat', 16, 4, Heartbeat, 'payload_variant'), )
Compressed._F = ((1, 'portnum', 7, 0, None, None), (2, 'data', 15, 0, None, None), )
NeighborInfo._F = ((1, 'node_id', 2, 0, None, None), (2, 'last_sent_by_id', 2, 0, None, None), (3, 'node_broadcast_interval_secs', 2, 0, None, None), (4, 'neighbors', 16, 1, Neighbor, None), )
Neighbor._F = ((1, 'node_id', 2, 0, None, None), (2, 'snr', 10, 0, None, None), (3, 'last_rx_time', 8, 0, None, None), (4, 'node_broadcast_interval_secs', 2, 0, None, None), )
DeviceMetadata._F = ((1, 'firmware_version', 14, 0, None, None), (2, 'device_state_version', 2, 0, None, None), (3, 'canShutdown', 6, 0, None, None), (4, 'hasWifi', 6, 0, None, None), (5, 'hasBluetooth', 6, 0, None, None), (6, 'hasEthernet', 6, 0, None, None), (7, 'role', 7, 0, None, None), (8, 'position_flags', 2, 0, None, None), (9, 'hw_model', 7, 0, None, None), (10, 'hasRemoteHardware', 6, 0, None, None), (11, 'hasPKC', 6, 0, None, None), (12, 'excluded_modules', 2, 0, None, None), (14, 'has_xeddsa', 6, 0, None, None), (16, 'display', 16, 4, DisplayInfo, None), (17, 'ble_address', 14, 0, None, None), (19, 'bootloader_version', 2, 0, None, None), )
DisplayInfo._F = ((1, 'width', 2, 0, None, None), (2, 'height', 2, 0, None, None), (3, 'format', 7, 0, None, None), (4, 'panel_class', 7, 0, None, None), (5, 'has_touch', 6, 0, None, None), )
LoRaPresetGroup._F = ((1, 'presets', 7, 3, None, None), (2, 'default_preset', 7, 0, None, None), (3, 'licensed_only', 6, 0, None, None), )
LoRaRegionPresets._F = ((1, 'region', 7, 0, None, None), (2, 'group_index', 2, 0, None, None), )
LoRaRegionPresetMap._F = ((1, 'groups', 16, 1, LoRaPresetGroup, None), (2, 'region_groups', 16, 1, LoRaRegionPresets, None), )
Heartbeat._F = ((1, 'nonce', 2, 0, None, None), )
NodeRemoteHardwarePin._F = ((1, 'node_num', 2, 0, None, None), (2, 'pin', 16, 4, module_config_pb2.RemoteHardwarePin, None), )
ChunkedPayload._F = ((1, 'payload_id', 2, 0, None, None), (2, 'chunk_count', 2, 0, None, None), (3, 'chunk_index', 2, 0, None, None), (4, 'payload_chunk', 15, 0, None, None), )
resend_chunks._F = ((1, 'chunks', 2, 3, None, None), )
ChunkedPayloadResponse._F = ((1, 'payload_id', 2, 0, None, None), (2, 'request_transfer', 6, 4, None, 'payload_variant'), (3, 'accept_transfer', 6, 4, None, 'payload_variant'), (4, 'resend_chunks', 16, 4, resend_chunks, 'payload_variant'), )
