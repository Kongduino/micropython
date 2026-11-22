# Generated from meshtastic/module_config.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import atak_pb2
from meshtastic.protobuf import channel_pb2
from meshtastic.protobuf import config_pb2
from meshtastic.protobuf import field_metadata_pb2

class RemoteHardwarePinType(Enum):
    _V = (('UNKNOWN', 0), ('DIGITAL_READ', 1), ('DIGITAL_WRITE', 2), )
    UNKNOWN = 0
    DIGITAL_READ = 1
    DIGITAL_WRITE = 2

class ModuleConfig(Message):
    class MQTTConfig(Message):
        pass
    class MapReportSettings(Message):
        pass
    class RemoteHardwareConfig(Message):
        pass
    class NeighborInfoConfig(Message):
        pass
    class DetectionSensorConfig(Message):
        class TriggerType(Enum):
            _V = (('LOGIC_LOW', 0), ('LOGIC_HIGH', 1), ('FALLING_EDGE', 2), ('RISING_EDGE', 3), ('EITHER_EDGE_ACTIVE_LOW', 4), ('EITHER_EDGE_ACTIVE_HIGH', 5), )
            LOGIC_LOW = 0
            LOGIC_HIGH = 1
            FALLING_EDGE = 2
            RISING_EDGE = 3
            EITHER_EDGE_ACTIVE_LOW = 4
            EITHER_EDGE_ACTIVE_HIGH = 5
        LOGIC_LOW = 0
        LOGIC_HIGH = 1
        FALLING_EDGE = 2
        RISING_EDGE = 3
        EITHER_EDGE_ACTIVE_LOW = 4
        EITHER_EDGE_ACTIVE_HIGH = 5
    class AudioConfig(Message):
        class Audio_Baud(Enum):
            _V = (('CODEC2_DEFAULT', 0), ('CODEC2_3200', 1), ('CODEC2_2400', 2), ('CODEC2_1600', 3), ('CODEC2_1400', 4), ('CODEC2_1300', 5), ('CODEC2_1200', 6), ('CODEC2_700', 7), ('CODEC2_700B', 8), ('CODEC2_700C', 9), ('CODEC2_450', 10), )
            CODEC2_DEFAULT = 0
            CODEC2_3200 = 1
            CODEC2_2400 = 2
            CODEC2_1600 = 3
            CODEC2_1400 = 4
            CODEC2_1300 = 5
            CODEC2_1200 = 6
            CODEC2_700 = 7
            CODEC2_700B = 8
            CODEC2_700C = 9
            CODEC2_450 = 10
        CODEC2_DEFAULT = 0
        CODEC2_3200 = 1
        CODEC2_2400 = 2
        CODEC2_1600 = 3
        CODEC2_1400 = 4
        CODEC2_1300 = 5
        CODEC2_1200 = 6
        CODEC2_700 = 7
        CODEC2_700B = 8
        CODEC2_700C = 9
        CODEC2_450 = 10
    class PaxcounterConfig(Message):
        pass
    class TrafficManagementConfig(Message):
        pass
    class SerialConfig(Message):
        class Serial_Baud(Enum):
            _V = (('BAUD_DEFAULT', 0), ('BAUD_110', 1), ('BAUD_300', 2), ('BAUD_600', 3), ('BAUD_1200', 4), ('BAUD_2400', 5), ('BAUD_4800', 6), ('BAUD_9600', 7), ('BAUD_19200', 8), ('BAUD_38400', 9), ('BAUD_57600', 10), ('BAUD_115200', 11), ('BAUD_230400', 12), ('BAUD_460800', 13), ('BAUD_576000', 14), ('BAUD_921600', 15), )
            BAUD_DEFAULT = 0
            BAUD_110 = 1
            BAUD_300 = 2
            BAUD_600 = 3
            BAUD_1200 = 4
            BAUD_2400 = 5
            BAUD_4800 = 6
            BAUD_9600 = 7
            BAUD_19200 = 8
            BAUD_38400 = 9
            BAUD_57600 = 10
            BAUD_115200 = 11
            BAUD_230400 = 12
            BAUD_460800 = 13
            BAUD_576000 = 14
            BAUD_921600 = 15
        BAUD_DEFAULT = 0
        BAUD_110 = 1
        BAUD_300 = 2
        BAUD_600 = 3
        BAUD_1200 = 4
        BAUD_2400 = 5
        BAUD_4800 = 6
        BAUD_9600 = 7
        BAUD_19200 = 8
        BAUD_38400 = 9
        BAUD_57600 = 10
        BAUD_115200 = 11
        BAUD_230400 = 12
        BAUD_460800 = 13
        BAUD_576000 = 14
        BAUD_921600 = 15
        class Serial_Mode(Enum):
            _V = (('DEFAULT', 0), ('SIMPLE', 1), ('PROTO', 2), ('TEXTMSG', 3), ('NMEA', 4), ('CALTOPO', 5), ('WS85', 6), ('VE_DIRECT', 7), ('MS_CONFIG', 8), ('LOG', 9), ('LOGTEXT', 10), ('MODBUS', 11), )
            DEFAULT = 0
            SIMPLE = 1
            PROTO = 2
            TEXTMSG = 3
            NMEA = 4
            CALTOPO = 5
            WS85 = 6
            VE_DIRECT = 7
            MS_CONFIG = 8
            LOG = 9
            LOGTEXT = 10
            MODBUS = 11
        DEFAULT = 0
        SIMPLE = 1
        PROTO = 2
        TEXTMSG = 3
        NMEA = 4
        CALTOPO = 5
        WS85 = 6
        VE_DIRECT = 7
        MS_CONFIG = 8
        LOG = 9
        LOGTEXT = 10
        MODBUS = 11
    class ExternalNotificationConfig(Message):
        pass
    class StoreForwardConfig(Message):
        pass
    class RangeTestConfig(Message):
        pass
    class TelemetryConfig(Message):
        pass
    class CannedMessageConfig(Message):
        class InputEventChar(Enum):
            _V = (('NONE', 0), ('UP', 17), ('DOWN', 18), ('LEFT', 19), ('RIGHT', 20), ('SELECT', 10), ('BACK', 27), ('CANCEL', 24), )
            NONE = 0
            UP = 17
            DOWN = 18
            LEFT = 19
            RIGHT = 20
            SELECT = 10
            BACK = 27
            CANCEL = 24
        NONE = 0
        UP = 17
        DOWN = 18
        LEFT = 19
        RIGHT = 20
        SELECT = 10
        BACK = 27
        CANCEL = 24
    class AmbientLightingConfig(Message):
        pass
    class StatusMessageConfig(Message):
        pass
    class MeshBeaconConfig(Message):
        class Flags(Enum):
            _V = (('FLAG_NONE', 0), ('FLAG_LISTEN_ENABLED', 1), ('FLAG_BROADCAST_ENABLED', 2), ('FLAG_LEGACY_SPLIT', 4), )
            FLAG_NONE = 0
            FLAG_LISTEN_ENABLED = 1
            FLAG_BROADCAST_ENABLED = 2
            FLAG_LEGACY_SPLIT = 4
        FLAG_NONE = 0
        FLAG_LISTEN_ENABLED = 1
        FLAG_BROADCAST_ENABLED = 2
        FLAG_LEGACY_SPLIT = 4
        class BroadcastTarget(Message):
            pass
    class TAKConfig(Message):
        pass

class RemoteHardwarePin(Message):
    pass

UNKNOWN = 0
DIGITAL_READ = 1
DIGITAL_WRITE = 2
ModuleConfig.MQTTConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'address', 14, 0, None, None), (3, 'username', 14, 0, None, None), (4, 'password', 14, 0, None, None), (5, 'encryption_enabled', 6, 0, None, None), (6, 'json_enabled', 6, 0, None, None), (7, 'tls_enabled', 6, 0, None, None), (8, 'root', 14, 0, None, None), (9, 'proxy_to_client_enabled', 6, 0, None, None), (10, 'map_reporting_enabled', 6, 0, None, None), (11, 'map_report_settings', 16, 4, ModuleConfig.MapReportSettings, None), )
ModuleConfig.MapReportSettings._F = ((1, 'publish_interval_secs', 2, 0, None, None), (2, 'position_precision', 2, 0, None, None), (3, 'should_report_location', 6, 0, None, None), )
ModuleConfig.RemoteHardwareConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'allow_undefined_pin_access', 6, 0, None, None), (3, 'available_pins', 16, 1, RemoteHardwarePin, None), )
ModuleConfig.NeighborInfoConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'update_interval', 2, 0, None, None), (3, 'transmit_over_lora', 6, 0, None, None), )
ModuleConfig.DetectionSensorConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'minimum_broadcast_secs', 2, 0, None, None), (3, 'state_broadcast_secs', 2, 0, None, None), (4, 'send_bell', 6, 0, None, None), (5, 'name', 14, 0, None, None), (6, 'monitor_pin', 2, 0, None, None), (7, 'detection_trigger_type', 7, 0, None, None), (8, 'use_pullup', 6, 0, None, None), )
ModuleConfig.AudioConfig._F = ((1, 'codec2_enabled', 6, 0, None, None), (2, 'ptt_pin', 2, 0, None, None), (3, 'bitrate', 7, 0, None, None), (4, 'i2s_ws', 2, 0, None, None), (5, 'i2s_sd', 2, 0, None, None), (6, 'i2s_din', 2, 0, None, None), (7, 'i2s_sck', 2, 0, None, None), )
ModuleConfig.PaxcounterConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'paxcounter_update_interval', 2, 0, None, None), (3, 'wifi_threshold', 0, 0, None, None), (4, 'ble_threshold', 0, 0, None, None), )
ModuleConfig.TrafficManagementConfig._F = ((4, 'position_min_interval_secs', 2, 0, None, None), (6, 'nodeinfo_direct_response_max_hops', 2, 0, None, None), (8, 'rate_limit_window_secs', 2, 0, None, None), (9, 'rate_limit_max_packets', 2, 0, None, None), (11, 'unknown_packet_threshold', 2, 0, None, None), )
ModuleConfig.SerialConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'echo', 6, 0, None, None), (3, 'rxd', 2, 0, None, None), (4, 'txd', 2, 0, None, None), (5, 'baud', 7, 0, None, None), (6, 'timeout', 2, 0, None, None), (7, 'mode', 7, 0, None, None), (8, 'override_console_serial_port', 6, 0, None, None), )
ModuleConfig.ExternalNotificationConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'output_ms', 2, 0, None, None), (3, 'output', 2, 0, None, None), (4, 'active', 6, 0, None, None), (5, 'alert_message', 6, 0, None, None), (6, 'alert_bell', 6, 0, None, None), (7, 'use_pwm', 6, 0, None, None), (8, 'output_vibra', 2, 0, None, None), (9, 'output_buzzer', 2, 0, None, None), (10, 'alert_message_vibra', 6, 0, None, None), (11, 'alert_message_buzzer', 6, 0, None, None), (12, 'alert_bell_vibra', 6, 0, None, None), (13, 'alert_bell_buzzer', 6, 0, None, None), (14, 'nag_timeout', 2, 0, None, None), (15, 'use_i2s_as_buzzer', 6, 0, None, None), )
ModuleConfig.StoreForwardConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'heartbeat', 6, 0, None, None), (3, 'records', 2, 0, None, None), (4, 'history_return_max', 2, 0, None, None), (5, 'history_return_window', 2, 0, None, None), (6, 'is_server', 6, 0, None, None), )
ModuleConfig.RangeTestConfig._F = ((1, 'enabled', 6, 0, None, None), (2, 'sender', 2, 0, None, None), (3, 'save', 6, 0, None, None), (4, 'clear_on_reboot', 6, 0, None, None), )
ModuleConfig.TelemetryConfig._F = ((1, 'device_update_interval', 2, 0, None, None), (2, 'environment_update_interval', 2, 0, None, None), (3, 'environment_measurement_enabled', 6, 0, None, None), (4, 'environment_screen_enabled', 6, 0, None, None), (5, 'environment_display_fahrenheit', 6, 0, None, None), (6, 'air_quality_enabled', 6, 0, None, None), (7, 'air_quality_interval', 2, 0, None, None), (8, 'power_measurement_enabled', 6, 0, None, None), (9, 'power_update_interval', 2, 0, None, None), (10, 'power_screen_enabled', 6, 0, None, None), (11, 'health_measurement_enabled', 6, 0, None, None), (12, 'health_update_interval', 2, 0, None, None), (13, 'health_screen_enabled', 6, 0, None, None), (14, 'device_telemetry_enabled', 6, 0, None, None), (15, 'air_quality_screen_enabled', 6, 0, None, None), )
ModuleConfig.CannedMessageConfig._F = ((1, 'rotary1_enabled', 6, 0, None, None), (2, 'inputbroker_pin_a', 2, 0, None, None), (3, 'inputbroker_pin_b', 2, 0, None, None), (4, 'inputbroker_pin_press', 2, 0, None, None), (5, 'inputbroker_event_cw', 7, 0, None, None), (6, 'inputbroker_event_ccw', 7, 0, None, None), (7, 'inputbroker_event_press', 7, 0, None, None), (8, 'updown1_enabled', 6, 0, None, None), (9, 'enabled', 6, 0, None, None), (10, 'allow_input_source', 14, 0, None, None), (11, 'send_bell', 6, 0, None, None), )
ModuleConfig.AmbientLightingConfig._F = ((1, 'led_state', 6, 0, None, None), (2, 'current', 2, 0, None, None), (3, 'red', 2, 0, None, None), (4, 'green', 2, 0, None, None), (5, 'blue', 2, 0, None, None), )
ModuleConfig.StatusMessageConfig._F = ((1, 'node_status', 14, 0, None, None), )
ModuleConfig.MeshBeaconConfig.BroadcastTarget._F = ((1, 'preset', 7, 4, None, None), (2, 'region', 7, 0, None, None), (4, 'channel_index', 2, 4, None, None), (5, 'frequency_slot', 2, 4, None, None), )
ModuleConfig.MeshBeaconConfig._F = ((1, 'flags', 2, 0, None, None), (2, 'broadcast_offer_frequency_slot', 2, 4, None, None), (4, 'broadcast_message', 14, 0, None, None), (5, 'broadcast_offer_channel', 16, 4, channel_pb2.ChannelSettings, None), (6, 'broadcast_offer_region', 7, 0, None, None), (7, 'broadcast_offer_preset', 7, 4, None, None), (11, 'broadcast_interval_secs', 2, 0, None, None), (13, 'broadcast_targets', 16, 1, ModuleConfig.MeshBeaconConfig.BroadcastTarget, None), )
ModuleConfig.TAKConfig._F = ((1, 'team', 7, 0, None, None), (2, 'role', 7, 0, None, None), )
ModuleConfig._F = ((1, 'mqtt', 16, 4, ModuleConfig.MQTTConfig, 'payload_variant'), (2, 'serial', 16, 4, ModuleConfig.SerialConfig, 'payload_variant'), (3, 'external_notification', 16, 4, ModuleConfig.ExternalNotificationConfig, 'payload_variant'), (4, 'store_forward', 16, 4, ModuleConfig.StoreForwardConfig, 'payload_variant'), (5, 'range_test', 16, 4, ModuleConfig.RangeTestConfig, 'payload_variant'), (6, 'telemetry', 16, 4, ModuleConfig.TelemetryConfig, 'payload_variant'), (7, 'canned_message', 16, 4, ModuleConfig.CannedMessageConfig, 'payload_variant'), (8, 'audio', 16, 4, ModuleConfig.AudioConfig, 'payload_variant'), (9, 'remote_hardware', 16, 4, ModuleConfig.RemoteHardwareConfig, 'payload_variant'), (10, 'neighbor_info', 16, 4, ModuleConfig.NeighborInfoConfig, 'payload_variant'), (11, 'ambient_lighting', 16, 4, ModuleConfig.AmbientLightingConfig, 'payload_variant'), (12, 'detection_sensor', 16, 4, ModuleConfig.DetectionSensorConfig, 'payload_variant'), (13, 'paxcounter', 16, 4, ModuleConfig.PaxcounterConfig, 'payload_variant'), (14, 'statusmessage', 16, 4, ModuleConfig.StatusMessageConfig, 'payload_variant'), (15, 'traffic_management', 16, 4, ModuleConfig.TrafficManagementConfig, 'payload_variant'), (16, 'tak', 16, 4, ModuleConfig.TAKConfig, 'payload_variant'), (17, 'mesh_beacon', 16, 4, ModuleConfig.MeshBeaconConfig, 'payload_variant'), )
RemoteHardwarePin._F = ((1, 'gpio_pin', 2, 0, None, None), (2, 'name', 14, 0, None, None), (3, 'type', 7, 0, None, None), )
