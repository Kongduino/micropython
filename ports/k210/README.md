# MicroPython port to the Kendryte K210

A port for the Sipeed Maix Amigo (K210, RV64 dual core at 400 MHz, 6 MB SRAM),
on the bare Kendryte standalone SDK. So far:

- the REPL (friendly and raw, so `mpremote` and Thonny connect) on the USB
  serial port;
- a littlefs file system on the SPI flash, mounted at `/`, with `boot.py` and
  `main.py` run at start-up;
- MicroPython's "extra features" level: `os`, `time` (epoch 1970), `select`,
  `random`, `help()` and so on; FAT for SD cards (`vfs.VfsFat`);
- `machine`: `Pin`, `I2C`, `SPI`, `UART`, `PWM`, `Timer`, `WDT`, `I2S`, `SoftI2C`,
  `SoftSPI`, `Signal`, `RTC`, `mem8/16/32`, `reset`, `reset_cause`, `freq`,
  `unique_id` (the flash chip's), `idle`, `lightsleep`, `deepsleep`;
- `hashlib.sha256` on the K210's hash unit;
- the screen: `lcd.LCD`, a 480x320 `framebuf` (RGB565) with `show()`, and
  `off()`/`on()` (the backlight too), and the touch screen: `touch.Touch`;
- `cryptolib`: AES in C (ECB, CBC, CTR), axTLS's implementation, and
  `k210.AES`, the K210's AES accelerator (ECB, CBC, GCM; 128, 192, 256-bit
  keys);
- the SD card: `k210.SDCard`, mounted at `/sd` at start-up when a card with a
  FAT file system is in the slot;
- the cameras: `camera.Camera`, frames as `framebuf`s, RGB565 (`capture()`)
  or greyscale (`grey()`), upright with the Amigo held upright: the rear one
  (OV7740), 240x320, or the front one (GC0328), 320x240, with
  `Camera(front=True)`;
- audio: `es8374.ES8374`, the codec (speaker and microphone), and `wav`,
  `wav.play(path)` and `wav.record(path, seconds)` (16-bit PCM WAV files);
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
| `PWM(pin, freq=1000, duty_u16=32768)` | the 4 channels of TIMER2, given out as PWM objects are made; also `duty_ns`, `invert` | |
| `Timer(0..7, mode=, period=/freq=, callback=)` | the channels of TIMER0 and TIMER1 at 1 MHz: 1 us to 71 min | |
| `WDT(0..1, timeout=5000)` | the two watchdogs, resetting the chip at the first time-out | |

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
(red, green, blue; lit when their pin is low, so `PWM(pin, invert=True)`
makes a higher duty brighter; blue's pin is pulled low, so it's lit until
set high), the white flash LED on 32, the keys on 20 and 23 (also
Grove port 3's SDA and SCL), the touch controller's interrupt on 33. MaixPy's
configuration names a BACK key on 31, but on this board IO31 isn't one.

## Building

It needs:

- a current RISC-V GCC: the xPack `riscv-none-elf-gcc` (15.2 tested), whose
  `rv64imafc/lp64f` multilib matches the SDK's flags;
- the Kendryte standalone SDK, by default next to this repository
  (`../kendryte-standalone-sdk`, or set `K210_SDK`); its last commit,
  02576ba, is the one tested:

    $ git clone https://github.com/kendryte/kendryte-standalone-sdk.git

Then, in this repository:

    $ make -C mpy-cross
    $ cd ports/k210
    $ make submodules
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
- SPI0 and SPI1 are shared: `machine.SPI`, the SD card (SPI1) and the screen
  (SPI0) each set the controller and its pins up again when another has used
  it since, so an SPI(1) device on other pins (the SX1276 SP-MOD: sck=9,
  mosi=7, miso=31, CS 12, RESET 19) works alongside the mounted SD card.
- `k210.AES` runs about 2.5-3 times faster than `cryptolib` on 64 bytes and
  10 times on 4 KB (9.9 MB/s). CBC's chaining across calls is the object's;
  a GCM object does one job (one nonce), needs at least one byte of data (the
  accelerator hangs on none) and compares tags in software, in constant time.
- `hashlib.sha256` is the port's own: on the hash unit (25 MB/s on 64 KB,
  6 times the software), which wants the length up front. Its count of
  blocks starts at its largest and is set at `digest()`, which the unit
  allows. One object at a time has the unit (until `digest()`, or until it's
  freed); others meanwhile hash in software, as does a hash past the count's
  4 MB, from the unit's intermediate state. Only `sha256`, as before.
- `Timer` and `PWM` share the three timer units: TIMER0 and TIMER1 (8
  channels) for `Timer`, TIMER2 (4) for `PWM`. Their callbacks, like pin
  interrupts, run through the scheduler. PWM at a duty of 0 or 65535 drives
  the pin as a GPIO (the timer can't hold its output for a whole period).
- `WDT` time-outs are powers of two of the watchdog's clock, the one asked
  for rounded up; a watchdog can't be stopped once started.
- The cameras (`k210.Camera`): the rear one's driver is the Meshtastic K210
  port's, the front one's register settings MaixPy's. Both sit on the DVP's
  data lines and on I2C2 (IO40/IO41) at the same address; the DVP's PWDN
  line powers one and holds the other down, so one runs at a time and
  `Camera()` of the other switches over. YUV in; the DVP writes each frame
  as RGB565 and as R, G, B planes (the G plane is `grey()`). The DVP's data
  pads are SPI0's, so they're routed to SPI0 as the screen has them. Each
  sensor's 320x240 frame is turned as it's copied out: the rear camera's a
  quarter turn and upside down (its own mirror and flip put its colour
  filter pattern out of step: green came out magenta), the front one's
  flipped top to bottom. Rear about 26 frames a second, front 15. `reg()`
  reads and writes the running sensor's registers.
- `lightsleep([ms])` runs the CPU (and the buses, from its clock) on the
  26 MHz oscillator with PLL0 powered down, until the time is up or an
  interrupt comes (a pin, a `Timer`, the REPL's UART: Ctrl-C works asleep);
  `ticks_ms()` and the time of day carry on, counted by the CLINT's timer.
  PLL1 (which also clocks the top 2 MB of RAM) and PLL2 run on. UARTs, I2C
  and SPI run slower while asleep, as does PWM. The high-speed UART's bit
  time measures about 10 clock cycles longer than its divider gives, which
  only shows at 26 MHz (4%), so its divider is set with them taken off.
  Measured at the USB input: about 112 mA awake and 60 mA asleep with the
  screen off; the backlight adds about 60 mA.
- `deepsleep(ms)` turns off the screen and the camera, sleeps as
  `lightsleep()` but through interrupts, then resets; `reset_cause()` then
  gives `DEEPSLEEP_RESET`, told from `machine.reset()` by a mark left in one
  of the AXP173's data registers. `deepsleep()` with no time has the AXP173
  turn the Amigo off (even on USB power, the USB serial chip too); the power
  button turns it on. `reset_cause()` gives `PWRON_RESET`, `SOFT_RESET`
  (`machine.reset()`), `WDT_RESET` or `DEEPSLEEP_RESET`: the SDK's start-up
  code keeps the reset status but doesn't tell a power-on from the reset
  line (which kflash and mpremote use), both `PWRON_RESET` here, as on rp2.
- `lcd.off()` puts the controller to sleep and holds it in reset, which
  turns the backlight off; `on()` sets it up again, blank until `show()`.
- `machine.I2S`: the three I2S controllers as controller (SCK, WS and MCK
  out), on any pins, TX on a controller's channel 2 and RX on channel 0 (as
  MaixPy), blocking, non-blocking (`irq()`) and asyncio, with DMA into a
  buffer in two halves and the shared ring buffer. The controller always
  works in 32-bit samples, a 16-bit sample in the top half (set to 16 bits,
  its transmitter sends a word's top half, which left the codec silent).
  PLL2 is set for each rate so that MCK is 256 times it, as codecs want:
  26 MHz * nf / no, the closest to 512 * rate * n, within 0.1% at the usual
  rates; one rate for the three controllers. The I2S pins are set to the
  weakest drive: at full drive, MCK and SCK disturbed the Amigo's internal
  I2C bus (arbitration lost in one transfer in a few, and once a chip left
  holding SDA). `machine.I2C` also clears a stuck bus after a failed
  transfer (up to 9 clocks with SDA let go, then a STOP).
- The ES8374's settings are those MaixPy's `es8374.py` makes (the codec as
  target, 16 bits, MCK / 256): speaker and microphone (PGA +18 dB) on,
  `volume()`, `mute()`, `mic_gain()`, `off()`. Its pins are IO13 (MCK),
  IO21 (SCK), IO18 (WS), IO34 (to it) and IO35 (from it), in
  `ES8374.TX_PINS` and `RX_PINS`. A voice close by records at a level of a
  few thousand.
- Floats are single precision, with the SDK's `lp64f` ABI.
- The second core is idle, waiting in the SDK's start-up code.
