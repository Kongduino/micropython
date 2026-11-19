# MicroPython port to the Kendryte K210

A port for the Sipeed Maix Amigo (K210, RV64 dual core at 400 MHz, 6 MB SRAM),
on the bare Kendryte standalone SDK. So far:

- the REPL (friendly and raw, so `mpremote` and Thonny connect) on the USB
  serial port;
- a littlefs file system on the SPI flash, mounted at `/`, with `boot.py` and
  `main.py` run at start-up;
- `os`, `time` (with `localtime` and `time`, epoch 1970), `help()`;
- `machine`: `RTC`, `reset`, `freq`, `unique_id` (the flash chip's), `idle`,
  `lightsleep`/`deepsleep` (a wait, and a wait then a reset, for now);
- `k210.Flash`, the file system's block device.

No `machine.Pin`, `I2C`, `SPI` or `UART` yet.

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
- The SDK's `iomem.c` doesn't build against current newlib (`_lock_t`), and
  nothing here uses it, so it's left out.
- The file system takes the 1 MB at 0xC00000, clear of Meshtastic's LittleFS
  (0x400000-0x5FFFFF) and MaixPy's SPIFFS (0xD00000-0xFFFFFF). The frozen
  `_boot.py` formats it if it holds no file system.
- The time of day is kept from the CPU's cycle counter and lost at reset;
  `machine.RTC().datetime(...)` sets it (Thonny does on connecting).
- Floats are single precision, with the SDK's `lp64f` ABI.
- The second core is idle, waiting in the SDK's start-up code.
