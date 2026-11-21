import vfs
import k210
from machine import I2C


# The power chip's (AXP173, 0x34 on I2C 0) LDO4 at 1.5 V and LDO2/LDO3 at
# 1.8 V/3.0 V, as MaixPy's boot.py sets them "for the sensor" (the camera)
try:
    i2c = I2C(0)
    i2c.writeto_mem(0x34, 0x27, b"\x20")
    i2c.writeto_mem(0x34, 0x28, b"\x0c")
    del i2c
except OSError:
    pass


# Mount the file system, formatting the flash region if it has none yet.
# The flash programs in 256-byte pages.
bdev = k210.Flash()
try:
    fs = vfs.VfsLfs2(bdev, progsize=256)
except:
    vfs.VfsLfs2.mkfs(bdev, progsize=256)
    fs = vfs.VfsLfs2(bdev, progsize=256)
vfs.mount(fs, "/")

# An SD card, if there's one in the slot with a FAT file system, at /sd
try:
    vfs.mount(vfs.VfsFat(k210.SDCard()), "/sd")
except OSError:
    pass

del vfs, k210, I2C, bdev, fs
