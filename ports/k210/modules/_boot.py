import vfs
import k210


# Mount the file system, formatting the flash region if it has none yet.
# The flash programs in 256-byte pages.
bdev = k210.Flash()
try:
    fs = vfs.VfsLfs2(bdev, progsize=256)
except:
    vfs.VfsLfs2.mkfs(bdev, progsize=256)
    fs = vfs.VfsLfs2(bdev, progsize=256)
vfs.mount(fs, "/")

del vfs, k210, bdev, fs
