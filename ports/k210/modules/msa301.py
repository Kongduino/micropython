# The Amigo's accelerometer: MSA301 (MEMSensing) on the internal I2C bus,
# 0x26.
#
#   from msa301 import MSA301
#   acc = MSA301()
#   acc.acceleration()       # (x, y, z) in g
#   acc.rotation()           # the lcd.LCD rotation the Amigo is held in
#
# Registers as in Adafruit's driver (MaixPy's msa301.py); set up as the
# Meshtastic K210 port does.

from machine import I2C

_ADDR = const(0x26)
_REG_PARTID = const(0x01)
_REG_OUT_X_L = const(0x02)
_REG_RESRANGE = const(0x0F)
_REG_ODR = const(0x10)
_REG_POWERMODE = const(0x11)
_PARTID = const(0x13)
_ONE_G = const(4096)  # 14 bits, +-2 g


class MSA301:
    def __init__(self, i2c=None):
        self.i2c = i2c or I2C(0)
        if self.i2c.readfrom_mem(_ADDR, _REG_PARTID, 1)[0] != _PARTID:
            raise OSError("no MSA301")
        self.buf = bytearray(6)
        self.i2c.writeto_mem(_ADDR, _REG_RESRANGE, b"\x00")  # +-2 g, 14 bits
        self.i2c.writeto_mem(_ADDR, _REG_ODR, b"\x06")  # 62.5 Hz, all axes
        self.i2c.writeto_mem(_ADDR, _REG_POWERMODE, b"\x00")  # normal (it starts suspended)

    def raw(self):
        # 14-bit values, left-aligned in little-endian 16-bit words
        b = self.buf
        self.i2c.readfrom_mem_into(_ADDR, _REG_OUT_X_L, b)
        out = []
        for i in (0, 2, 4):
            v = b[i] | (b[i + 1] << 8)
            if v & 0x8000:
                v -= 0x10000
            out.append(v >> 2)
        return tuple(out)

    def acceleration(self):
        x, y, z = self.raw()
        return x / _ONE_G, y / _ONE_G, z / _ONE_G

    def rotation(self):
        # The lcd.LCD rotation that shows the picture upright as the Amigo is
        # held, or None when it lies (nearly) flat. Y runs along the screen's
        # short side, X along its long side.
        x, y, z = self.raw()
        if max(abs(x), abs(y)) < _ONE_G // 2:
            return None
        if abs(y) >= abs(x):
            return 0 if y > 0 else 2
        return 3 if x < 0 else 1
