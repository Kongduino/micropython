# The Amigo's touch screen: FT6X36 (FocalTech) on the internal I2C bus, 0x38.
#
#   from touch import Touch
#   touch = Touch()          # the same rotation as lcd.LCD's
#   point = touch.read()     # (x, y) in screen pixels, or None
#
# The driver is the Meshtastic K210 port's (from the Maix_Amigo repository's).

import time
from machine import I2C

_ADDR = const(0x38)
_REG_TD_STATUS = const(0x02)
_REG_TH_GROUP = const(0x80)
_EVENT_DOWN = const(0)
_PANEL_SHORT = const(320)  # raw coordinates are the panel's, portrait
_PANEL_LONG = const(480)
_STALE_MS = const(200)


class Touch:
    def __init__(self, i2c=None, rotation=0, threshold=12):
        # threshold: lower is more sensitive (12 is MaixPy's)
        self.i2c = i2c or I2C(0)
        self.rotation = rotation & 3
        self.buf = bytearray(13)
        self.touching = False
        self.skip_stale = False
        self.start = 0
        self.last = None
        self.i2c.writeto_mem(_ADDR, _REG_TH_GROUP, bytes((threshold,)))

    def read(self):
        # TD_STATUS and both 6-byte point records: the whole frame, as reading
        # only the first point leaves the chip reporting the same, stale one
        buf = self.buf
        try:
            self.i2c.readfrom_mem_into(_ADDR, _REG_TD_STATUS, buf)
        except OSError:
            return None
        n = buf[0] & 0x0F
        if n == 0 or n > 2:
            self.touching = False
            return None
        col = ((buf[1] & 0x0F) << 8) | buf[2]
        row = ((buf[3] & 0x0F) << 8) | buf[4]
        # At the start of a touch, the chip can report the previous touch's
        # last point for up to ~100 ms before the real one: that point only is
        # held back, and only briefly
        if not self.touching:
            self.touching = True
            self.start = time.ticks_ms()
            self.skip_stale = (buf[1] >> 6) != _EVENT_DOWN
        if self.skip_stale:
            if (col, row) == self.last and time.ticks_diff(time.ticks_ms(), self.start) < _STALE_MS:
                return None
            self.skip_stale = False
        if col >= _PANEL_SHORT or row >= _PANEL_LONG:
            return None
        self.last = (col, row)
        r = self.rotation
        if r == 0:  # landscape, camera on the left
            return row, _PANEL_SHORT - 1 - col
        if r == 1:  # portrait, camera at the top
            return col, row
        if r == 2:
            return _PANEL_LONG - 1 - row, col
        return _PANEL_SHORT - 1 - col, _PANEL_LONG - 1 - row
