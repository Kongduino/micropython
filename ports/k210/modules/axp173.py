# The Amigo's power chip: AXP173 (X-Powers) on the internal I2C bus, 0x34.
#
#   from axp173 import AXP173
#   pmu = AXP173()
#   pmu.battery_voltage()    # mV
#   pmu.battery_level()      # %, estimated from the voltage
#   pmu.charging()
#   pmu.usb_voltage()        # mV (the Amigo's USB power is the chip's ACIN)
#
# Registers as the Meshtastic K210 port reads them, and the ADC registers of
# the AXP192 family. Writes go one register at a time: the chip takes a
# multi-byte write as register and value pairs.

from machine import I2C

_ADDR = const(0x34)
_REG_POWER_STATUS = const(0x00)  # bit 7 ACIN present, bit 5 VBUS present
_REG_CHARGE_STATUS = const(0x01)  # bit 6 charging, bit 5 battery present
_REG_ACIN_VOLTAGE = const(0x56)  # 12 bits, 1.7 mV per step
_REG_ACIN_CURRENT = const(0x58)  # 12 bits, 0.625 mA per step
_REG_VBUS_VOLTAGE = const(0x5A)  # 12 bits, 1.7 mV per step
_REG_VBUS_CURRENT = const(0x5C)  # 12 bits, 0.375 mA per step
_REG_TEMPERATURE = const(0x5E)  # 12 bits, 0.1 C per step from -144.7 C
_REG_BATT_VOLTAGE = const(0x78)  # 12 bits, 1.1 mV per step
_REG_CHARGE_CURRENT = const(0x7A)  # 13 bits, 0.5 mA per step
_REG_DISCHARGE_CURRENT = const(0x7C)  # 13 bits, 0.5 mA per step
_REG_ADC_ENABLE_1 = const(0x82)
_REG_ADC_ENABLE_2 = const(0x83)

# A LiPo cell's open-circuit voltage at 100%, 90% ... 0% (Meshtastic's table)
_OCV = (4190, 4050, 3990, 3890, 3800, 3720, 3630, 3530, 3420, 3300, 3100)


class AXP173:
    def __init__(self, i2c=None):
        self.i2c = i2c or I2C(0)
        self.buf1 = bytearray(1)
        self.buf2 = bytearray(2)
        # ADCs on: battery, ACIN and VBUS voltage and current, and the
        # internal temperature
        self._write(_REG_ADC_ENABLE_1, self._read(_REG_ADC_ENABLE_1) | 0xFC)
        self._write(_REG_ADC_ENABLE_2, self._read(_REG_ADC_ENABLE_2) | 0x80)

    def _read(self, reg):
        self.i2c.readfrom_mem_into(_ADDR, reg, self.buf1)
        return self.buf1[0]

    def _write(self, reg, value):
        self.buf1[0] = value
        self.i2c.writeto_mem(_ADDR, reg, self.buf1)

    def _adc12(self, reg):
        b = self.buf2
        self.i2c.readfrom_mem_into(_ADDR, reg, b)
        return (b[0] << 4) | (b[1] & 0x0F)

    def _adc13(self, reg):
        b = self.buf2
        self.i2c.readfrom_mem_into(_ADDR, reg, b)
        return (b[0] << 5) | (b[1] & 0x1F)

    def battery_present(self):
        return bool(self._read(_REG_CHARGE_STATUS) & 0x20)

    def charging(self):
        return bool(self._read(_REG_CHARGE_STATUS) & 0x40)

    def usb_present(self):
        # external power, on ACIN (the Amigo's USB) or VBUS
        return bool(self._read(_REG_POWER_STATUS) & 0xA0)

    def battery_voltage(self):
        # mV
        return self._adc12(_REG_BATT_VOLTAGE) * 11 // 10

    def battery_current(self):
        # mA: positive charging, negative discharging
        return (self._adc13(_REG_CHARGE_CURRENT) - self._adc13(_REG_DISCHARGE_CURRENT)) // 2

    def battery_level(self):
        # %, from the voltage: rough while charging or under load
        if not self.battery_present():
            return None
        mv = self.battery_voltage()
        if mv >= _OCV[0]:
            return 100
        for i in range(1, len(_OCV)):
            if mv >= _OCV[i]:
                hi, lo = _OCV[i - 1], _OCV[i]
                return (10 - i) * 10 + (mv - lo) * 10 // (hi - lo)
        return 0

    def _acin(self):
        return bool(self._read(_REG_POWER_STATUS) & 0x80)

    def usb_voltage(self):
        # mV, of ACIN or else VBUS
        if self._acin():
            return self._adc12(_REG_ACIN_VOLTAGE) * 17 // 10
        return self._adc12(_REG_VBUS_VOLTAGE) * 17 // 10

    def usb_current(self):
        # mA, drawn from ACIN or else VBUS
        if self._acin():
            return self._adc12(_REG_ACIN_CURRENT) * 5 // 8
        return self._adc12(_REG_VBUS_CURRENT) * 3 // 8

    def temperature(self):
        # the chip's, in C
        return self._adc12(_REG_TEMPERATURE) / 10 - 144.7
