# The Amigo's cameras, as framebufs upright with the Amigo held upright: the
# rear one (OV7740), 240x320, or the front one (GC0328), 320x240, with
# Camera(front=True). One runs at a time.
#
#   from camera import Camera
#   from lcd import LCD
#   cam, lcd = Camera(), LCD(1)        # the screen upright, 320x480
#   lcd.blit(cam.capture(), 40, 80)   # an RGB565 frame, onto the screen
#   lcd.show()
#   g = cam.grey()                     # a GS8 frame (the green channel)

import framebuf
import k210


class Camera:
    def __init__(self, front=False):
        self.camera = k210.Camera(front)
        self.width, self.height = self.camera.size()
        self.buffer = bytearray(self.width * self.height * 2)
        self.frame = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)
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
            self.grey_buffer = bytearray(self.width * self.height)
            self.grey_frame = framebuf.FrameBuffer(self.grey_buffer, self.width, self.height, framebuf.GS8)
        self.camera.grey(self.grey_buffer)
        return self.grey_frame

    def reg(self, addr, value=None):
        # Reads (or, given a value, writes) one of the camera's registers
        if value is None:
            return self.camera.reg(addr)
        self.camera.reg(addr, value)

    def off(self):
        self.camera.off()
