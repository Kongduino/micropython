# The Amigo's rear camera (OV7740), 320x240, as framebufs:
#
#   from camera import Camera
#   from lcd import LCD
#   cam, lcd = Camera(), LCD()
#   lcd.blit(cam.capture(), 80, 40)   # an RGB565 frame, onto the screen
#   lcd.show()
#   g = cam.grey()                     # a GS8 frame (the green channel)

import framebuf
import k210


class Camera:
    WIDTH = 320
    HEIGHT = 240

    def __init__(self):
        self.camera = k210.Camera()
        self.buffer = bytearray(self.WIDTH * self.HEIGHT * 2)
        self.frame = framebuf.FrameBuffer(self.buffer, self.WIDTH, self.HEIGHT, framebuf.RGB565)
        self.grey_buffer = None
        self.grey_frame = None

    def capture(self):
        # The next frame, in self.buffer; returns self.frame (RGB565)
        self.camera.rgb565(self.buffer)
        return self.frame

    def grey(self):
        # The next frame's green channel, in self.grey_buffer; returns
        # self.grey_frame (GS8)
        if self.grey_buffer is None:
            self.grey_buffer = bytearray(self.WIDTH * self.HEIGHT)
            self.grey_frame = framebuf.FrameBuffer(self.grey_buffer, self.WIDTH, self.HEIGHT, framebuf.GS8)
        self.camera.grey(self.grey_buffer)
        return self.grey_frame

    def reg(self, addr, value=None):
        # Reads (or, given a value, writes) one of the OV7740's registers
        if value is None:
            return self.camera.reg(addr)
        self.camera.reg(addr, value)

    def off(self):
        self.camera.off()
