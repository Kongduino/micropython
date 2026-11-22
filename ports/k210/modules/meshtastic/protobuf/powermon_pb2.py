# Generated from meshtastic/powermon.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class PowerMon(Message):
    class State(Enum):
        _V = (('None', 0), ('CPU_DeepSleep', 1), ('CPU_LightSleep', 2), ('Vext1_On', 4), ('Lora_RXOn', 8), ('Lora_TXOn', 16), ('Lora_RXActive', 32), ('BT_On', 64), ('LED_On', 128), ('Screen_On', 256), ('Screen_Drawing', 512), ('Wifi_On', 1024), ('GPS_Active', 2048), )
        CPU_DeepSleep = 1
        CPU_LightSleep = 2
        Vext1_On = 4
        Lora_RXOn = 8
        Lora_TXOn = 16
        Lora_RXActive = 32
        BT_On = 64
        LED_On = 128
        Screen_On = 256
        Screen_Drawing = 512
        Wifi_On = 1024
        GPS_Active = 2048
    CPU_DeepSleep = 1
    CPU_LightSleep = 2
    Vext1_On = 4
    Lora_RXOn = 8
    Lora_TXOn = 16
    Lora_RXActive = 32
    BT_On = 64
    LED_On = 128
    Screen_On = 256
    Screen_Drawing = 512
    Wifi_On = 1024
    GPS_Active = 2048

class PowerStressMessage(Message):
    class Opcode(Enum):
        _V = (('UNSET', 0), ('PRINT_INFO', 1), ('FORCE_QUIET', 2), ('END_QUIET', 3), ('SCREEN_ON', 16), ('SCREEN_OFF', 17), ('CPU_IDLE', 32), ('CPU_DEEPSLEEP', 33), ('CPU_FULLON', 34), ('LED_ON', 48), ('LED_OFF', 49), ('LORA_OFF', 64), ('LORA_TX', 65), ('LORA_RX', 66), ('BT_OFF', 80), ('BT_ON', 81), ('WIFI_OFF', 96), ('WIFI_ON', 97), ('GPS_OFF', 112), ('GPS_ON', 113), )
        UNSET = 0
        PRINT_INFO = 1
        FORCE_QUIET = 2
        END_QUIET = 3
        SCREEN_ON = 16
        SCREEN_OFF = 17
        CPU_IDLE = 32
        CPU_DEEPSLEEP = 33
        CPU_FULLON = 34
        LED_ON = 48
        LED_OFF = 49
        LORA_OFF = 64
        LORA_TX = 65
        LORA_RX = 66
        BT_OFF = 80
        BT_ON = 81
        WIFI_OFF = 96
        WIFI_ON = 97
        GPS_OFF = 112
        GPS_ON = 113
    UNSET = 0
    PRINT_INFO = 1
    FORCE_QUIET = 2
    END_QUIET = 3
    SCREEN_ON = 16
    SCREEN_OFF = 17
    CPU_IDLE = 32
    CPU_DEEPSLEEP = 33
    CPU_FULLON = 34
    LED_ON = 48
    LED_OFF = 49
    LORA_OFF = 64
    LORA_TX = 65
    LORA_RX = 66
    BT_OFF = 80
    BT_ON = 81
    WIFI_OFF = 96
    WIFI_ON = 97
    GPS_OFF = 112
    GPS_ON = 113

setattr(PowerMon.State, 'None', 0)
setattr(PowerMon, 'None', 0)
PowerMon._F = ()
PowerStressMessage._F = ((1, 'cmd', 7, 0, None, None), (2, 'num_seconds', 10, 0, None, None), )
