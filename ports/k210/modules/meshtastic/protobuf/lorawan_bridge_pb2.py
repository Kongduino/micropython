# Generated from meshtastic/lorawan_bridge.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class LoRaWANBridge(Message):
    class Uplink(Message):
        pass
    class Downlink(Message):
        pass
    class PayloadChunk(Message):
        pass
    class TxResult(Message):
        class Status(Enum):
            _V = (('NONE', 0), ('TOO_LATE', 1), ('TOO_EARLY', 2), ('COLLISION_PACKET', 3), ('COLLISION_BEACON', 4), ('TX_FREQ', 5), ('TX_POWER', 6), ('GPS_UNLOCKED', 7), ('DEFERRED', 8), ('DROPPED', 9), )
            NONE = 0
            TOO_LATE = 1
            TOO_EARLY = 2
            COLLISION_PACKET = 3
            COLLISION_BEACON = 4
            TX_FREQ = 5
            TX_POWER = 6
            GPS_UNLOCKED = 7
            DEFERRED = 8
            DROPPED = 9
        NONE = 0
        TOO_LATE = 1
        TOO_EARLY = 2
        COLLISION_PACKET = 3
        COLLISION_BEACON = 4
        TX_FREQ = 5
        TX_POWER = 6
        GPS_UNLOCKED = 7
        DEFERRED = 8
        DROPPED = 9

LoRaWANBridge.Uplink._F = ((1, 'freq_hz', 8, 0, None, None), (2, 'tmst', 8, 0, None, None), (3, 'rssi_x10', 4, 0, None, None), (4, 'snr_x10', 4, 0, None, None), (5, 'radio_params', 2, 0, None, None), (6, 'payload', 15, 0, None, None), (7, 'payload_id', 2, 0, None, None), (8, 'chunk_count', 2, 0, None, None), (9, 'fsk_bitrate', 2, 0, None, None), )
LoRaWANBridge.Downlink._F = ((1, 'freq_hz', 8, 0, None, None), (2, 'tmst', 8, 0, None, None), (3, 'radio_params', 2, 0, None, None), (4, 'power_dbm', 2, 0, None, None), (5, 'immediate', 6, 0, None, None), (6, 'invert_polarity', 6, 0, None, None), (7, 'no_crc', 6, 0, None, None), (8, 'may_defer', 6, 0, None, None), (9, 'payload', 15, 0, None, None), (10, 'payload_id', 2, 0, None, None), (11, 'chunk_count', 2, 0, None, None), (12, 'request_id', 2, 0, None, None), )
LoRaWANBridge.PayloadChunk._F = ((1, 'payload_id', 2, 0, None, None), (2, 'chunk_index', 2, 0, None, None), (3, 'payload_chunk', 15, 0, None, None), )
LoRaWANBridge.TxResult._F = ((1, 'tmst', 8, 0, None, None), (2, 'status', 7, 0, None, None), (3, 'request_id', 2, 0, None, None), )
LoRaWANBridge._F = ((1, 'uplink', 16, 4, LoRaWANBridge.Uplink, 'variant'), (2, 'downlink', 16, 4, LoRaWANBridge.Downlink, 'variant'), (3, 'tx_result', 16, 4, LoRaWANBridge.TxResult, 'variant'), (4, 'chunk', 16, 4, LoRaWANBridge.PayloadChunk, 'variant'), )
