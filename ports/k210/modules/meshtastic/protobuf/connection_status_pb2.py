# Generated from meshtastic/connection_status.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class DeviceConnectionStatus(Message):
    pass

class WifiConnectionStatus(Message):
    pass

class EthernetConnectionStatus(Message):
    pass

class NetworkConnectionStatus(Message):
    pass

class BluetoothConnectionStatus(Message):
    pass

class SerialConnectionStatus(Message):
    pass

DeviceConnectionStatus._F = ((1, 'wifi', 16, 4, WifiConnectionStatus, None), (2, 'ethernet', 16, 4, EthernetConnectionStatus, None), (3, 'bluetooth', 16, 4, BluetoothConnectionStatus, None), (4, 'serial', 16, 4, SerialConnectionStatus, None), )
WifiConnectionStatus._F = ((1, 'status', 16, 4, NetworkConnectionStatus, None), (2, 'ssid', 14, 0, None, None), (3, 'rssi', 0, 0, None, None), )
EthernetConnectionStatus._F = ((1, 'status', 16, 4, NetworkConnectionStatus, None), )
NetworkConnectionStatus._F = ((1, 'ip_address', 8, 0, None, None), (2, 'is_connected', 6, 0, None, None), (3, 'is_mqtt_connected', 6, 0, None, None), (4, 'is_syslog_connected', 6, 0, None, None), )
BluetoothConnectionStatus._F = ((1, 'pin', 2, 0, None, None), (2, 'rssi', 0, 0, None, None), (3, 'is_connected', 6, 0, None, None), )
SerialConnectionStatus._F = ((1, 'baud', 2, 0, None, None), (2, 'is_connected', 6, 0, None, None), )
