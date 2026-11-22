# Generated from meshtastic/telemetry.proto by gen_mp_protobuf.py, for protobuf.py: do not edit.
from protobuf import Message, Enum

class TelemetrySensorType(Enum):
    _V = (('SENSOR_UNSET', 0), ('BME280', 1), ('BME680', 2), ('MCP9808', 3), ('INA260', 4), ('INA219', 5), ('BMP280', 6), ('SHTC3', 7), ('LPS22', 8), ('QMC6310', 9), ('QMI8658', 10), ('QMC5883L', 11), ('SHT31', 12), ('PMSA003I', 13), ('INA3221', 14), ('BMP085', 15), ('RCWL9620', 16), ('SHT4X', 17), ('VEML7700', 18), ('MLX90632', 19), ('OPT3001', 20), ('LTR390UV', 21), ('TSL25911FN', 22), ('AHT10', 23), ('DFROBOT_LARK', 24), ('NAU7802', 25), ('BMP3XX', 26), ('ICM20948', 27), ('MAX17048', 28), ('CUSTOM_SENSOR', 29), ('MAX30102', 30), ('MLX90614', 31), ('SCD4X', 32), ('RADSENS', 33), ('INA226', 34), ('DFROBOT_RAIN', 35), ('DPS310', 36), ('RAK12035', 37), ('MAX17261', 38), ('PCT2075', 39), ('ADS1X15', 40), ('ADS1X15_ALT', 41), ('SFA30', 42), ('SEN5X', 43), ('TSL2561', 44), ('BH1750', 45), ('HDC1080', 46), ('SHT21', 47), ('STC31', 48), ('SCD30', 49), ('SHTXX', 50), ('DS248X', 51), ('MMC5983MA', 52), ('ICM42607P', 53), ('SPA06', 54), ('HM330X', 55), ('SEN6X', 56), ('AS3935', 57), )
    SENSOR_UNSET = 0
    BME280 = 1
    BME680 = 2
    MCP9808 = 3
    INA260 = 4
    INA219 = 5
    BMP280 = 6
    SHTC3 = 7
    LPS22 = 8
    QMC6310 = 9
    QMI8658 = 10
    QMC5883L = 11
    SHT31 = 12
    PMSA003I = 13
    INA3221 = 14
    BMP085 = 15
    RCWL9620 = 16
    SHT4X = 17
    VEML7700 = 18
    MLX90632 = 19
    OPT3001 = 20
    LTR390UV = 21
    TSL25911FN = 22
    AHT10 = 23
    DFROBOT_LARK = 24
    NAU7802 = 25
    BMP3XX = 26
    ICM20948 = 27
    MAX17048 = 28
    CUSTOM_SENSOR = 29
    MAX30102 = 30
    MLX90614 = 31
    SCD4X = 32
    RADSENS = 33
    INA226 = 34
    DFROBOT_RAIN = 35
    DPS310 = 36
    RAK12035 = 37
    MAX17261 = 38
    PCT2075 = 39
    ADS1X15 = 40
    ADS1X15_ALT = 41
    SFA30 = 42
    SEN5X = 43
    TSL2561 = 44
    BH1750 = 45
    HDC1080 = 46
    SHT21 = 47
    STC31 = 48
    SCD30 = 49
    SHTXX = 50
    DS248X = 51
    MMC5983MA = 52
    ICM42607P = 53
    SPA06 = 54
    HM330X = 55
    SEN6X = 56
    AS3935 = 57

class DeviceMetrics(Message):
    pass

class EnvironmentMetrics(Message):
    pass

class SoilWaterMetrics(Message):
    pass

class PowerMetrics(Message):
    pass

class AirQualityMetrics(Message):
    pass

class LocalStats(Message):
    pass

class TrafficManagementStats(Message):
    pass

class HealthMetrics(Message):
    pass

class HostMetrics(Message):
    pass

class Telemetry(Message):
    pass

class Nau7802Config(Message):
    pass

class AS3935State(Message):
    pass

class SEN5XState(Message):
    pass

class SEN6XState(Message):
    pass

SENSOR_UNSET = 0
BME280 = 1
BME680 = 2
MCP9808 = 3
INA260 = 4
INA219 = 5
BMP280 = 6
SHTC3 = 7
LPS22 = 8
QMC6310 = 9
QMI8658 = 10
QMC5883L = 11
SHT31 = 12
PMSA003I = 13
INA3221 = 14
BMP085 = 15
RCWL9620 = 16
SHT4X = 17
VEML7700 = 18
MLX90632 = 19
OPT3001 = 20
LTR390UV = 21
TSL25911FN = 22
AHT10 = 23
DFROBOT_LARK = 24
NAU7802 = 25
BMP3XX = 26
ICM20948 = 27
MAX17048 = 28
CUSTOM_SENSOR = 29
MAX30102 = 30
MLX90614 = 31
SCD4X = 32
RADSENS = 33
INA226 = 34
DFROBOT_RAIN = 35
DPS310 = 36
RAK12035 = 37
MAX17261 = 38
PCT2075 = 39
ADS1X15 = 40
ADS1X15_ALT = 41
SFA30 = 42
SEN5X = 43
TSL2561 = 44
BH1750 = 45
HDC1080 = 46
SHT21 = 47
STC31 = 48
SCD30 = 49
SHTXX = 50
DS248X = 51
MMC5983MA = 52
ICM42607P = 53
SPA06 = 54
HM330X = 55
SEN6X = 56
AS3935 = 57
DeviceMetrics._F = ((1, 'battery_level', 2, 4, None, None), (2, 'voltage', 10, 4, None, None), (3, 'channel_utilization', 10, 4, None, None), (4, 'air_util_tx', 10, 4, None, None), (5, 'uptime_seconds', 2, 4, None, None), )
EnvironmentMetrics._F = ((1, 'temperature', 10, 4, None, None), (2, 'relative_humidity', 10, 4, None, None), (3, 'barometric_pressure', 10, 4, None, None), (4, 'gas_resistance', 10, 4, None, None), (5, 'voltage', 10, 4, None, None), (6, 'current', 10, 4, None, None), (7, 'iaq', 2, 4, None, None), (8, 'distance', 10, 4, None, None), (9, 'lux', 10, 4, None, None), (10, 'white_lux', 10, 4, None, None), (11, 'ir_lux', 10, 4, None, None), (12, 'uv_lux', 10, 4, None, None), (13, 'wind_direction', 2, 4, None, None), (14, 'wind_speed', 10, 4, None, None), (15, 'weight', 10, 4, None, None), (16, 'wind_gust', 10, 4, None, None), (17, 'wind_lull', 10, 4, None, None), (18, 'radiation', 10, 4, None, None), (19, 'rainfall_1h', 10, 4, None, None), (20, 'rainfall_24h', 10, 4, None, None), (21, 'soil_moisture', 2, 4, None, None), (22, 'soil_temperature', 10, 4, None, None), (23, 'one_wire_temperature', 10, 3, None, None), (24, 'adc_voltage_ch0', 10, 4, None, None), (25, 'adc_voltage_ch1', 10, 4, None, None), (26, 'adc_voltage_ch2', 10, 4, None, None), (27, 'adc_voltage_ch3', 10, 4, None, None), (28, 'adc_voltage_ch4', 10, 4, None, None), (29, 'adc_voltage_ch5', 10, 4, None, None), (30, 'adc_voltage_ch6', 10, 4, None, None), (31, 'adc_voltage_ch7', 10, 4, None, None), (32, 'one_wire_temperature_ch0', 10, 4, None, None), (33, 'one_wire_temperature_ch1', 10, 4, None, None), (34, 'one_wire_temperature_ch2', 10, 4, None, None), (35, 'one_wire_temperature_ch3', 10, 4, None, None), (36, 'one_wire_temperature_ch4', 10, 4, None, None), (37, 'one_wire_temperature_ch5', 10, 4, None, None), (38, 'one_wire_temperature_ch6', 10, 4, None, None), (39, 'one_wire_temperature_ch7', 10, 4, None, None), (40, 'lightning_strike_count_1h', 2, 4, None, None), (41, 'lightning_distance_km', 10, 4, None, None), )
SoilWaterMetrics._F = ((1, 'soil_ph', 10, 4, None, None), (2, 'ph', 10, 4, None, None), (3, 'electrical_conductivity', 10, 4, None, None), (4, 'salinity', 10, 4, None, None), (5, 'nitrogen', 10, 4, None, None), (6, 'phosphorus', 10, 4, None, None), (7, 'potassium', 10, 4, None, None), (8, 'dissolved_oxygen', 10, 4, None, None), (9, 'orp', 10, 4, None, None), (10, 'chemical_oxygen_demand', 10, 4, None, None), (11, 'turbidity', 10, 4, None, None), (12, 'nitrate', 10, 4, None, None), (13, 'ammonium', 10, 4, None, None), (14, 'biochemical_oxygen_demand', 10, 4, None, None), (15, 'solar_irradiance', 10, 4, None, None), )
PowerMetrics._F = ((1, 'ch1_voltage', 10, 4, None, None), (2, 'ch1_current', 10, 4, None, None), (3, 'ch2_voltage', 10, 4, None, None), (4, 'ch2_current', 10, 4, None, None), (5, 'ch3_voltage', 10, 4, None, None), (6, 'ch3_current', 10, 4, None, None), (7, 'ch4_voltage', 10, 4, None, None), (8, 'ch4_current', 10, 4, None, None), (9, 'ch5_voltage', 10, 4, None, None), (10, 'ch5_current', 10, 4, None, None), (11, 'ch6_voltage', 10, 4, None, None), (12, 'ch6_current', 10, 4, None, None), (13, 'ch7_voltage', 10, 4, None, None), (14, 'ch7_current', 10, 4, None, None), (15, 'ch8_voltage', 10, 4, None, None), (16, 'ch8_current', 10, 4, None, None), )
AirQualityMetrics._F = ((1, 'pm10_standard', 2, 4, None, None), (2, 'pm25_standard', 2, 4, None, None), (3, 'pm100_standard', 2, 4, None, None), (4, 'pm10_environmental', 2, 4, None, None), (5, 'pm25_environmental', 2, 4, None, None), (6, 'pm100_environmental', 2, 4, None, None), (7, 'particles_03um', 2, 4, None, None), (8, 'particles_05um', 2, 4, None, None), (9, 'particles_10um', 2, 4, None, None), (10, 'particles_25um', 2, 4, None, None), (11, 'particles_50um', 2, 4, None, None), (12, 'particles_100um', 2, 4, None, None), (13, 'co2', 2, 4, None, None), (14, 'co2_temperature', 10, 4, None, None), (15, 'co2_humidity', 10, 4, None, None), (16, 'form_formaldehyde', 10, 4, None, None), (17, 'form_humidity', 10, 4, None, None), (18, 'form_temperature', 10, 4, None, None), (19, 'pm40_standard', 2, 4, None, None), (20, 'particles_40um', 2, 4, None, None), (21, 'pm_temperature', 10, 4, None, None), (22, 'pm_humidity', 10, 4, None, None), (23, 'pm_voc_idx', 10, 4, None, None), (24, 'pm_nox_idx', 10, 4, None, None), (25, 'particles_tps', 10, 4, None, None), (26, 'pm_status_flags', 2, 4, None, None), )
LocalStats._F = ((1, 'uptime_seconds', 2, 0, None, None), (2, 'channel_utilization', 10, 0, None, None), (3, 'air_util_tx', 10, 0, None, None), (4, 'num_packets_tx', 2, 0, None, None), (5, 'num_packets_rx', 2, 0, None, None), (6, 'num_packets_rx_bad', 2, 0, None, None), (7, 'num_online_nodes', 2, 0, None, None), (8, 'num_total_nodes', 2, 0, None, None), (9, 'num_rx_dupe', 2, 0, None, None), (10, 'num_tx_relay', 2, 0, None, None), (11, 'num_tx_relay_canceled', 2, 0, None, None), (12, 'heap_total_bytes', 2, 0, None, None), (13, 'heap_free_bytes', 2, 0, None, None), (14, 'num_tx_dropped', 2, 0, None, None), (15, 'noise_floor', 0, 0, None, None), )
TrafficManagementStats._F = ((1, 'packets_inspected', 2, 0, None, None), (2, 'position_dedup_drops', 2, 0, None, None), (3, 'nodeinfo_cache_hits', 2, 0, None, None), (4, 'rate_limit_drops', 2, 0, None, None), (5, 'unknown_packet_drops', 2, 0, None, None), (6, 'hop_exhausted_packets', 2, 0, None, None), (7, 'router_hops_preserved', 2, 0, None, None), )
HealthMetrics._F = ((1, 'heart_bpm', 2, 4, None, None), (2, 'spO2', 2, 4, None, None), (3, 'temperature', 10, 4, None, None), )
HostMetrics._F = ((1, 'uptime_seconds', 2, 0, None, None), (2, 'freemem_bytes', 3, 0, None, None), (3, 'diskfree1_bytes', 3, 0, None, None), (4, 'diskfree2_bytes', 3, 4, None, None), (5, 'diskfree3_bytes', 3, 4, None, None), (6, 'load1', 2, 0, None, None), (7, 'load5', 2, 0, None, None), (8, 'load15', 2, 0, None, None), (9, 'user_string', 14, 4, None, None), )
Telemetry._F = ((1, 'time', 8, 0, None, None), (2, 'device_metrics', 16, 4, DeviceMetrics, 'variant'), (3, 'environment_metrics', 16, 4, EnvironmentMetrics, 'variant'), (4, 'air_quality_metrics', 16, 4, AirQualityMetrics, 'variant'), (5, 'power_metrics', 16, 4, PowerMetrics, 'variant'), (6, 'local_stats', 16, 4, LocalStats, 'variant'), (7, 'health_metrics', 16, 4, HealthMetrics, 'variant'), (8, 'host_metrics', 16, 4, HostMetrics, 'variant'), (9, 'traffic_management_stats', 16, 4, TrafficManagementStats, 'variant'), (11, 'soil_water_metrics', 16, 4, SoilWaterMetrics, 'variant'), )
Nau7802Config._F = ((1, 'zeroOffset', 0, 0, None, None), (2, 'calibrationFactor', 10, 0, None, None), )
AS3935State._F = ((1, 'tuning_cap_pf', 2, 0, None, None), )
SEN5XState._F = ((1, 'last_cleaning_time', 2, 0, None, None), (2, 'last_cleaning_valid', 6, 0, None, None), (3, 'one_shot_mode', 6, 0, None, None), (4, 'voc_state_time', 2, 4, None, None), (5, 'voc_state_valid', 6, 4, None, None), (6, 'voc_state_array', 11, 4, None, None), )
SEN6XState._F = ((1, 'last_cleaning_time', 2, 0, None, None), (2, 'last_cleaning_valid', 6, 0, None, None), (3, 'one_shot_mode', 6, 0, None, None), (4, 'voc_state_time', 2, 4, None, None), (5, 'voc_state_valid', 6, 4, None, None), (6, 'voc_state_array', 11, 4, None, None), )
