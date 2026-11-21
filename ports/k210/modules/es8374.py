# The Amigo's audio codec: ES8374 (Everest) on the internal I2C bus, 0x10,
# with its I2S on IO13 (MCK), IO21 (SCK), IO18 (WS), IO34 (to the codec) and
# IO35 (from it). It plays on the speaker (class D) and records from the
# microphone; machine.I2S carries the samples, 16-bit, MCK 256 times the
# rate (machine.I2S on the K210 sets it so).
#
#   from es8374 import ES8374
#   from machine import I2S
#   codec = ES8374()
#   codec.volume(70)                  # %, 0 is muted
#   out = I2S(0, mode=I2S.TX, rate=16000, bits=16, format=I2S.MONO,
#             ibuf=8192, **ES8374.TX_PINS)
#   out.write(samples)
#   mic = I2S(0, mode=I2S.RX, ..., **ES8374.RX_PINS)
#
# The register settings are those MaixPy's es8374.py (MaixPy_scripts, MIT
# licence) makes: the codec as I2S target, 16-bit samples, MCK / 256 the
# sample rate, SCK MCK / 4, the speaker and the microphone (PGA +18 dB) on.

import time
from machine import I2C

_ADDR = const(0x10)


class ES8374:
    TX_PINS = {"mck": 13, "sck": 21, "ws": 18, "sd": 34}
    RX_PINS = {"mck": 13, "sck": 21, "ws": 18, "sd": 35}

    def __init__(self, i2c=None):
        self.i2c = i2c or I2C(0)
        self.buf = bytearray(1)
        if _ADDR not in self.i2c.scan():
            raise OSError("no ES8374")
        w, m = self._write, self._modify
        # Stopped, muted
        m(0x36, 0xFF, 0x20)
        m(0x1A, 0xFF, 0x08)
        m(0x1A, 0xDF, 0)
        w(0x1D, 0x12)
        w(0x1E, 0x20)
        m(0x15, 0xFF, 0x20)
        m(0x10, 0xFF, 0xC0)
        m(0x21, 0xFF, 0xC0)
        # Reset, clocks on, target (slave) mode (the chip doesn't answer for
        # a moment after the reset)
        w(0x00, 0x3F)
        time.sleep_ms(5)
        w(0x00, 0x03)
        time.sleep_ms(5)
        w(0x01, 0x7F)
        m(0x0F, 0x7F, 0)
        # The codec's PLL
        for reg, value in ((0x6F, 0xA0), (0x72, 0x41), (0x09, 0x01), (0x0C, 0x08), (0x0D, 0x13),
                           (0x0E, 0xE0), (0x0A, 0x8A), (0x0B, 0x08), (0x09, 0x41)):
            w(reg, value)
        # SCK = MCK / 4, LRCK = MCK / 256
        m(0x0F, 0xE0, 0x04)
        w(0x06, 0x01)
        w(0x07, 0x00)
        w(0x24, 0x08)
        w(0x36, 0x00)
        w(0x12, 0x30)
        w(0x13, 0x20)
        # I2S format, 16 bits, ADC and DAC
        m(0x10, 0xE0, 0x0C)
        m(0x11, 0xE0, 0x0C)
        # Microphone input and PGA, class D divider, start
        for reg, value in ((0x21, 0x50), (0x22, 0xFF), (0x21, 0x14), (0x22, 0x55), (0x08, 0x21),
                           (0x00, 0x80), (0x25, 0x00), (0x38, 0x00),
                           (0x14, 0x8A), (0x15, 0x40), (0x1A, 0xA0), (0x1B, 0x19), (0x1C, 0x90),
                           (0x1D, 0x01), (0x1F, 0x00), (0x1E, 0x20), (0x28, 0x70), (0x26, 0x4E),
                           (0x27, 0x10), (0x29, 0x00), (0x2B, 0x00), (0x25, 0x00), (0x38, 0x00),
                           (0x37, 0x30), (0x6D, 0x60), (0x71, 0x05), (0x73, 0x70)):
            w(reg, value)
        # The speaker
        w(0x1D, 0x02)
        m(0x1C, 0xFF, 0x80)
        w(0x1D, 0x02)
        w(0x1F, 0x00)
        w(0x1E, 0xA0)
        # The microphone, +18 dB, D2SE PGA on
        m(0x21, 0xCF, 0x14)
        w(0x21, 0x24)
        w(0x38, 0xC0)
        w(0x37, 0x00)
        w(0x22, 0x66)
        m(0x21, 0xFB, 0x04)
        # Running: ADC and DAC powered, speaker on, unmuted, full volume
        m(0x21, 0x3F, 0)
        m(0x10, 0x3F, 0)
        m(0x1A, 0xFF, 0x08)
        m(0x1A, 0xDF, 0)
        w(0x1D, 0x12)
        w(0x1E, 0x20)
        m(0x15, 0xDF, 0)
        m(0x1A, 0xFF, 0x20)
        m(0x1A, 0xF7, 0)
        w(0x1D, 0x02)
        w(0x1E, 0xA0)
        self.volume(100)
        self.mute(False)

    def _write(self, reg, value):
        self.buf[0] = value
        self.i2c.writeto_mem(_ADDR, reg, self.buf)

    def _read(self, reg):
        self.i2c.readfrom_mem_into(_ADDR, reg, self.buf)
        return self.buf[0]

    def _modify(self, reg, keep, set_bits):
        self._write(reg, (self._read(reg) & keep) | set_bits)

    def volume(self, percent=None):
        # The DAC's volume, 100 (0 dB) to 1 (-59.5 dB), 0 muted; or, with no
        # argument, what it is
        if percent is None:
            reg = self._read(0x38)
            return 0 if reg >= 192 else max(0, 100 - reg * 10 // 12)
        percent = max(0, min(100, percent))
        self._write(0x38, 192 if percent == 0 else (100 - percent) * 12 // 10)

    def mute(self, on):
        self._modify(0x36, 0xDF, 0x20 if on else 0)

    def mic_gain(self, db):
        # The microphone's PGA, 0 to 21 dB in 3 dB steps
        n = max(0, min(7, db // 3))
        self._write(0x22, n | (n << 4))

    def off(self):
        # Speaker off, ADC and DAC down, then the chip reset and stopped
        self.mute(True)
        self._write(0x1E, 0x20)
        self._modify(0x15, 0xFF, 0x20)
        self._modify(0x10, 0xFF, 0xC0)
        self._modify(0x21, 0xFF, 0xC0)
        self._write(0x00, 0x7F)
