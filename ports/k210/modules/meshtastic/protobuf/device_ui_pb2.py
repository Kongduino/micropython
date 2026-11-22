# Generated from meshtastic/device_ui.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class CompassMode(Enum):
    _V = (('DYNAMIC', 0), ('FIXED_RING', 1), ('FREEZE_HEADING', 2), )
    DYNAMIC = 0
    FIXED_RING = 1
    FREEZE_HEADING = 2

class Theme(Enum):
    _V = (('DARK', 0), ('LIGHT', 1), ('RED', 2), )
    DARK = 0
    LIGHT = 1
    RED = 2

class Language(Enum):
    _V = (('ENGLISH', 0), ('FRENCH', 1), ('GERMAN', 2), ('ITALIAN', 3), ('PORTUGUESE', 4), ('SPANISH', 5), ('SWEDISH', 6), ('FINNISH', 7), ('POLISH', 8), ('TURKISH', 9), ('SERBIAN', 10), ('RUSSIAN', 11), ('DUTCH', 12), ('GREEK', 13), ('NORWEGIAN', 14), ('SLOVENIAN', 15), ('UKRAINIAN', 16), ('BULGARIAN', 17), ('CZECH', 18), ('DANISH', 19), ('HUNGARIAN', 20), ('AZERBAIJANI', 21), ('SIMPLIFIED_CHINESE', 30), ('TRADITIONAL_CHINESE', 31), )
    ENGLISH = 0
    FRENCH = 1
    GERMAN = 2
    ITALIAN = 3
    PORTUGUESE = 4
    SPANISH = 5
    SWEDISH = 6
    FINNISH = 7
    POLISH = 8
    TURKISH = 9
    SERBIAN = 10
    RUSSIAN = 11
    DUTCH = 12
    GREEK = 13
    NORWEGIAN = 14
    SLOVENIAN = 15
    UKRAINIAN = 16
    BULGARIAN = 17
    CZECH = 18
    DANISH = 19
    HUNGARIAN = 20
    AZERBAIJANI = 21
    SIMPLIFIED_CHINESE = 30
    TRADITIONAL_CHINESE = 31

class DeviceUIConfig(Message):
    class GpsCoordinateFormat(Enum):
        _V = (('DEC', 0), ('DMS', 1), ('UTM', 2), ('MGRS', 3), ('OLC', 4), ('OSGR', 5), ('MLS', 6), )
        DEC = 0
        DMS = 1
        UTM = 2
        MGRS = 3
        OLC = 4
        OSGR = 5
        MLS = 6
    DEC = 0
    DMS = 1
    UTM = 2
    MGRS = 3
    OLC = 4
    OSGR = 5
    MLS = 6

class NodeFilter(Message):
    pass

class NodeHighlight(Message):
    pass

class GeoPoint(Message):
    pass

class Map(Message):
    pass

DYNAMIC = 0
FIXED_RING = 1
FREEZE_HEADING = 2
DARK = 0
LIGHT = 1
RED = 2
ENGLISH = 0
FRENCH = 1
GERMAN = 2
ITALIAN = 3
PORTUGUESE = 4
SPANISH = 5
SWEDISH = 6
FINNISH = 7
POLISH = 8
TURKISH = 9
SERBIAN = 10
RUSSIAN = 11
DUTCH = 12
GREEK = 13
NORWEGIAN = 14
SLOVENIAN = 15
UKRAINIAN = 16
BULGARIAN = 17
CZECH = 18
DANISH = 19
HUNGARIAN = 20
AZERBAIJANI = 21
SIMPLIFIED_CHINESE = 30
TRADITIONAL_CHINESE = 31
DeviceUIConfig._F = ((1, 'version', 2, 0, None, None), (2, 'screen_brightness', 2, 0, None, None), (3, 'screen_timeout', 2, 0, None, None), (4, 'screen_lock', 6, 0, None, None), (5, 'settings_lock', 6, 0, None, None), (6, 'pin_code', 2, 0, None, None), (7, 'theme', 7, 0, None, None), (8, 'alert_enabled', 6, 0, None, None), (9, 'banner_enabled', 6, 0, None, None), (10, 'ring_tone_id', 2, 0, None, None), (11, 'language', 7, 0, None, None), (12, 'node_filter', 16, 4, NodeFilter, None), (13, 'node_highlight', 16, 4, NodeHighlight, None), (14, 'calibration_data', 15, 0, None, None), (15, 'map_data', 16, 4, Map, None), (16, 'compass_mode', 7, 0, None, None), (17, 'screen_rgb_color', 2, 0, None, None), (18, 'is_clockface_analog', 6, 0, None, None), (19, 'gps_format', 7, 0, None, None), )
NodeFilter._F = ((1, 'unknown_switch', 6, 0, None, None), (2, 'offline_switch', 6, 0, None, None), (3, 'public_key_switch', 6, 0, None, None), (4, 'hops_away', 0, 0, None, None), (5, 'position_switch', 6, 0, None, None), (6, 'node_name', 14, 0, None, None), (7, 'channel', 0, 0, None, None), )
NodeHighlight._F = ((1, 'chat_switch', 6, 0, None, None), (2, 'position_switch', 6, 0, None, None), (3, 'telemetry_switch', 6, 0, None, None), (4, 'iaq_switch', 6, 0, None, None), (5, 'node_name', 14, 0, None, None), )
GeoPoint._F = ((1, 'zoom', 0, 0, None, None), (2, 'latitude', 0, 0, None, None), (3, 'longitude', 0, 0, None, None), )
Map._F = ((1, 'home', 16, 4, GeoPoint, None), (2, 'style', 14, 0, None, None), (3, 'follow_gps', 6, 0, None, None), )
