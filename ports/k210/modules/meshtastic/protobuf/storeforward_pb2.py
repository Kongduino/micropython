# Generated from meshtastic/storeforward.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class StoreAndForward(Message):
    class RequestResponse(Enum):
        _V = (('UNSET', 0), ('ROUTER_ERROR', 1), ('ROUTER_HEARTBEAT', 2), ('ROUTER_PING', 3), ('ROUTER_PONG', 4), ('ROUTER_BUSY', 5), ('ROUTER_HISTORY', 6), ('ROUTER_STATS', 7), ('ROUTER_TEXT_DIRECT', 8), ('ROUTER_TEXT_BROADCAST', 9), ('CLIENT_ERROR', 64), ('CLIENT_HISTORY', 65), ('CLIENT_STATS', 66), ('CLIENT_PING', 67), ('CLIENT_PONG', 68), ('CLIENT_ABORT', 106), )
        UNSET = 0
        ROUTER_ERROR = 1
        ROUTER_HEARTBEAT = 2
        ROUTER_PING = 3
        ROUTER_PONG = 4
        ROUTER_BUSY = 5
        ROUTER_HISTORY = 6
        ROUTER_STATS = 7
        ROUTER_TEXT_DIRECT = 8
        ROUTER_TEXT_BROADCAST = 9
        CLIENT_ERROR = 64
        CLIENT_HISTORY = 65
        CLIENT_STATS = 66
        CLIENT_PING = 67
        CLIENT_PONG = 68
        CLIENT_ABORT = 106
    UNSET = 0
    ROUTER_ERROR = 1
    ROUTER_HEARTBEAT = 2
    ROUTER_PING = 3
    ROUTER_PONG = 4
    ROUTER_BUSY = 5
    ROUTER_HISTORY = 6
    ROUTER_STATS = 7
    ROUTER_TEXT_DIRECT = 8
    ROUTER_TEXT_BROADCAST = 9
    CLIENT_ERROR = 64
    CLIENT_HISTORY = 65
    CLIENT_STATS = 66
    CLIENT_PING = 67
    CLIENT_PONG = 68
    CLIENT_ABORT = 106
    class Statistics(Message):
        pass
    class History(Message):
        pass
    class Heartbeat(Message):
        pass

StoreAndForward.Statistics._F = ((1, 'messages_total', 2, 0, None, None), (2, 'messages_saved', 2, 0, None, None), (3, 'messages_max', 2, 0, None, None), (4, 'up_time', 2, 0, None, None), (5, 'requests', 2, 0, None, None), (6, 'requests_history', 2, 0, None, None), (7, 'heartbeat', 6, 0, None, None), (8, 'return_max', 2, 0, None, None), (9, 'return_window', 2, 0, None, None), )
StoreAndForward.History._F = ((1, 'history_messages', 2, 0, None, None), (2, 'window', 2, 0, None, None), (3, 'last_request', 2, 0, None, None), )
StoreAndForward.Heartbeat._F = ((1, 'period', 2, 0, None, None), (2, 'secondary', 2, 0, None, None), )
StoreAndForward._F = ((1, 'rr', 7, 0, None, None), (2, 'stats', 16, 4, StoreAndForward.Statistics, 'variant'), (3, 'history', 16, 4, StoreAndForward.History, 'variant'), (4, 'heartbeat', 16, 4, StoreAndForward.Heartbeat, 'variant'), (5, 'text', 15, 4, None, 'variant'), (6, 'original_id', 2, 0, None, None), )
