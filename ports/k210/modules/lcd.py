# The Amigo's screen as a framebuf: draw with FrameBuffer's methods (fill,
# text, line, rect, blit...), then show().
#
#   from lcd import LCD
#   lcd = LCD()
#   lcd.fill(0)
#   lcd.text("Hello", 10, 10, LCD.color(255, 255, 0))
#   lcd.show()

import framebuf
import k210


class LCD(framebuf.FrameBuffer):
    def __init__(self, rotation=0):
        # rotation 0 to 3, a quarter turn each; 0 is landscape, 480x320
        self.panel = k210.LCD(rotation)
        self.width, self.height = self.panel.size()
        self.buffer = bytearray(self.width * self.height * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)

    def show(self):
        self.panel.show(self.buffer)

    def on(self):
        self.panel.on()

    def off(self):
        self.panel.off()

    @staticmethod
    def color(r, g, b):
        # RGB565 from 8-bit red, green and blue
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
