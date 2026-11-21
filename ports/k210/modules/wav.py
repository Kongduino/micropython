# WAV files on the Amigo's speaker, and from its microphone: 16-bit PCM,
# mono or stereo, at any rate, through the ES8374 codec and machine.I2S.
#
#   import wav
#   wav.play("/sd/hello.wav")            # returns when it's played
#   wav.play("/sd/hello.wav", volume=50)
#   wav.record("/sd/note.wav", 5)        # 5 s from the microphone, 16 kHz

import struct
from machine import I2S
from es8374 import ES8374

_IBUF = const(16384)
_CHUNK = const(4096)

_codec = None


def codec():
    # The codec, set up once
    global _codec
    if _codec is None:
        _codec = ES8374()
    return _codec


def _chunks(f):
    # (id, size) of each chunk of a RIFF file, the file at its data
    hdr = f.read(12)
    if len(hdr) < 12 or hdr[0:4] != b"RIFF" or hdr[8:12] != b"WAVE":
        raise ValueError("not a WAV file")
    while True:
        h = f.read(8)
        if len(h) < 8:
            return
        cid, size = h[0:4], struct.unpack("<I", h[4:8])[0]
        yield cid, size
        f.seek(f.tell() + size + (size & 1))


def play(path, volume=None):
    c = codec()
    if volume is not None:
        c.volume(volume)
    with open(path, "rb") as f:
        fmt = None
        for cid, size in _chunks(f):
            if cid == b"fmt ":
                fmt = struct.unpack("<HHIIHH", f.read(16))
                f.seek(f.tell() - 16)
            elif cid == b"data":
                break
        else:
            raise ValueError("no audio in the file")
        if fmt is None or fmt[0] != 1 or fmt[5] not in (16, 32) or fmt[1] not in (1, 2):
            raise ValueError("only 16 or 32-bit PCM, mono or stereo")
        _, channels, rate, _, _, bits = fmt
        out = I2S(0, mode=I2S.TX, rate=rate, bits=bits, format=I2S.STEREO if channels == 2 else I2S.MONO,
                  ibuf=_IBUF, **ES8374.TX_PINS)
        try:
            buf = bytearray(_CHUNK)
            mv = memoryview(buf)
            left = size
            while left > 0:
                n = f.readinto(mv[:min(left, _CHUNK)])
                if not n:
                    break
                out.write(mv[:n])
                left -= n
            # Silence after it, so that the end has gone through the ring
            # buffer before the I2S stops
            out.write(bytearray(_IBUF))
        finally:
            out.deinit()


def record(path, seconds, rate=16000):
    codec()
    size = int(seconds * rate) * 2
    mic = I2S(0, mode=I2S.RX, rate=rate, bits=16, format=I2S.MONO, ibuf=_IBUF, **ES8374.RX_PINS)
    try:
        buf = bytearray(_CHUNK)
        mic.readinto(buf)  # the ADC settles
        with open(path, "wb") as f:
            f.write(b"RIFF" + struct.pack("<I", 36 + size) + b"WAVE")
            f.write(b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate * 2, 2, 16))
            f.write(b"data" + struct.pack("<I", size))
            left = size
            while left > 0:
                n = min(left, _CHUNK)
                mic.readinto(memoryview(buf)[:n])
                f.write(memoryview(buf)[:n])
                left -= n
    finally:
        mic.deinit()
