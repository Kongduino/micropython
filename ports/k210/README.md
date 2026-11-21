# MicroPython port to the Kendryte K210

A port for the Sipeed Maix Amigo (K210, RV64 dual core at 400 MHz, 6 MB SRAM),
on the bare Kendryte standalone SDK. So far:

- the REPL (friendly and raw, so `mpremote` and Thonny connect) on the USB
  serial port;
- a littlefs file system on the SPI flash, mounted at `/`, with `boot.py` and
  `main.py` run at start-up;
- MicroPython's "extra features" level: `os`, `time` (epoch 1970), `select`,
  `random`, `help()` and so on; FAT for SD cards (`vfs.VfsFat`);
- `machine`: `Pin`, `I2C`, `SPI`, `UART`, `SoftI2C`, `SoftSPI`, `Signal`,
  `RTC`, `mem8/16/32`, `reset`, `freq`, `unique_id` (the flash chip's),
  `idle`, `lightsleep`/`deepsleep` (a wait, and a wait then a reset, for now);
- the screen: `lcd.LCD`, a 480x320 `framebuf` (RGB565) with `show()`, and
  the touch screen: `touch.Touch`;
- `cryptolib`: AES in C (ECB, CBC, CTR), axTLS's implementation, and
  `k210.AES`, the K210's AES accelerator (ECB, CBC, GCM; 128, 192, 256-bit
  keys);
- the SD card: `k210.SDCard`, mounted at `/sd` at start-up when a card with a
  FAT file system is in the slot;
- the onboard chips: `axp173.AXP173` (battery, USB power, charging) and
  `msa301.MSA301` (acceleration, and the screen rotation the Amigo is held in);
- `k210.Flash`, the file system's block device, and `k210.LCD`, the panel.

## Pins and buses

Pins are the K210's IO numbers, 0 to 47 (`Pin(14)`, or `14` as an argument).
The FPIOA routes any function to any pin, so every bus takes its pins as
arguments:

| Class | Hardware | Defaults |
|---|---|---|
| `Pin(n)` | one of the 32 high-speed GPIO channels, taken when the pin is first used | |
| `I2C(0..2, scl=, sda=, freq=400000)` | the three I2C controllers | `I2C(0)`: the internal bus, scl=24, sda=27 (AXP173 0x34, MSA301 0x26, FT6X36 0x38, ES8374 0x10) |
| `SPI(0..1, baudrate, sck=, mosi=, miso=)` | SPI0 and SPI1, master, mode 0-3, 8 bits, MSB first; chip select is a `Pin` | `SPI(1)`: the SD card slot, sck=11, mosi=10, miso=6 (CS is 26) |
| `UART(1..3, baudrate, tx=, rx=)` | UART1 to UART3, interrupt-driven receive buffer (`rxbuf=`, 256 bytes by default) | |

The screen:

    from lcd import LCD
    lcd = LCD()            # rotation 0-3, a quarter turn each; 0: landscape
    lcd.fill(0)
    lcd.text("Hello", 10, 10, LCD.color(255, 255, 0))
    lcd.show()             # returns while the DMA sends the frame (about 20 ms)

The touch screen (FT6X36 on `I2C(0)`), in the screen's coordinates:

    from touch import Touch
    touch = Touch()        # the same rotation as the LCD's
    touch.read()           # (x, y), or None when nothing touches

The power chip and the accelerometer:

    from axp173 import AXP173
    pmu = AXP173()
    pmu.battery_voltage(), pmu.battery_level(), pmu.charging(), pmu.usb_voltage()

    from msa301 import MSA301
    acc = MSA301()
    acc.acceleration()     # (x, y, z) in g
    lcd = LCD(acc.rotation() or 0)   # None when lying flat

AES on the accelerator, ECB and CBC as `cryptolib.aes`, GCM as PyCryptodome:

    from k210 import AES
    ct = AES(key, AES.MODE_CBC, iv).encrypt(data)       # multiples of 16 bytes
    ct, tag = AES(key, AES.MODE_GCM, nonce).encrypt_and_digest(data, aad)
    data = AES(key, AES.MODE_GCM, nonce).decrypt_and_verify(ct, tag, aad)

The SD card is mounted at `/sd` at start-up if one is in the slot. By hand
(after changing cards, say):

    import vfs, k210
    vfs.mount(vfs.VfsFat(k210.SDCard()), "/sd")   # SPI1, pins 11/10/6, CS 26

Other pins of the board (from Maixduino's Amigo variant): LEDs on 14, 15, 17
(red, green, blue), the white flash LED on 32, the keys on 20 and 23 (also
Grove port 3's SDA and SCL), the touch controller's interrupt on 33. MaixPy's
configuration names a BACK key on 31, but on this board IO31 isn't one.

## Building

It needs:

- a current RISC-V GCC: the xPack `riscv-none-elf-gcc` (15.2 tested), whose
  `rv64imafc/lp64f` multilib matches the SDK's flags;
- the Kendryte standalone SDK, by default next to this repository
  (`../kendryte-standalone-sdk`, or set `K210_SDK`).

    $ make -C mpy-cross
    $ cd ports/k210
    $ make

## Flashing

`make deploy` writes `build/firmware.bin` to address 0 with kflash (the copy in
PlatformIO's `tool-kflash-kendryte210` by default; set `KFLASH`). The serial
port defaults to `/dev/cu.usbserial-2101`; set `PORT` otherwise.

    $ make deploy PORT=/dev/cu.usbserial-XXXX

The REPL is on the same port at 115200 baud.

## Notes

- The SDK's start-up code (`lib/bsp`) runs first: it zeroes .bss, starts the
  PLIC and puts the SDK console on UART3. `main()` then raises PLL0 to 800 MHz
  and moves IO4/IO5 to the high-speed UART, whose receive interrupt fills a
  4 KB buffer (the hardware FIFO holds 8 bytes).
- The SDK's `iomem.c` (the DMA driver's allocator) wants the `_lock_t` of
  older newlibs; it's built with the SDK's own definition (`long`).
- The file system takes the 1 MB at 0xC00000, clear of Meshtastic's LittleFS
  (0x400000-0x5FFFFF) and MaixPy's SPIFFS (0xD00000-0xFFFFFF). The frozen
  `_boot.py` formats it if it holds no file system.
- The time of day is kept from the CPU's cycle counter and lost at reset;
  `machine.RTC().datetime(...)` sets it (Thonny does on connecting).
- I2C: the controller ends a transfer with a STOP when its transmit FIFO runs
  empty and has no STOP or address-only command, so a transfer's bytes are
  fed without a gap (a write then a read is one transfer, with a repeated
  START), and a write of nothing (`scan`, `writeto(addr, b'')`) probes with a
  1-byte read.
- Pin interrupts: the GPIO fires on both edges whichever is enabled, so both
  are, and the level read in the interrupt picks the edges asked for. Handlers
  run through the scheduler (no `hard=True`).
- At most 32 pins can be `Pin`s at once (the high-speed GPIO channels); a pin
  given to a bus frees its channel.
- `k210.SDCard` speaks the same SPI protocol as micropython-lib's `sdcard.py`,
  but polls the card in a tight loop where `sdcard.py` sleeps 1 ms: about
  2.2 MB/s reading and 1.7 MB/s writing at 25 MHz, against 85 KB/s reading
  with `sdcard.py`. It takes SPI1 for itself.
- The screen (ILI9481 on SPI0 in octal mode, IO36-IO39, the DVP's data
  lines) is turned by the panel (MADCTL); `show()` copies the framebuf into
  one of two uncached frame buffers, swapping each pair of pixels into the
  order the bus sends them, and the DMA sends it. SPI0 and DMA channel 5 are
  the screen's.
- IO36-IO47 are set to 1.8 V at start-up, as Maixduino and MaixPy do.
- `cryptolib` takes only axTLS's `aes.c` (extmod.mk builds axTLS for the
  `ssl` module, which isn't here); `axtls-include/arpa/inet.h` gives it the
  byte-order functions a bare-metal toolchain lacks.
- `k210.AES` runs about 2.5-3 times faster than `cryptolib` on 64 bytes and
  10 times on 4 KB (9.9 MB/s). CBC's chaining across calls is the object's;
  a GCM object does one job (one nonce), needs at least one byte of data (the
  accelerator hangs on none) and compares tags in software, in constant time.
- Floats are single precision, with the SDK's `lp64f` ABI.
- The second core is idle, waiting in the SDK's start-up code.
