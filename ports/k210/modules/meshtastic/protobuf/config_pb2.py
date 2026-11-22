# Generated from meshtastic/config.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import device_ui_pb2
from meshtastic.protobuf import field_metadata_pb2

class Config(Message):
    class DeviceConfig(Message):
        class Role(Enum):
            _V = (('CLIENT', 0), ('CLIENT_MUTE', 1), ('ROUTER', 2), ('ROUTER_CLIENT', 3), ('REPEATER', 4), ('TRACKER', 5), ('SENSOR', 6), ('TAK', 7), ('CLIENT_HIDDEN', 8), ('LOST_AND_FOUND', 9), ('TAK_TRACKER', 10), ('ROUTER_LATE', 11), ('CLIENT_BASE', 12), )
            CLIENT = 0
            CLIENT_MUTE = 1
            ROUTER = 2
            ROUTER_CLIENT = 3
            REPEATER = 4
            TRACKER = 5
            SENSOR = 6
            TAK = 7
            CLIENT_HIDDEN = 8
            LOST_AND_FOUND = 9
            TAK_TRACKER = 10
            ROUTER_LATE = 11
            CLIENT_BASE = 12
        CLIENT = 0
        CLIENT_MUTE = 1
        ROUTER = 2
        ROUTER_CLIENT = 3
        REPEATER = 4
        TRACKER = 5
        SENSOR = 6
        TAK = 7
        CLIENT_HIDDEN = 8
        LOST_AND_FOUND = 9
        TAK_TRACKER = 10
        ROUTER_LATE = 11
        CLIENT_BASE = 12
        class RebroadcastMode(Enum):
            _V = (('ALL', 0), ('ALL_SKIP_DECODING', 1), ('LOCAL_ONLY', 2), ('KNOWN_ONLY', 3), ('NONE', 4), ('CORE_PORTNUMS_ONLY', 5), )
            ALL = 0
            ALL_SKIP_DECODING = 1
            LOCAL_ONLY = 2
            KNOWN_ONLY = 3
            NONE = 4
            CORE_PORTNUMS_ONLY = 5
        ALL = 0
        ALL_SKIP_DECODING = 1
        LOCAL_ONLY = 2
        KNOWN_ONLY = 3
        NONE = 4
        CORE_PORTNUMS_ONLY = 5
        class BuzzerMode(Enum):
            _V = (('ALL_ENABLED', 0), ('DISABLED', 1), ('NOTIFICATIONS_ONLY', 2), ('SYSTEM_ONLY', 3), ('DIRECT_MSG_ONLY', 4), )
            ALL_ENABLED = 0
            DISABLED = 1
            NOTIFICATIONS_ONLY = 2
            SYSTEM_ONLY = 3
            DIRECT_MSG_ONLY = 4
        ALL_ENABLED = 0
        DISABLED = 1
        NOTIFICATIONS_ONLY = 2
        SYSTEM_ONLY = 3
        DIRECT_MSG_ONLY = 4
    class PositionConfig(Message):
        class PositionFlags(Enum):
            _V = (('UNSET', 0), ('ALTITUDE', 1), ('ALTITUDE_MSL', 2), ('GEOIDAL_SEPARATION', 4), ('DOP', 8), ('HVDOP', 16), ('SATINVIEW', 32), ('SEQ_NO', 64), ('TIMESTAMP', 128), ('HEADING', 256), ('SPEED', 512), )
            UNSET = 0
            ALTITUDE = 1
            ALTITUDE_MSL = 2
            GEOIDAL_SEPARATION = 4
            DOP = 8
            HVDOP = 16
            SATINVIEW = 32
            SEQ_NO = 64
            TIMESTAMP = 128
            HEADING = 256
            SPEED = 512
        UNSET = 0
        ALTITUDE = 1
        ALTITUDE_MSL = 2
        GEOIDAL_SEPARATION = 4
        DOP = 8
        HVDOP = 16
        SATINVIEW = 32
        SEQ_NO = 64
        TIMESTAMP = 128
        HEADING = 256
        SPEED = 512
        class GpsMode(Enum):
            _V = (('DISABLED', 0), ('ENABLED', 1), ('NOT_PRESENT', 2), )
            DISABLED = 0
            ENABLED = 1
            NOT_PRESENT = 2
        DISABLED = 0
        ENABLED = 1
        NOT_PRESENT = 2
    class PowerConfig(Message):
        pass
    class NetworkConfig(Message):
        class AddressMode(Enum):
            _V = (('DHCP', 0), ('STATIC', 1), )
            DHCP = 0
            STATIC = 1
        DHCP = 0
        STATIC = 1
        class ProtocolFlags(Enum):
            _V = (('NO_BROADCAST', 0), ('UDP_BROADCAST', 1), )
            NO_BROADCAST = 0
            UDP_BROADCAST = 1
        NO_BROADCAST = 0
        UDP_BROADCAST = 1
        class IpV4Config(Message):
            pass
    class DisplayConfig(Message):
        class DeprecatedGpsCoordinateFormat(Enum):
            _V = (('UNUSED', 0), )
            UNUSED = 0
        UNUSED = 0
        class DisplayUnits(Enum):
            _V = (('METRIC', 0), ('IMPERIAL', 1), )
            METRIC = 0
            IMPERIAL = 1
        METRIC = 0
        IMPERIAL = 1
        class OledType(Enum):
            _V = (('OLED_AUTO', 0), ('OLED_SSD1306', 1), ('OLED_SH1106', 2), ('OLED_SH1107', 3), ('OLED_SH1107_128_128', 4), ('OLED_SH1107_ROTATED', 5), )
            OLED_AUTO = 0
            OLED_SSD1306 = 1
            OLED_SH1106 = 2
            OLED_SH1107 = 3
            OLED_SH1107_128_128 = 4
            OLED_SH1107_ROTATED = 5
        OLED_AUTO = 0
        OLED_SSD1306 = 1
        OLED_SH1106 = 2
        OLED_SH1107 = 3
        OLED_SH1107_128_128 = 4
        OLED_SH1107_ROTATED = 5
        class DisplayMode(Enum):
            _V = (('DEFAULT', 0), ('TWOCOLOR', 1), ('INVERTED', 2), ('COLOR', 3), )
            DEFAULT = 0
            TWOCOLOR = 1
            INVERTED = 2
            COLOR = 3
        DEFAULT = 0
        TWOCOLOR = 1
        INVERTED = 2
        COLOR = 3
        class CompassOrientation(Enum):
            _V = (('DEGREES_0', 0), ('DEGREES_90', 1), ('DEGREES_180', 2), ('DEGREES_270', 3), ('DEGREES_0_INVERTED', 4), ('DEGREES_90_INVERTED', 5), ('DEGREES_180_INVERTED', 6), ('DEGREES_270_INVERTED', 7), )
            DEGREES_0 = 0
            DEGREES_90 = 1
            DEGREES_180 = 2
            DEGREES_270 = 3
            DEGREES_0_INVERTED = 4
            DEGREES_90_INVERTED = 5
            DEGREES_180_INVERTED = 6
            DEGREES_270_INVERTED = 7
        DEGREES_0 = 0
        DEGREES_90 = 1
        DEGREES_180 = 2
        DEGREES_270 = 3
        DEGREES_0_INVERTED = 4
        DEGREES_90_INVERTED = 5
        DEGREES_180_INVERTED = 6
        DEGREES_270_INVERTED = 7
    class LoRaConfig(Message):
        class RegionCode(Enum):
            _V = (('UNSET', 0), ('US', 1), ('EU_433', 2), ('EU_868', 3), ('CN', 4), ('JP', 5), ('ANZ', 6), ('KR', 7), ('TW', 8), ('RU', 9), ('IN', 10), ('NZ_865', 11), ('TH', 12), ('LORA_24', 13), ('UA_433', 14), ('UA_868', 15), ('MY_433', 16), ('MY_919', 17), ('SG_923', 18), ('PH_433', 19), ('PH_868', 20), ('PH_915', 21), ('ANZ_433', 22), ('KZ_433', 23), ('KZ_863', 24), ('NP_865', 25), ('BR_902', 26), ('ITU1_2M', 27), ('ITU2_2M', 28), ('EU_866', 29), ('EU_874', 30), ('EU_917', 31), ('EU_N_868', 32), ('ITU3_2M', 33), ('ITU1_70CM', 34), ('ITU2_70CM', 35), ('ITU3_70CM', 36), ('ITU2_125CM', 37), )
            UNSET = 0
            US = 1
            EU_433 = 2
            EU_868 = 3
            CN = 4
            JP = 5
            ANZ = 6
            KR = 7
            TW = 8
            RU = 9
            IN = 10
            NZ_865 = 11
            TH = 12
            LORA_24 = 13
            UA_433 = 14
            UA_868 = 15
            MY_433 = 16
            MY_919 = 17
            SG_923 = 18
            PH_433 = 19
            PH_868 = 20
            PH_915 = 21
            ANZ_433 = 22
            KZ_433 = 23
            KZ_863 = 24
            NP_865 = 25
            BR_902 = 26
            ITU1_2M = 27
            ITU2_2M = 28
            EU_866 = 29
            EU_874 = 30
            EU_917 = 31
            EU_N_868 = 32
            ITU3_2M = 33
            ITU1_70CM = 34
            ITU2_70CM = 35
            ITU3_70CM = 36
            ITU2_125CM = 37
        UNSET = 0
        US = 1
        EU_433 = 2
        EU_868 = 3
        CN = 4
        JP = 5
        ANZ = 6
        KR = 7
        TW = 8
        RU = 9
        IN = 10
        NZ_865 = 11
        TH = 12
        LORA_24 = 13
        UA_433 = 14
        UA_868 = 15
        MY_433 = 16
        MY_919 = 17
        SG_923 = 18
        PH_433 = 19
        PH_868 = 20
        PH_915 = 21
        ANZ_433 = 22
        KZ_433 = 23
        KZ_863 = 24
        NP_865 = 25
        BR_902 = 26
        ITU1_2M = 27
        ITU2_2M = 28
        EU_866 = 29
        EU_874 = 30
        EU_917 = 31
        EU_N_868 = 32
        ITU3_2M = 33
        ITU1_70CM = 34
        ITU2_70CM = 35
        ITU3_70CM = 36
        ITU2_125CM = 37
        class ModemPreset(Enum):
            _V = (('LONG_FAST', 0), ('LONG_SLOW', 1), ('VERY_LONG_SLOW', 2), ('MEDIUM_SLOW', 3), ('MEDIUM_FAST', 4), ('SHORT_SLOW', 5), ('SHORT_FAST', 6), ('LONG_MODERATE', 7), ('SHORT_TURBO', 8), ('LONG_TURBO', 9), ('LITE_FAST', 10), ('LITE_SLOW', 11), ('NARROW_FAST', 12), ('NARROW_SLOW', 13), ('TINY_FAST', 14), ('TINY_SLOW', 15), ('MEDIUM_TURBO', 16), )
            LONG_FAST = 0
            LONG_SLOW = 1
            VERY_LONG_SLOW = 2
            MEDIUM_SLOW = 3
            MEDIUM_FAST = 4
            SHORT_SLOW = 5
            SHORT_FAST = 6
            LONG_MODERATE = 7
            SHORT_TURBO = 8
            LONG_TURBO = 9
            LITE_FAST = 10
            LITE_SLOW = 11
            NARROW_FAST = 12
            NARROW_SLOW = 13
            TINY_FAST = 14
            TINY_SLOW = 15
            MEDIUM_TURBO = 16
        LONG_FAST = 0
        LONG_SLOW = 1
        VERY_LONG_SLOW = 2
        MEDIUM_SLOW = 3
        MEDIUM_FAST = 4
        SHORT_SLOW = 5
        SHORT_FAST = 6
        LONG_MODERATE = 7
        SHORT_TURBO = 8
        LONG_TURBO = 9
        LITE_FAST = 10
        LITE_SLOW = 11
        NARROW_FAST = 12
        NARROW_SLOW = 13
        TINY_FAST = 14
        TINY_SLOW = 15
        MEDIUM_TURBO = 16
        class FEM_LNA_Mode(Enum):
            _V = (('DISABLED', 0), ('ENABLED', 1), ('NOT_PRESENT', 2), )
            DISABLED = 0
            ENABLED = 1
            NOT_PRESENT = 2
        DISABLED = 0
        ENABLED = 1
        NOT_PRESENT = 2
    class BluetoothConfig(Message):
        class PairingMode(Enum):
            _V = (('RANDOM_PIN', 0), ('FIXED_PIN', 1), ('NO_PIN', 2), )
            RANDOM_PIN = 0
            FIXED_PIN = 1
            NO_PIN = 2
        RANDOM_PIN = 0
        FIXED_PIN = 1
        NO_PIN = 2
    class SecurityConfig(Message):
        class PacketSignaturePolicy(Enum):
            _V = (('PACKET_SIGNATURE_POLICY_COMPATIBLE', 0), ('PACKET_SIGNATURE_POLICY_BALANCED', 1), ('PACKET_SIGNATURE_POLICY_STRICT', 2), )
            PACKET_SIGNATURE_POLICY_COMPATIBLE = 0
            PACKET_SIGNATURE_POLICY_BALANCED = 1
            PACKET_SIGNATURE_POLICY_STRICT = 2
        PACKET_SIGNATURE_POLICY_COMPATIBLE = 0
        PACKET_SIGNATURE_POLICY_BALANCED = 1
        PACKET_SIGNATURE_POLICY_STRICT = 2
    class SessionkeyConfig(Message):
        pass

Config.DeviceConfig._F = ((1, 'role', 7, 0, None, None), (2, 'serial_enabled', 6, 0, None, None), (4, 'button_gpio', 2, 0, None, None), (5, 'buzzer_gpio', 2, 0, None, None), (6, 'rebroadcast_mode', 7, 0, None, None), (7, 'node_info_broadcast_secs', 2, 0, None, None), (8, 'double_tap_as_button_press', 6, 0, None, None), (9, 'is_managed', 6, 0, None, None), (10, 'disable_triple_click', 6, 0, None, None), (11, 'tzdef', 14, 0, None, None), (12, 'led_heartbeat_disabled', 6, 0, None, None), (13, 'buzzer_mode', 7, 0, None, None), )
Config.PositionConfig._F = ((1, 'position_broadcast_secs', 2, 0, None, None), (2, 'position_broadcast_smart_enabled', 6, 0, None, None), (3, 'fixed_position', 6, 0, None, None), (4, 'gps_enabled', 6, 0, None, None), (5, 'gps_update_interval', 2, 0, None, None), (6, 'gps_attempt_time', 2, 0, None, None), (7, 'position_flags', 2, 0, None, None), (8, 'rx_gpio', 2, 0, None, None), (9, 'tx_gpio', 2, 0, None, None), (10, 'broadcast_smart_minimum_distance', 2, 0, None, None), (11, 'broadcast_smart_minimum_interval_secs', 2, 0, None, None), (12, 'gps_en_gpio', 2, 0, None, None), (13, 'gps_mode', 7, 0, None, None), )
Config.PowerConfig._F = ((1, 'is_power_saving', 6, 0, None, None), (2, 'on_battery_shutdown_after_secs', 2, 0, None, None), (3, 'adc_multiplier_override', 10, 0, None, None), (4, 'wait_bluetooth_secs', 2, 0, None, None), (6, 'sds_secs', 2, 0, None, None), (7, 'ls_secs', 2, 0, None, None), (8, 'min_wake_secs', 2, 0, None, None), (9, 'device_battery_ina_address', 2, 0, None, None), (32, 'powermon_enables', 3, 0, None, None), )
Config.NetworkConfig.IpV4Config._F = ((1, 'ip', 8, 0, None, None), (2, 'gateway', 8, 0, None, None), (3, 'subnet', 8, 0, None, None), (4, 'dns', 8, 0, None, None), )
Config.NetworkConfig._F = ((1, 'wifi_enabled', 6, 0, None, None), (3, 'wifi_ssid', 14, 0, None, None), (4, 'wifi_psk', 14, 0, None, None), (5, 'ntp_server', 14, 0, None, None), (6, 'eth_enabled', 6, 0, None, None), (7, 'address_mode', 7, 0, None, None), (8, 'ipv4_config', 16, 4, Config.NetworkConfig.IpV4Config, None), (9, 'rsyslog_server', 14, 0, None, None), (10, 'enabled_protocols', 2, 0, None, None), (11, 'ipv6_enabled', 6, 0, None, None), )
Config.DisplayConfig._F = ((1, 'screen_on_secs', 2, 0, None, None), (2, 'gps_format', 7, 0, None, None), (3, 'auto_screen_carousel_secs', 2, 0, None, None), (4, 'compass_north_top', 6, 0, None, None), (5, 'flip_screen', 6, 0, None, None), (6, 'units', 7, 0, None, None), (7, 'oled', 7, 0, None, None), (8, 'displaymode', 7, 0, None, None), (9, 'heading_bold', 6, 0, None, None), (10, 'wake_on_tap_or_motion', 6, 0, None, None), (11, 'compass_orientation', 7, 0, None, None), (12, 'use_12h_clock', 6, 0, None, None), (13, 'use_long_node_name', 6, 0, None, None), (14, 'enable_message_bubbles', 6, 0, None, None), )
Config.LoRaConfig._F = ((1, 'use_preset', 6, 0, None, None), (2, 'modem_preset', 7, 0, None, None), (3, 'bandwidth', 2, 0, None, None), (4, 'spread_factor', 2, 0, None, None), (5, 'coding_rate', 2, 0, None, None), (6, 'frequency_offset', 10, 0, None, None), (7, 'region', 7, 0, None, None), (8, 'hop_limit', 2, 0, None, None), (9, 'tx_enabled', 6, 0, None, None), (10, 'tx_power', 0, 0, None, None), (11, 'channel_num', 2, 0, None, None), (12, 'override_duty_cycle', 6, 0, None, None), (13, 'sx126x_rx_boosted_gain', 6, 0, None, None), (14, 'override_frequency', 10, 0, None, None), (15, 'pa_fan_disabled', 6, 0, None, None), (103, 'ignore_incoming', 2, 3, None, None), (104, 'ignore_mqtt', 6, 0, None, None), (105, 'config_ok_to_mqtt', 6, 0, None, None), (106, 'fem_lna_mode', 7, 0, None, None), (107, 'serial_hal_only', 6, 0, None, None), (108, 'transparent_mode', 6, 0, None, None), )
Config.BluetoothConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'mode', 7, 0, None, None), (3, 'fixed_pin', 2, 0, None, None), )
Config.SecurityConfig._F = ((1, 'public_key', 15, 0, None, None), (2, 'private_key', 15, 0, None, None), (3, 'admin_key', 15, 1, None, None), (4, 'is_managed', 6, 0, None, None), (5, 'serial_enabled', 6, 0, None, None), (6, 'debug_log_api_enabled', 6, 0, None, None), (8, 'admin_channel_enabled', 6, 0, None, None), (9, 'packet_signature_policy', 7, 0, None, None), )
Config.SessionkeyConfig._F = ()
Config._F = ((1, 'device', 16, 4, Config.DeviceConfig, 'payload_variant'), (2, 'position', 16, 4, Config.PositionConfig, 'payload_variant'), (3, 'power', 16, 4, Config.PowerConfig, 'payload_variant'), (4, 'network', 16, 4, Config.NetworkConfig, 'payload_variant'), (5, 'display', 16, 4, Config.DisplayConfig, 'payload_variant'), (6, 'lora', 16, 4, Config.LoRaConfig, 'payload_variant'), (7, 'bluetooth', 16, 4, Config.BluetoothConfig, 'payload_variant'), (8, 'security', 16, 4, Config.SecurityConfig, 'payload_variant'), (9, 'sessionkey', 16, 4, Config.SessionkeyConfig, 'payload_variant'), (10, 'device_ui', 16, 4, device_ui_pb2.DeviceUIConfig, 'payload_variant'), )
