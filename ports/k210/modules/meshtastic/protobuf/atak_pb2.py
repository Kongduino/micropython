# Generated from meshtastic/atak.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum
from meshtastic.protobuf import field_metadata_pb2

class Team(Enum):
    _V = (('Unspecifed_Color', 0), ('White', 1), ('Yellow', 2), ('Orange', 3), ('Magenta', 4), ('Red', 5), ('Maroon', 6), ('Purple', 7), ('Dark_Blue', 8), ('Blue', 9), ('Cyan', 10), ('Teal', 11), ('Green', 12), ('Dark_Green', 13), ('Brown', 14), )
    Unspecifed_Color = 0
    White = 1
    Yellow = 2
    Orange = 3
    Magenta = 4
    Red = 5
    Maroon = 6
    Purple = 7
    Dark_Blue = 8
    Blue = 9
    Cyan = 10
    Teal = 11
    Green = 12
    Dark_Green = 13
    Brown = 14

class MemberRole(Enum):
    _V = (('Unspecifed', 0), ('TeamMember', 1), ('TeamLead', 2), ('HQ', 3), ('Sniper', 4), ('Medic', 5), ('ForwardObserver', 6), ('RTO', 7), ('K9', 8), )
    Unspecifed = 0
    TeamMember = 1
    TeamLead = 2
    HQ = 3
    Sniper = 4
    Medic = 5
    ForwardObserver = 6
    RTO = 7
    K9 = 8

class CotHow(Enum):
    _V = (('CotHow_Unspecified', 0), ('CotHow_h_e', 1), ('CotHow_m_g', 2), ('CotHow_h_g_i_g_o', 3), ('CotHow_m_r', 4), ('CotHow_m_f', 5), ('CotHow_m_p', 6), ('CotHow_m_s', 7), )
    CotHow_Unspecified = 0
    CotHow_h_e = 1
    CotHow_m_g = 2
    CotHow_h_g_i_g_o = 3
    CotHow_m_r = 4
    CotHow_m_f = 5
    CotHow_m_p = 6
    CotHow_m_s = 7

class CotType(Enum):
    _V = (('CotType_Other', 0), ('CotType_a_f_G_U_C', 1), ('CotType_a_f_G_U_C_I', 2), ('CotType_a_n_A_C_F', 3), ('CotType_a_n_A_C_H', 4), ('CotType_a_n_A_C', 5), ('CotType_a_f_A_M_H', 6), ('CotType_a_f_A_M', 7), ('CotType_a_f_A_M_F_F', 8), ('CotType_a_f_A_M_H_A', 9), ('CotType_a_f_A_M_H_U_M', 10), ('CotType_a_h_A_M_F_F', 11), ('CotType_a_h_A_M_H_A', 12), ('CotType_a_u_A_C', 13), ('CotType_t_x_d_d', 14), ('CotType_a_f_G_E_S_E', 15), ('CotType_a_f_G_E_V_C', 16), ('CotType_a_f_S', 17), ('CotType_a_f_A_M_F', 18), ('CotType_a_f_A_M_F_C_H', 19), ('CotType_a_f_A_M_F_U_L', 20), ('CotType_a_f_A_M_F_L', 21), ('CotType_a_f_A_M_F_P', 22), ('CotType_a_f_A_C_H', 23), ('CotType_a_n_A_M_F_Q', 24), ('CotType_b_t_f', 25), ('CotType_b_r_f_h_c', 26), ('CotType_b_a_o_pan', 27), ('CotType_b_a_o_opn', 28), ('CotType_b_a_o_can', 29), ('CotType_b_a_o_tbl', 30), ('CotType_b_a_g', 31), ('CotType_a_f_G', 32), ('CotType_a_f_G_U', 33), ('CotType_a_h_G', 34), ('CotType_a_u_G', 35), ('CotType_a_n_G', 36), ('CotType_b_m_r', 37), ('CotType_b_m_p_w', 38), ('CotType_b_m_p_s_p_i', 39), ('CotType_u_d_f', 40), ('CotType_u_d_r', 41), ('CotType_u_d_c_c', 42), ('CotType_u_rb_a', 43), ('CotType_a_h_A', 44), ('CotType_a_u_A', 45), ('CotType_a_f_A_M_H_Q', 46), ('CotType_a_f_A_C_F', 47), ('CotType_a_f_A_C', 48), ('CotType_a_f_A_C_L', 49), ('CotType_a_f_A', 50), ('CotType_a_f_A_M_H_C', 51), ('CotType_a_n_A_M_F_F', 52), ('CotType_a_u_A_C_F', 53), ('CotType_a_f_G_U_C_F_T_A', 54), ('CotType_a_f_G_U_C_V_S', 55), ('CotType_a_f_G_U_C_R_X', 56), ('CotType_a_f_G_U_C_I_Z', 57), ('CotType_a_f_G_U_C_E_C_W', 58), ('CotType_a_f_G_U_C_I_L', 59), ('CotType_a_f_G_U_C_R_O', 60), ('CotType_a_f_G_U_C_R_V', 61), ('CotType_a_f_G_U_H', 62), ('CotType_a_f_G_U_U_M_S_E', 63), ('CotType_a_f_G_U_S_M_C', 64), ('CotType_a_f_G_E_S', 65), ('CotType_a_f_G_E', 66), ('CotType_a_f_G_E_V_C_U', 67), ('CotType_a_f_G_E_V_C_ps', 68), ('CotType_a_u_G_E_V', 69), ('CotType_a_f_S_N_N_R', 70), ('CotType_a_f_F_B', 71), ('CotType_b_m_p_s_p_loc', 72), ('CotType_b_i_v', 73), ('CotType_b_f_t_r', 74), ('CotType_b_f_t_a', 75), ('CotType_u_d_f_m', 76), ('CotType_u_d_p', 77), ('CotType_b_m_p_s_m', 78), ('CotType_b_m_p_c', 79), ('CotType_u_r_b_c_c', 80), ('CotType_u_r_b_bullseye', 81), ('CotType_a_f_G_E_V_A', 82), ('CotType_a_n_A', 83), ('CotType_a_u_G_U_C_F', 84), ('CotType_a_n_G_U_C_F', 85), ('CotType_a_h_G_U_C_F', 86), ('CotType_a_f_G_U_C_F', 87), ('CotType_a_u_G_I', 88), ('CotType_a_n_G_I', 89), ('CotType_a_h_G_I', 90), ('CotType_a_f_G_I', 91), ('CotType_a_u_G_E_X_M', 92), ('CotType_a_n_G_E_X_M', 93), ('CotType_a_h_G_E_X_M', 94), ('CotType_a_f_G_E_X_M', 95), ('CotType_a_u_S', 96), ('CotType_a_n_S', 97), ('CotType_a_h_S', 98), ('CotType_a_u_G_U_C_I_d', 99), ('CotType_a_n_G_U_C_I_d', 100), ('CotType_a_h_G_U_C_I_d', 101), ('CotType_a_f_G_U_C_I_d', 102), ('CotType_a_u_G_E_V_A_T', 103), ('CotType_a_n_G_E_V_A_T', 104), ('CotType_a_h_G_E_V_A_T', 105), ('CotType_a_f_G_E_V_A_T', 106), ('CotType_a_u_G_U_C_I', 107), ('CotType_a_n_G_U_C_I', 108), ('CotType_a_h_G_U_C_I', 109), ('CotType_a_n_G_E_V', 110), ('CotType_a_h_G_E_V', 111), ('CotType_a_f_G_E_V', 112), ('CotType_b_m_p_w_GOTO', 113), ('CotType_b_m_p_c_ip', 114), ('CotType_b_m_p_c_cp', 115), ('CotType_b_m_p_s_p_op', 116), ('CotType_u_d_v', 117), ('CotType_u_d_v_m', 118), ('CotType_u_d_c_e', 119), ('CotType_b_i_x_i', 120), ('CotType_b_t_f_d', 121), ('CotType_b_t_f_r', 122), ('CotType_b_a_o_c', 123), ('CotType_t_s', 124), ('CotType_m_t_t', 125), ('CotType_y', 126), )
    CotType_Other = 0
    CotType_a_f_G_U_C = 1
    CotType_a_f_G_U_C_I = 2
    CotType_a_n_A_C_F = 3
    CotType_a_n_A_C_H = 4
    CotType_a_n_A_C = 5
    CotType_a_f_A_M_H = 6
    CotType_a_f_A_M = 7
    CotType_a_f_A_M_F_F = 8
    CotType_a_f_A_M_H_A = 9
    CotType_a_f_A_M_H_U_M = 10
    CotType_a_h_A_M_F_F = 11
    CotType_a_h_A_M_H_A = 12
    CotType_a_u_A_C = 13
    CotType_t_x_d_d = 14
    CotType_a_f_G_E_S_E = 15
    CotType_a_f_G_E_V_C = 16
    CotType_a_f_S = 17
    CotType_a_f_A_M_F = 18
    CotType_a_f_A_M_F_C_H = 19
    CotType_a_f_A_M_F_U_L = 20
    CotType_a_f_A_M_F_L = 21
    CotType_a_f_A_M_F_P = 22
    CotType_a_f_A_C_H = 23
    CotType_a_n_A_M_F_Q = 24
    CotType_b_t_f = 25
    CotType_b_r_f_h_c = 26
    CotType_b_a_o_pan = 27
    CotType_b_a_o_opn = 28
    CotType_b_a_o_can = 29
    CotType_b_a_o_tbl = 30
    CotType_b_a_g = 31
    CotType_a_f_G = 32
    CotType_a_f_G_U = 33
    CotType_a_h_G = 34
    CotType_a_u_G = 35
    CotType_a_n_G = 36
    CotType_b_m_r = 37
    CotType_b_m_p_w = 38
    CotType_b_m_p_s_p_i = 39
    CotType_u_d_f = 40
    CotType_u_d_r = 41
    CotType_u_d_c_c = 42
    CotType_u_rb_a = 43
    CotType_a_h_A = 44
    CotType_a_u_A = 45
    CotType_a_f_A_M_H_Q = 46
    CotType_a_f_A_C_F = 47
    CotType_a_f_A_C = 48
    CotType_a_f_A_C_L = 49
    CotType_a_f_A = 50
    CotType_a_f_A_M_H_C = 51
    CotType_a_n_A_M_F_F = 52
    CotType_a_u_A_C_F = 53
    CotType_a_f_G_U_C_F_T_A = 54
    CotType_a_f_G_U_C_V_S = 55
    CotType_a_f_G_U_C_R_X = 56
    CotType_a_f_G_U_C_I_Z = 57
    CotType_a_f_G_U_C_E_C_W = 58
    CotType_a_f_G_U_C_I_L = 59
    CotType_a_f_G_U_C_R_O = 60
    CotType_a_f_G_U_C_R_V = 61
    CotType_a_f_G_U_H = 62
    CotType_a_f_G_U_U_M_S_E = 63
    CotType_a_f_G_U_S_M_C = 64
    CotType_a_f_G_E_S = 65
    CotType_a_f_G_E = 66
    CotType_a_f_G_E_V_C_U = 67
    CotType_a_f_G_E_V_C_ps = 68
    CotType_a_u_G_E_V = 69
    CotType_a_f_S_N_N_R = 70
    CotType_a_f_F_B = 71
    CotType_b_m_p_s_p_loc = 72
    CotType_b_i_v = 73
    CotType_b_f_t_r = 74
    CotType_b_f_t_a = 75
    CotType_u_d_f_m = 76
    CotType_u_d_p = 77
    CotType_b_m_p_s_m = 78
    CotType_b_m_p_c = 79
    CotType_u_r_b_c_c = 80
    CotType_u_r_b_bullseye = 81
    CotType_a_f_G_E_V_A = 82
    CotType_a_n_A = 83
    CotType_a_u_G_U_C_F = 84
    CotType_a_n_G_U_C_F = 85
    CotType_a_h_G_U_C_F = 86
    CotType_a_f_G_U_C_F = 87
    CotType_a_u_G_I = 88
    CotType_a_n_G_I = 89
    CotType_a_h_G_I = 90
    CotType_a_f_G_I = 91
    CotType_a_u_G_E_X_M = 92
    CotType_a_n_G_E_X_M = 93
    CotType_a_h_G_E_X_M = 94
    CotType_a_f_G_E_X_M = 95
    CotType_a_u_S = 96
    CotType_a_n_S = 97
    CotType_a_h_S = 98
    CotType_a_u_G_U_C_I_d = 99
    CotType_a_n_G_U_C_I_d = 100
    CotType_a_h_G_U_C_I_d = 101
    CotType_a_f_G_U_C_I_d = 102
    CotType_a_u_G_E_V_A_T = 103
    CotType_a_n_G_E_V_A_T = 104
    CotType_a_h_G_E_V_A_T = 105
    CotType_a_f_G_E_V_A_T = 106
    CotType_a_u_G_U_C_I = 107
    CotType_a_n_G_U_C_I = 108
    CotType_a_h_G_U_C_I = 109
    CotType_a_n_G_E_V = 110
    CotType_a_h_G_E_V = 111
    CotType_a_f_G_E_V = 112
    CotType_b_m_p_w_GOTO = 113
    CotType_b_m_p_c_ip = 114
    CotType_b_m_p_c_cp = 115
    CotType_b_m_p_s_p_op = 116
    CotType_u_d_v = 117
    CotType_u_d_v_m = 118
    CotType_u_d_c_e = 119
    CotType_b_i_x_i = 120
    CotType_b_t_f_d = 121
    CotType_b_t_f_r = 122
    CotType_b_a_o_c = 123
    CotType_t_s = 124
    CotType_m_t_t = 125
    CotType_y = 126

class GeoPointSource(Enum):
    _V = (('GeoPointSource_Unspecified', 0), ('GeoPointSource_GPS', 1), ('GeoPointSource_USER', 2), ('GeoPointSource_NETWORK', 3), )
    GeoPointSource_Unspecified = 0
    GeoPointSource_GPS = 1
    GeoPointSource_USER = 2
    GeoPointSource_NETWORK = 3

class TAKPacket(Message):
    pass

class GeoChat(Message):
    class ReceiptType(Enum):
        _V = (('ReceiptType_None', 0), ('ReceiptType_Delivered', 1), ('ReceiptType_Read', 2), )
        ReceiptType_None = 0
        ReceiptType_Delivered = 1
        ReceiptType_Read = 2
    ReceiptType_None = 0
    ReceiptType_Delivered = 1
    ReceiptType_Read = 2

class Group(Message):
    pass

class Status(Message):
    pass

class Contact(Message):
    pass

class PLI(Message):
    pass

class AircraftTrack(Message):
    pass

class CotGeoPoint(Message):
    pass

class DrawnShape(Message):
    class Kind(Enum):
        _V = (('Kind_Unspecified', 0), ('Kind_Circle', 1), ('Kind_Rectangle', 2), ('Kind_Freeform', 3), ('Kind_Telestration', 4), ('Kind_Polygon', 5), ('Kind_RangingCircle', 6), ('Kind_Bullseye', 7), ('Kind_Ellipse', 8), ('Kind_Vehicle2D', 9), ('Kind_Vehicle3D', 10), )
        Kind_Unspecified = 0
        Kind_Circle = 1
        Kind_Rectangle = 2
        Kind_Freeform = 3
        Kind_Telestration = 4
        Kind_Polygon = 5
        Kind_RangingCircle = 6
        Kind_Bullseye = 7
        Kind_Ellipse = 8
        Kind_Vehicle2D = 9
        Kind_Vehicle3D = 10
    Kind_Unspecified = 0
    Kind_Circle = 1
    Kind_Rectangle = 2
    Kind_Freeform = 3
    Kind_Telestration = 4
    Kind_Polygon = 5
    Kind_RangingCircle = 6
    Kind_Bullseye = 7
    Kind_Ellipse = 8
    Kind_Vehicle2D = 9
    Kind_Vehicle3D = 10
    class StyleMode(Enum):
        _V = (('StyleMode_Unspecified', 0), ('StyleMode_StrokeOnly', 1), ('StyleMode_FillOnly', 2), ('StyleMode_StrokeAndFill', 3), )
        StyleMode_Unspecified = 0
        StyleMode_StrokeOnly = 1
        StyleMode_FillOnly = 2
        StyleMode_StrokeAndFill = 3
    StyleMode_Unspecified = 0
    StyleMode_StrokeOnly = 1
    StyleMode_FillOnly = 2
    StyleMode_StrokeAndFill = 3

class Marker(Message):
    class Kind(Enum):
        _V = (('Kind_Unspecified', 0), ('Kind_Spot', 1), ('Kind_Waypoint', 2), ('Kind_Checkpoint', 3), ('Kind_SelfPosition', 4), ('Kind_Symbol2525', 5), ('Kind_SpotMap', 6), ('Kind_CustomIcon', 7), ('Kind_GoToPoint', 8), ('Kind_InitialPoint', 9), ('Kind_ContactPoint', 10), ('Kind_ObservationPost', 11), ('Kind_ImageMarker', 12), )
        Kind_Unspecified = 0
        Kind_Spot = 1
        Kind_Waypoint = 2
        Kind_Checkpoint = 3
        Kind_SelfPosition = 4
        Kind_Symbol2525 = 5
        Kind_SpotMap = 6
        Kind_CustomIcon = 7
        Kind_GoToPoint = 8
        Kind_InitialPoint = 9
        Kind_ContactPoint = 10
        Kind_ObservationPost = 11
        Kind_ImageMarker = 12
    Kind_Unspecified = 0
    Kind_Spot = 1
    Kind_Waypoint = 2
    Kind_Checkpoint = 3
    Kind_SelfPosition = 4
    Kind_Symbol2525 = 5
    Kind_SpotMap = 6
    Kind_CustomIcon = 7
    Kind_GoToPoint = 8
    Kind_InitialPoint = 9
    Kind_ContactPoint = 10
    Kind_ObservationPost = 11
    Kind_ImageMarker = 12

class RangeAndBearing(Message):
    pass

class Route(Message):
    class Method(Enum):
        _V = (('Method_Unspecified', 0), ('Method_Driving', 1), ('Method_Walking', 2), ('Method_Flying', 3), ('Method_Swimming', 4), ('Method_Watercraft', 5), )
        Method_Unspecified = 0
        Method_Driving = 1
        Method_Walking = 2
        Method_Flying = 3
        Method_Swimming = 4
        Method_Watercraft = 5
    Method_Unspecified = 0
    Method_Driving = 1
    Method_Walking = 2
    Method_Flying = 3
    Method_Swimming = 4
    Method_Watercraft = 5
    class Direction(Enum):
        _V = (('Direction_Unspecified', 0), ('Direction_Infil', 1), ('Direction_Exfil', 2), )
        Direction_Unspecified = 0
        Direction_Infil = 1
        Direction_Exfil = 2
    Direction_Unspecified = 0
    Direction_Infil = 1
    Direction_Exfil = 2
    class Link(Message):
        pass

class CasevacReport(Message):
    class Precedence(Enum):
        _V = (('Precedence_Unspecified', 0), ('Precedence_Urgent', 1), ('Precedence_UrgentSurgical', 2), ('Precedence_Priority', 3), ('Precedence_Routine', 4), ('Precedence_Convenience', 5), )
        Precedence_Unspecified = 0
        Precedence_Urgent = 1
        Precedence_UrgentSurgical = 2
        Precedence_Priority = 3
        Precedence_Routine = 4
        Precedence_Convenience = 5
    Precedence_Unspecified = 0
    Precedence_Urgent = 1
    Precedence_UrgentSurgical = 2
    Precedence_Priority = 3
    Precedence_Routine = 4
    Precedence_Convenience = 5
    class HlzMarking(Enum):
        _V = (('HlzMarking_Unspecified', 0), ('HlzMarking_Panels', 1), ('HlzMarking_PyroSignal', 2), ('HlzMarking_Smoke', 3), ('HlzMarking_None', 4), ('HlzMarking_Other', 5), )
        HlzMarking_Unspecified = 0
        HlzMarking_Panels = 1
        HlzMarking_PyroSignal = 2
        HlzMarking_Smoke = 3
        HlzMarking_None = 4
        HlzMarking_Other = 5
    HlzMarking_Unspecified = 0
    HlzMarking_Panels = 1
    HlzMarking_PyroSignal = 2
    HlzMarking_Smoke = 3
    HlzMarking_None = 4
    HlzMarking_Other = 5
    class Security(Enum):
        _V = (('Security_Unspecified', 0), ('Security_NoEnemy', 1), ('Security_PossibleEnemy', 2), ('Security_EnemyInArea', 3), ('Security_EnemyInArmedContact', 4), )
        Security_Unspecified = 0
        Security_NoEnemy = 1
        Security_PossibleEnemy = 2
        Security_EnemyInArea = 3
        Security_EnemyInArmedContact = 4
    Security_Unspecified = 0
    Security_NoEnemy = 1
    Security_PossibleEnemy = 2
    Security_EnemyInArea = 3
    Security_EnemyInArmedContact = 4

class ZMistEntry(Message):
    pass

class EmergencyAlert(Message):
    class Type(Enum):
        _V = (('Type_Unspecified', 0), ('Type_Alert911', 1), ('Type_RingTheBell', 2), ('Type_InContact', 3), ('Type_GeoFenceBreached', 4), ('Type_Custom', 5), ('Type_Cancel', 6), )
        Type_Unspecified = 0
        Type_Alert911 = 1
        Type_RingTheBell = 2
        Type_InContact = 3
        Type_GeoFenceBreached = 4
        Type_Custom = 5
        Type_Cancel = 6
    Type_Unspecified = 0
    Type_Alert911 = 1
    Type_RingTheBell = 2
    Type_InContact = 3
    Type_GeoFenceBreached = 4
    Type_Custom = 5
    Type_Cancel = 6

class TaskRequest(Message):
    class Priority(Enum):
        _V = (('Priority_Unspecified', 0), ('Priority_Low', 1), ('Priority_Normal', 2), ('Priority_High', 3), ('Priority_Critical', 4), )
        Priority_Unspecified = 0
        Priority_Low = 1
        Priority_Normal = 2
        Priority_High = 3
        Priority_Critical = 4
    Priority_Unspecified = 0
    Priority_Low = 1
    Priority_Normal = 2
    Priority_High = 3
    Priority_Critical = 4
    class Status(Enum):
        _V = (('Status_Unspecified', 0), ('Status_Pending', 1), ('Status_Acknowledged', 2), ('Status_InProgress', 3), ('Status_Completed', 4), ('Status_Cancelled', 5), )
        Status_Unspecified = 0
        Status_Pending = 1
        Status_Acknowledged = 2
        Status_InProgress = 3
        Status_Completed = 4
        Status_Cancelled = 5
    Status_Unspecified = 0
    Status_Pending = 1
    Status_Acknowledged = 2
    Status_InProgress = 3
    Status_Completed = 4
    Status_Cancelled = 5

class TAKEnvironment(Message):
    pass

class SensorFov(Message):
    class SensorType(Enum):
        _V = (('SensorType_Unspecified', 0), ('SensorType_Camera', 1), ('SensorType_Thermal', 2), ('SensorType_Laser', 3), ('SensorType_Nvg', 4), ('SensorType_Rf', 5), ('SensorType_Other', 6), )
        SensorType_Unspecified = 0
        SensorType_Camera = 1
        SensorType_Thermal = 2
        SensorType_Laser = 3
        SensorType_Nvg = 4
        SensorType_Rf = 5
        SensorType_Other = 6
    SensorType_Unspecified = 0
    SensorType_Camera = 1
    SensorType_Thermal = 2
    SensorType_Laser = 3
    SensorType_Nvg = 4
    SensorType_Rf = 5
    SensorType_Other = 6

class TakTalkMessage(Message):
    pass

class TakTalkRoomData(Message):
    pass

class Marti(Message):
    pass

class TAKPacketV2(Message):
    pass

Unspecifed_Color = 0
White = 1
Yellow = 2
Orange = 3
Magenta = 4
Red = 5
Maroon = 6
Purple = 7
Dark_Blue = 8
Blue = 9
Cyan = 10
Teal = 11
Green = 12
Dark_Green = 13
Brown = 14
Unspecifed = 0
TeamMember = 1
TeamLead = 2
HQ = 3
Sniper = 4
Medic = 5
ForwardObserver = 6
RTO = 7
K9 = 8
CotHow_Unspecified = 0
CotHow_h_e = 1
CotHow_m_g = 2
CotHow_h_g_i_g_o = 3
CotHow_m_r = 4
CotHow_m_f = 5
CotHow_m_p = 6
CotHow_m_s = 7
CotType_Other = 0
CotType_a_f_G_U_C = 1
CotType_a_f_G_U_C_I = 2
CotType_a_n_A_C_F = 3
CotType_a_n_A_C_H = 4
CotType_a_n_A_C = 5
CotType_a_f_A_M_H = 6
CotType_a_f_A_M = 7
CotType_a_f_A_M_F_F = 8
CotType_a_f_A_M_H_A = 9
CotType_a_f_A_M_H_U_M = 10
CotType_a_h_A_M_F_F = 11
CotType_a_h_A_M_H_A = 12
CotType_a_u_A_C = 13
CotType_t_x_d_d = 14
CotType_a_f_G_E_S_E = 15
CotType_a_f_G_E_V_C = 16
CotType_a_f_S = 17
CotType_a_f_A_M_F = 18
CotType_a_f_A_M_F_C_H = 19
CotType_a_f_A_M_F_U_L = 20
CotType_a_f_A_M_F_L = 21
CotType_a_f_A_M_F_P = 22
CotType_a_f_A_C_H = 23
CotType_a_n_A_M_F_Q = 24
CotType_b_t_f = 25
CotType_b_r_f_h_c = 26
CotType_b_a_o_pan = 27
CotType_b_a_o_opn = 28
CotType_b_a_o_can = 29
CotType_b_a_o_tbl = 30
CotType_b_a_g = 31
CotType_a_f_G = 32
CotType_a_f_G_U = 33
CotType_a_h_G = 34
CotType_a_u_G = 35
CotType_a_n_G = 36
CotType_b_m_r = 37
CotType_b_m_p_w = 38
CotType_b_m_p_s_p_i = 39
CotType_u_d_f = 40
CotType_u_d_r = 41
CotType_u_d_c_c = 42
CotType_u_rb_a = 43
CotType_a_h_A = 44
CotType_a_u_A = 45
CotType_a_f_A_M_H_Q = 46
CotType_a_f_A_C_F = 47
CotType_a_f_A_C = 48
CotType_a_f_A_C_L = 49
CotType_a_f_A = 50
CotType_a_f_A_M_H_C = 51
CotType_a_n_A_M_F_F = 52
CotType_a_u_A_C_F = 53
CotType_a_f_G_U_C_F_T_A = 54
CotType_a_f_G_U_C_V_S = 55
CotType_a_f_G_U_C_R_X = 56
CotType_a_f_G_U_C_I_Z = 57
CotType_a_f_G_U_C_E_C_W = 58
CotType_a_f_G_U_C_I_L = 59
CotType_a_f_G_U_C_R_O = 60
CotType_a_f_G_U_C_R_V = 61
CotType_a_f_G_U_H = 62
CotType_a_f_G_U_U_M_S_E = 63
CotType_a_f_G_U_S_M_C = 64
CotType_a_f_G_E_S = 65
CotType_a_f_G_E = 66
CotType_a_f_G_E_V_C_U = 67
CotType_a_f_G_E_V_C_ps = 68
CotType_a_u_G_E_V = 69
CotType_a_f_S_N_N_R = 70
CotType_a_f_F_B = 71
CotType_b_m_p_s_p_loc = 72
CotType_b_i_v = 73
CotType_b_f_t_r = 74
CotType_b_f_t_a = 75
CotType_u_d_f_m = 76
CotType_u_d_p = 77
CotType_b_m_p_s_m = 78
CotType_b_m_p_c = 79
CotType_u_r_b_c_c = 80
CotType_u_r_b_bullseye = 81
CotType_a_f_G_E_V_A = 82
CotType_a_n_A = 83
CotType_a_u_G_U_C_F = 84
CotType_a_n_G_U_C_F = 85
CotType_a_h_G_U_C_F = 86
CotType_a_f_G_U_C_F = 87
CotType_a_u_G_I = 88
CotType_a_n_G_I = 89
CotType_a_h_G_I = 90
CotType_a_f_G_I = 91
CotType_a_u_G_E_X_M = 92
CotType_a_n_G_E_X_M = 93
CotType_a_h_G_E_X_M = 94
CotType_a_f_G_E_X_M = 95
CotType_a_u_S = 96
CotType_a_n_S = 97
CotType_a_h_S = 98
CotType_a_u_G_U_C_I_d = 99
CotType_a_n_G_U_C_I_d = 100
CotType_a_h_G_U_C_I_d = 101
CotType_a_f_G_U_C_I_d = 102
CotType_a_u_G_E_V_A_T = 103
CotType_a_n_G_E_V_A_T = 104
CotType_a_h_G_E_V_A_T = 105
CotType_a_f_G_E_V_A_T = 106
CotType_a_u_G_U_C_I = 107
CotType_a_n_G_U_C_I = 108
CotType_a_h_G_U_C_I = 109
CotType_a_n_G_E_V = 110
CotType_a_h_G_E_V = 111
CotType_a_f_G_E_V = 112
CotType_b_m_p_w_GOTO = 113
CotType_b_m_p_c_ip = 114
CotType_b_m_p_c_cp = 115
CotType_b_m_p_s_p_op = 116
CotType_u_d_v = 117
CotType_u_d_v_m = 118
CotType_u_d_c_e = 119
CotType_b_i_x_i = 120
CotType_b_t_f_d = 121
CotType_b_t_f_r = 122
CotType_b_a_o_c = 123
CotType_t_s = 124
CotType_m_t_t = 125
CotType_y = 126
GeoPointSource_Unspecified = 0
GeoPointSource_GPS = 1
GeoPointSource_USER = 2
GeoPointSource_NETWORK = 3
TAKPacket._F = ((1, 'is_compressed', 6, 0, None, None), (2, 'contact', 16, 4, Contact, None), (3, 'group', 16, 4, Group, None), (4, 'status', 16, 4, Status, None), (5, 'pli', 16, 4, PLI, 'payload_variant'), (6, 'chat', 16, 4, GeoChat, 'payload_variant'), (7, 'detail', 15, 4, None, 'payload_variant'), )
GeoChat._F = ((1, 'message', 14, 0, None, None), (2, 'to', 14, 4, None, None), (3, 'to_callsign', 14, 4, None, None), (4, 'receipt_for_uid', 14, 0, None, None), (5, 'receipt_type', 7, 0, None, None), (6, 'lang', 14, 4, None, None), (7, 'room_id', 14, 4, None, None), (8, 'voice_profile_id', 14, 4, None, None), )
Group._F = ((1, 'role', 7, 0, None, None), (2, 'team', 7, 0, None, None), )
Status._F = ((1, 'battery', 2, 0, None, None), )
Contact._F = ((1, 'callsign', 14, 0, None, None), (2, 'device_callsign', 14, 0, None, None), )
PLI._F = ((1, 'latitude_i', 9, 0, None, None), (2, 'longitude_i', 9, 0, None, None), (3, 'altitude', 0, 0, None, None), (4, 'speed', 2, 0, None, None), (5, 'course', 2, 0, None, None), )
AircraftTrack._F = ((1, 'icao', 14, 0, None, None), (2, 'registration', 14, 0, None, None), (3, 'flight', 14, 0, None, None), (4, 'aircraft_type', 14, 0, None, None), (5, 'squawk', 2, 0, None, None), (6, 'category', 14, 0, None, None), (7, 'rssi_x10', 4, 0, None, None), (8, 'gps', 6, 0, None, None), (9, 'cot_host_id', 14, 0, None, None), )
CotGeoPoint._F = ((1, 'lat_delta_i', 4, 0, None, None), (2, 'lon_delta_i', 4, 0, None, None), )
DrawnShape._F = ((1, 'kind', 7, 0, None, None), (2, 'style', 7, 0, None, None), (3, 'major_cm', 2, 0, None, None), (4, 'minor_cm', 2, 0, None, None), (5, 'angle_deg', 2, 0, None, None), (6, 'stroke_color', 7, 0, None, None), (7, 'stroke_argb', 8, 0, None, None), (8, 'stroke_weight_x10', 2, 0, None, None), (9, 'fill_color', 7, 0, None, None), (10, 'fill_argb', 8, 0, None, None), (11, 'labels_on', 6, 0, None, None), (13, 'truncated', 6, 0, None, None), (14, 'bullseye_distance_dm', 2, 0, None, None), (15, 'bullseye_bearing_ref', 2, 0, None, None), (16, 'bullseye_flags', 2, 0, None, None), (17, 'bullseye_uid_ref', 14, 0, None, None), (18, 'vertex_lat_deltas', 4, 3, None, None), (19, 'vertex_lon_deltas', 4, 3, None, None), )
Marker._F = ((1, 'kind', 7, 0, None, None), (2, 'color', 7, 0, None, None), (3, 'color_argb', 8, 0, None, None), (4, 'readiness', 6, 0, None, None), (5, 'parent_uid', 14, 0, None, None), (6, 'parent_type', 14, 0, None, None), (7, 'parent_callsign', 14, 0, None, None), (8, 'iconset', 14, 0, None, None), )
RangeAndBearing._F = ((1, 'anchor', 16, 4, CotGeoPoint, None), (2, 'anchor_uid', 14, 0, None, None), (3, 'range_cm', 2, 0, None, None), (4, 'bearing_cdeg', 2, 0, None, None), (5, 'stroke_color', 7, 0, None, None), (6, 'stroke_argb', 8, 0, None, None), (7, 'stroke_weight_x10', 2, 0, None, None), )
Route.Link._F = ((1, 'point', 16, 4, CotGeoPoint, None), (2, 'uid', 14, 0, None, None), (3, 'callsign', 14, 0, None, None), (4, 'link_type', 2, 0, None, None), )
Route._F = ((1, 'method', 7, 0, None, None), (2, 'direction', 7, 0, None, None), (3, 'prefix', 14, 0, None, None), (4, 'stroke_weight_x10', 2, 0, None, None), (5, 'links', 16, 1, Route.Link, None), (6, 'truncated', 6, 0, None, None), )
CasevacReport._F = ((1, 'precedence', 7, 0, None, None), (2, 'equipment_flags', 2, 0, None, None), (3, 'litter_patients', 2, 0, None, None), (4, 'ambulatory_patients', 2, 0, None, None), (5, 'security', 7, 0, None, None), (6, 'hlz_marking', 7, 0, None, None), (7, 'zone_marker', 14, 0, None, None), (8, 'us_military', 2, 0, None, None), (9, 'us_civilian', 2, 0, None, None), (10, 'non_us_military', 2, 0, None, None), (11, 'non_us_civilian', 2, 0, None, None), (12, 'epw', 2, 0, None, None), (13, 'child', 2, 0, None, None), (14, 'terrain_flags', 2, 0, None, None), (15, 'frequency', 14, 0, None, None), (16, 'title', 14, 0, None, None), (17, 'medline_remarks', 14, 0, None, None), (18, 'urgent_count', 2, 0, None, None), (19, 'urgent_surgical_count', 2, 0, None, None), (20, 'priority_count', 2, 0, None, None), (21, 'routine_count', 2, 0, None, None), (22, 'convenience_count', 2, 0, None, None), (23, 'equipment_detail', 14, 0, None, None), (24, 'zone_protected_coord', 14, 0, None, None), (25, 'terrain_slope_dir', 14, 0, None, None), (26, 'terrain_other_detail', 14, 0, None, None), (27, 'marked_by', 14, 0, None, None), (28, 'obstacles', 14, 0, None, None), (29, 'winds_are_from', 14, 0, None, None), (30, 'friendlies', 14, 0, None, None), (31, 'enemy', 14, 0, None, None), (32, 'hlz_remarks', 14, 0, None, None), (33, 'zmist', 16, 1, ZMistEntry, None), )
ZMistEntry._F = ((1, 'title', 14, 0, None, None), (2, 'z', 14, 0, None, None), (3, 'm', 14, 0, None, None), (4, 'i', 14, 0, None, None), (5, 's', 14, 0, None, None), (6, 't', 14, 0, None, None), )
EmergencyAlert._F = ((1, 'type', 7, 0, None, None), (2, 'authoring_uid', 14, 0, None, None), (3, 'cancel_reference_uid', 14, 0, None, None), )
TaskRequest._F = ((1, 'task_type', 14, 0, None, None), (2, 'target_uid', 14, 0, None, None), (3, 'assignee_uid', 14, 0, None, None), (4, 'priority', 7, 0, None, None), (5, 'status', 7, 0, None, None), (6, 'note', 14, 0, None, None), )
TAKEnvironment._F = ((1, 'temperature_c_x10', 4, 0, None, None), (2, 'wind_direction_deg', 2, 0, None, None), (3, 'wind_speed_cm_s', 2, 0, None, None), )
SensorFov._F = ((1, 'type', 7, 0, None, None), (2, 'azimuth_deg', 2, 0, None, None), (3, 'range_m', 2, 4, None, None), (4, 'fov_horizontal_deg', 2, 0, None, None), (5, 'fov_vertical_deg', 2, 0, None, None), (6, 'elevation_deg', 4, 0, None, None), (7, 'roll_deg', 4, 0, None, None), (8, 'model', 14, 0, None, None), )
TakTalkMessage._F = ((1, 'text', 14, 0, None, None), (2, 'chatroom_id', 14, 0, None, None), (3, 'lang', 14, 0, None, None), (4, 'from_voice', 6, 0, None, None), )
TakTalkRoomData._F = ((1, 'sender_callsign', 14, 0, None, None), (2, 'room_id', 14, 0, None, None), (3, 'room_name', 14, 0, None, None), (4, 'participants', 14, 1, None, None), )
Marti._F = ((1, 'dest_callsign', 14, 1, None, None), )
TAKPacketV2._F = ((1, 'cot_type_id', 7, 0, None, None), (2, 'how', 7, 0, None, None), (3, 'callsign', 14, 0, None, None), (4, 'team', 7, 0, None, None), (5, 'role', 7, 0, None, None), (6, 'latitude_i', 9, 0, None, None), (7, 'longitude_i', 9, 0, None, None), (8, 'altitude', 4, 0, None, None), (9, 'speed', 2, 0, None, None), (10, 'course', 2, 0, None, None), (11, 'battery', 2, 0, None, None), (12, 'geo_src', 7, 0, None, None), (13, 'alt_src', 7, 0, None, None), (14, 'uid', 14, 0, None, None), (15, 'device_callsign', 14, 0, None, None), (16, 'stale_seconds', 2, 0, None, None), (17, 'tak_version', 14, 0, None, None), (18, 'tak_device', 14, 0, None, None), (19, 'tak_platform', 14, 0, None, None), (20, 'tak_os', 14, 0, None, None), (21, 'endpoint', 14, 0, None, None), (22, 'phone', 14, 0, None, None), (23, 'cot_type_str', 14, 0, None, None), (24, 'remarks', 14, 0, None, None), (25, 'environment', 16, 4, TAKEnvironment, None), (26, 'sensor_fov', 16, 4, SensorFov, None), (29, 'marti', 16, 4, Marti, None), (31, 'chat', 16, 4, GeoChat, 'payload_variant'), (32, 'aircraft', 16, 4, AircraftTrack, 'payload_variant'), (33, 'raw_detail', 15, 4, None, 'payload_variant'), (34, 'shape', 16, 4, DrawnShape, 'payload_variant'), (35, 'marker', 16, 4, Marker, 'payload_variant'), (36, 'rab', 16, 4, RangeAndBearing, 'payload_variant'), (37, 'route', 16, 4, Route, 'payload_variant'), (38, 'casevac', 16, 4, CasevacReport, 'payload_variant'), (39, 'emergency', 16, 4, EmergencyAlert, 'payload_variant'), (40, 'task', 16, 4, TaskRequest, 'payload_variant'), (41, 'taktalk', 16, 4, TakTalkMessage, 'payload_variant'), (42, 'taktalk_room', 16, 4, TakTalkRoomData, 'payload_variant'), (43, 'start_epoch_lo14', 2, 4, None, None), )
