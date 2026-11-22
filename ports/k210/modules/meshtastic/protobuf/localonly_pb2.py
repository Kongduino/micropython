# Generated from meshtastic/localonly.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import config_pb2
from meshtastic.protobuf import module_config_pb2

class LocalConfig(Message):
    pass

class LocalModuleConfig(Message):
    pass

LocalConfig._F = ((1, 'device', 16, 4, config_pb2.Config.DeviceConfig, None), (2, 'position', 16, 4, config_pb2.Config.PositionConfig, None), (3, 'power', 16, 4, config_pb2.Config.PowerConfig, None), (4, 'network', 16, 4, config_pb2.Config.NetworkConfig, None), (5, 'display', 16, 4, config_pb2.Config.DisplayConfig, None), (6, 'lora', 16, 4, config_pb2.Config.LoRaConfig, None), (7, 'bluetooth', 16, 4, config_pb2.Config.BluetoothConfig, None), (8, 'version', 2, 0, None, None), (9, 'security', 16, 4, config_pb2.Config.SecurityConfig, None), )
LocalModuleConfig._F = ((1, 'mqtt', 16, 4, module_config_pb2.ModuleConfig.MQTTConfig, None), (2, 'serial', 16, 4, module_config_pb2.ModuleConfig.SerialConfig, None), (3, 'external_notification', 16, 4, module_config_pb2.ModuleConfig.ExternalNotificationConfig, None), (4, 'store_forward', 16, 4, module_config_pb2.ModuleConfig.StoreForwardConfig, None), (5, 'range_test', 16, 4, module_config_pb2.ModuleConfig.RangeTestConfig, None), (6, 'telemetry', 16, 4, module_config_pb2.ModuleConfig.TelemetryConfig, None), (7, 'canned_message', 16, 4, module_config_pb2.ModuleConfig.CannedMessageConfig, None), (8, 'version', 2, 0, None, None), (9, 'audio', 16, 4, module_config_pb2.ModuleConfig.AudioConfig, None), (10, 'remote_hardware', 16, 4, module_config_pb2.ModuleConfig.RemoteHardwareConfig, None), (11, 'neighbor_info', 16, 4, module_config_pb2.ModuleConfig.NeighborInfoConfig, None), (12, 'ambient_lighting', 16, 4, module_config_pb2.ModuleConfig.AmbientLightingConfig, None), (13, 'detection_sensor', 16, 4, module_config_pb2.ModuleConfig.DetectionSensorConfig, None), (14, 'paxcounter', 16, 4, module_config_pb2.ModuleConfig.PaxcounterConfig, None), (15, 'statusmessage', 16, 4, module_config_pb2.ModuleConfig.StatusMessageConfig, None), (16, 'traffic_management', 16, 4, module_config_pb2.ModuleConfig.TrafficManagementConfig, None), (17, 'tak', 16, 4, module_config_pb2.ModuleConfig.TAKConfig, None), (18, 'mesh_beacon', 16, 4, module_config_pb2.ModuleConfig.MeshBeaconConfig, None), )
