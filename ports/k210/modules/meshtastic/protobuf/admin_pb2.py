# Generated from meshtastic/admin.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import channel_pb2
from meshtastic.protobuf import config_pb2
from meshtastic.protobuf import connection_status_pb2
from meshtastic.protobuf import device_ui_pb2
from meshtastic.protobuf import mesh_pb2
from meshtastic.protobuf import module_config_pb2

class OTAMode(Enum):
    _V = (('NO_REBOOT_OTA', 0), ('OTA_BLE', 1), ('OTA_WIFI', 2), )
    NO_REBOOT_OTA = 0
    OTA_BLE = 1
    OTA_WIFI = 2

class AdminMessage(Message):
    class ConfigType(Enum):
        _V = (('DEVICE_CONFIG', 0), ('POSITION_CONFIG', 1), ('POWER_CONFIG', 2), ('NETWORK_CONFIG', 3), ('DISPLAY_CONFIG', 4), ('LORA_CONFIG', 5), ('BLUETOOTH_CONFIG', 6), ('SECURITY_CONFIG', 7), ('SESSIONKEY_CONFIG', 8), ('DEVICEUI_CONFIG', 9), )
        DEVICE_CONFIG = 0
        POSITION_CONFIG = 1
        POWER_CONFIG = 2
        NETWORK_CONFIG = 3
        DISPLAY_CONFIG = 4
        LORA_CONFIG = 5
        BLUETOOTH_CONFIG = 6
        SECURITY_CONFIG = 7
        SESSIONKEY_CONFIG = 8
        DEVICEUI_CONFIG = 9
    DEVICE_CONFIG = 0
    POSITION_CONFIG = 1
    POWER_CONFIG = 2
    NETWORK_CONFIG = 3
    DISPLAY_CONFIG = 4
    LORA_CONFIG = 5
    BLUETOOTH_CONFIG = 6
    SECURITY_CONFIG = 7
    SESSIONKEY_CONFIG = 8
    DEVICEUI_CONFIG = 9
    class ModuleConfigType(Enum):
        _V = (('MQTT_CONFIG', 0), ('SERIAL_CONFIG', 1), ('EXTNOTIF_CONFIG', 2), ('STOREFORWARD_CONFIG', 3), ('RANGETEST_CONFIG', 4), ('TELEMETRY_CONFIG', 5), ('CANNEDMSG_CONFIG', 6), ('AUDIO_CONFIG', 7), ('REMOTEHARDWARE_CONFIG', 8), ('NEIGHBORINFO_CONFIG', 9), ('AMBIENTLIGHTING_CONFIG', 10), ('DETECTIONSENSOR_CONFIG', 11), ('PAXCOUNTER_CONFIG', 12), ('STATUSMESSAGE_CONFIG', 13), ('TRAFFICMANAGEMENT_CONFIG', 14), ('TAK_CONFIG', 15), ('MESHBEACON_CONFIG', 16), )
        MQTT_CONFIG = 0
        SERIAL_CONFIG = 1
        EXTNOTIF_CONFIG = 2
        STOREFORWARD_CONFIG = 3
        RANGETEST_CONFIG = 4
        TELEMETRY_CONFIG = 5
        CANNEDMSG_CONFIG = 6
        AUDIO_CONFIG = 7
        REMOTEHARDWARE_CONFIG = 8
        NEIGHBORINFO_CONFIG = 9
        AMBIENTLIGHTING_CONFIG = 10
        DETECTIONSENSOR_CONFIG = 11
        PAXCOUNTER_CONFIG = 12
        STATUSMESSAGE_CONFIG = 13
        TRAFFICMANAGEMENT_CONFIG = 14
        TAK_CONFIG = 15
        MESHBEACON_CONFIG = 16
    MQTT_CONFIG = 0
    SERIAL_CONFIG = 1
    EXTNOTIF_CONFIG = 2
    STOREFORWARD_CONFIG = 3
    RANGETEST_CONFIG = 4
    TELEMETRY_CONFIG = 5
    CANNEDMSG_CONFIG = 6
    AUDIO_CONFIG = 7
    REMOTEHARDWARE_CONFIG = 8
    NEIGHBORINFO_CONFIG = 9
    AMBIENTLIGHTING_CONFIG = 10
    DETECTIONSENSOR_CONFIG = 11
    PAXCOUNTER_CONFIG = 12
    STATUSMESSAGE_CONFIG = 13
    TRAFFICMANAGEMENT_CONFIG = 14
    TAK_CONFIG = 15
    MESHBEACON_CONFIG = 16
    class BackupLocation(Enum):
        _V = (('FLASH', 0), ('SD', 1), )
        FLASH = 0
        SD = 1
    FLASH = 0
    SD = 1
    class InputEvent(Message):
        pass
    class OTAEvent(Message):
        pass

class LockdownAuth(Message):
    pass

class HamParameters(Message):
    pass

class NodeRemoteHardwarePinsResponse(Message):
    pass

class SharedContact(Message):
    pass

class KeyVerificationAdmin(Message):
    class MessageType(Enum):
        _V = (('INITIATE_VERIFICATION', 0), ('PROVIDE_SECURITY_NUMBER', 1), ('DO_VERIFY', 2), ('DO_NOT_VERIFY', 3), )
        INITIATE_VERIFICATION = 0
        PROVIDE_SECURITY_NUMBER = 1
        DO_VERIFY = 2
        DO_NOT_VERIFY = 3
    INITIATE_VERIFICATION = 0
    PROVIDE_SECURITY_NUMBER = 1
    DO_VERIFY = 2
    DO_NOT_VERIFY = 3

class SensorConfig(Message):
    pass

class SCD4X_config(Message):
    pass

class SEN5X_config(Message):
    pass

class SEN6X_config(Message):
    pass

class SCD30_config(Message):
    pass

class SHTXX_config(Message):
    pass

class DS248X_config(Message):
    pass

class AS3935_config(Message):
    pass

NO_REBOOT_OTA = 0
OTA_BLE = 1
OTA_WIFI = 2
AdminMessage.InputEvent._F = ((1, 'event_code', 2, 0, None, None), (2, 'kb_char', 2, 0, None, None), (3, 'touch_x', 2, 0, None, None), (4, 'touch_y', 2, 0, None, None), )
AdminMessage.OTAEvent._F = ((1, 'reboot_ota_mode', 7, 0, None, None), (2, 'ota_hash', 15, 0, None, None), )
AdminMessage._F = ((1, 'get_channel_request', 2, 4, None, 'payload_variant'), (2, 'get_channel_response', 16, 4, channel_pb2.Channel, 'payload_variant'), (3, 'get_owner_request', 6, 4, None, 'payload_variant'), (4, 'get_owner_response', 16, 4, mesh_pb2.User, 'payload_variant'), (5, 'get_config_request', 7, 4, None, 'payload_variant'), (6, 'get_config_response', 16, 4, config_pb2.Config, 'payload_variant'), (7, 'get_module_config_request', 7, 4, None, 'payload_variant'), (8, 'get_module_config_response', 16, 4, module_config_pb2.ModuleConfig, 'payload_variant'), (10, 'get_canned_message_module_messages_request', 6, 4, None, 'payload_variant'), (11, 'get_canned_message_module_messages_response', 14, 4, None, 'payload_variant'), (12, 'get_device_metadata_request', 6, 4, None, 'payload_variant'), (13, 'get_device_metadata_response', 16, 4, mesh_pb2.DeviceMetadata, 'payload_variant'), (14, 'get_ringtone_request', 6, 4, None, 'payload_variant'), (15, 'get_ringtone_response', 14, 4, None, 'payload_variant'), (16, 'get_device_connection_status_request', 6, 4, None, 'payload_variant'), (17, 'get_device_connection_status_response', 16, 4, connection_status_pb2.DeviceConnectionStatus, 'payload_variant'), (18, 'set_ham_mode', 16, 4, HamParameters, 'payload_variant'), (19, 'get_node_remote_hardware_pins_request', 6, 4, None, 'payload_variant'), (20, 'get_node_remote_hardware_pins_response', 16, 4, NodeRemoteHardwarePinsResponse, 'payload_variant'), (21, 'enter_dfu_mode_request', 6, 4, None, 'payload_variant'), (22, 'delete_file_request', 14, 4, None, 'payload_variant'), (23, 'set_scale', 2, 4, None, 'payload_variant'), (24, 'backup_preferences', 7, 4, None, 'payload_variant'), (25, 'restore_preferences', 7, 4, None, 'payload_variant'), (26, 'remove_backup_preferences', 7, 4, None, 'payload_variant'), (27, 'send_input_event', 16, 4, AdminMessage.InputEvent, 'payload_variant'), (32, 'set_owner', 16, 4, mesh_pb2.User, 'payload_variant'), (33, 'set_channel', 16, 4, channel_pb2.Channel, 'payload_variant'), (34, 'set_config', 16, 4, config_pb2.Config, 'payload_variant'), (35, 'set_module_config', 16, 4, module_config_pb2.ModuleConfig, 'payload_variant'), (36, 'set_canned_message_module_messages', 14, 4, None, 'payload_variant'), (37, 'set_ringtone_message', 14, 4, None, 'payload_variant'), (38, 'remove_by_nodenum', 2, 4, None, 'payload_variant'), (39, 'set_favorite_node', 2, 4, None, 'payload_variant'), (40, 'remove_favorite_node', 2, 4, None, 'payload_variant'), (41, 'set_fixed_position', 16, 4, mesh_pb2.Position, 'payload_variant'), (42, 'remove_fixed_position', 6, 4, None, 'payload_variant'), (43, 'set_time_only', 8, 4, None, 'payload_variant'), (44, 'get_ui_config_request', 6, 4, None, 'payload_variant'), (45, 'get_ui_config_response', 16, 4, device_ui_pb2.DeviceUIConfig, 'payload_variant'), (46, 'store_ui_config', 16, 4, device_ui_pb2.DeviceUIConfig, 'payload_variant'), (47, 'set_ignored_node', 2, 4, None, 'payload_variant'), (48, 'remove_ignored_node', 2, 4, None, 'payload_variant'), (49, 'toggle_muted_node', 2, 4, None, 'payload_variant'), (50, 'get_display_frame_request', 6, 4, None, 'payload_variant'), (51, 'set_display_mirror', 6, 4, None, 'payload_variant'), (64, 'begin_edit_settings', 6, 4, None, 'payload_variant'), (65, 'commit_edit_settings', 6, 4, None, 'payload_variant'), (66, 'add_contact', 16, 4, SharedContact, 'payload_variant'), (67, 'key_verification', 16, 4, KeyVerificationAdmin, 'payload_variant'), (94, 'factory_reset_device', 0, 4, None, 'payload_variant'), (95, 'reboot_ota_seconds', 0, 4, None, 'payload_variant'), (96, 'exit_simulator', 6, 4, None, 'payload_variant'), (97, 'reboot_seconds', 0, 4, None, 'payload_variant'), (98, 'shutdown_seconds', 0, 4, None, 'payload_variant'), (99, 'factory_reset_config', 0, 4, None, 'payload_variant'), (100, 'nodedb_reset', 6, 4, None, 'payload_variant'), (101, 'session_passkey', 15, 0, None, None), (102, 'ota_request', 16, 4, AdminMessage.OTAEvent, 'payload_variant'), (103, 'sensor_config', 16, 4, SensorConfig, 'payload_variant'), (104, 'lockdown_auth', 16, 4, LockdownAuth, 'payload_variant'), )
LockdownAuth._F = ((1, 'passphrase', 15, 0, None, None), (2, 'boots_remaining', 2, 0, None, None), (3, 'valid_until_epoch', 2, 0, None, None), (4, 'lock_now', 6, 0, None, None), (5, 'max_session_seconds', 2, 0, None, None), (6, 'disable', 6, 0, None, None), )
HamParameters._F = ((1, 'call_sign', 14, 0, None, None), (2, 'tx_power', 0, 0, None, None), (3, 'frequency', 10, 0, None, None), (4, 'short_name', 14, 0, None, None), (5, 'long_name', 14, 0, None, None), )
NodeRemoteHardwarePinsResponse._F = ((1, 'node_remote_hardware_pins', 16, 1, mesh_pb2.NodeRemoteHardwarePin, None), )
SharedContact._F = ((1, 'node_num', 2, 0, None, None), (2, 'user', 16, 4, mesh_pb2.User, None), (3, 'should_ignore', 6, 0, None, None), (4, 'manually_verified', 6, 0, None, None), )
KeyVerificationAdmin._F = ((1, 'message_type', 7, 0, None, None), (2, 'remote_nodenum', 2, 0, None, None), (3, 'nonce', 3, 0, None, None), (4, 'security_number', 2, 4, None, None), )
SensorConfig._F = ((1, 'scd4x_config', 16, 4, SCD4X_config, None), (2, 'sen5x_config', 16, 4, SEN5X_config, None), (3, 'scd30_config', 16, 4, SCD30_config, None), (4, 'shtxx_config', 16, 4, SHTXX_config, None), (5, 'ds248x_config', 16, 4, DS248X_config, None), (6, 'sen6x_config', 16, 4, SEN6X_config, None), (7, 'as3935_config', 16, 4, AS3935_config, None), )
SCD4X_config._F = ((1, 'set_asc', 6, 4, None, None), (2, 'set_target_co2_conc', 2, 4, None, None), (3, 'set_temperature', 10, 4, None, None), (4, 'set_altitude', 2, 4, None, None), (5, 'set_ambient_pressure', 2, 4, None, None), (6, 'factory_reset', 6, 4, None, None), (7, 'set_power_mode', 6, 4, None, None), )
SEN5X_config._F = ((1, 'set_temperature', 10, 4, None, None), (2, 'set_one_shot_mode', 6, 4, None, None), (3, 'start_fan_cleaning', 6, 4, None, None), )
SEN6X_config._F = ((1, 'set_temperature', 10, 4, None, None), (2, 'set_one_shot_mode', 6, 4, None, None), (3, 'start_fan_cleaning', 6, 4, None, None), (4, 'set_asc', 6, 4, None, None), (5, 'set_target_co2_conc', 2, 4, None, None), (6, 'set_altitude', 2, 4, None, None), (7, 'set_ambient_pressure', 2, 4, None, None), (8, 'factory_reset', 6, 4, None, None), )
SCD30_config._F = ((1, 'set_asc', 6, 4, None, None), (2, 'set_target_co2_conc', 2, 4, None, None), (3, 'set_temperature', 10, 4, None, None), (4, 'set_altitude', 2, 4, None, None), (5, 'set_measurement_interval', 2, 4, None, None), (6, 'soft_reset', 6, 4, None, None), )
SHTXX_config._F = ((1, 'set_accuracy', 2, 4, None, None), )
DS248X_config._F = ((1, 'main_temperature_channel', 2, 4, None, None), )
AS3935_config._F = ((1, 'set_tuning_cap_pf', 2, 4, None, None), )
