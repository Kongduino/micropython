// k210.SDCard: an SD card in SPI mode, as a block device for vfs.VfsFat.
//
// The protocol is micropython-lib's sdcard.py's, in C: the card is polled
// in a tight loop (with a time limit) for its data token and while it's
// busy, where sdcard.py sleeps 1 ms between polls, which held reads to about
// 85 KB/s. SPI1 is the card's; the pins default to the Amigo's slot.

#include <string.h>

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "extmod/vfs.h"

#include "fpioa.h"
#include "gpiohs.h"
#include "spi.h"

#define SD_SPI (1)
#define SD_BLOCK (512)
#define SD_INIT_BAUDRATE (400000)
#define SD_DEFAULT_BAUDRATE (25000000)

#define CMD_TIMEOUT_MS (100) // waiting for a data token
#define BUSY_TIMEOUT_MS (1000) // waiting for a write to finish
#define INIT_TIMEOUT_MS (1000) // waiting for the card to leave idle

#define R1_IDLE (0x01)
#define R1_ILLEGAL_COMMAND (0x04)
#define TOKEN_DATA (0xFE)
#define TOKEN_MULTI_WRITE (0xFC)
#define TOKEN_STOP_TRAN (0xFD)

typedef struct _k210_sdcard_obj_t {
    mp_obj_base_t base;
    uint8_t sck, mosi, miso, cs;
    int cs_channel;
    uint32_t baudrate;
    bool block_addressing; // SDHC/SDXC: blocks; SDSC: bytes
    uint32_t sectors;
} k210_sdcard_obj_t;

extern const mp_obj_type_t k210_sdcard_type;

static void sd_bus(k210_sdcard_obj_t *self, uint32_t baudrate) {
    k210_spi_owner[SD_SPI] = self;
    machine_pin_set_function(self->sck, FUNC_SPI1_SCLK);
    machine_pin_set_function(self->mosi, FUNC_SPI1_D0);
    machine_pin_set_function(self->miso, FUNC_SPI1_D1);
    spi_init(SD_SPI, SPI_WORK_MODE_0, SPI_FF_STANDARD, 8, 0);
    spi_set_clk_rate(SD_SPI, baudrate);
    volatile spi_t *regs = spi[SD_SPI];
    regs->ctrlr0 = (regs->ctrlr0 & ~(3U << 8)) | (SPI_TMOD_TRANS_RECV << 8);
}

static void sd_cs(k210_sdcard_obj_t *self, int level) {
    gpiohs_set_pin(self->cs_channel, level ? GPIO_PV_HIGH : GPIO_PV_LOW);
}

static uint8_t sd_byte(uint8_t out) {
    uint8_t in;
    k210_spi_transfer(SD_SPI, 1, &out, &in);
    return in;
}

static void sd_read(uint8_t *buf, size_t len) {
    k210_spi_transfer(SD_SPI, len, NULL, buf);
}

static void sd_write(const uint8_t *buf, size_t len) {
    k210_spi_transfer(SD_SPI, len, buf, NULL);
}

// Ends a command: CS high and a byte of clocks
static void sd_release(k210_sdcard_obj_t *self) {
    sd_cs(self, 1);
    sd_byte(0xFF);
}

// Waits while the card holds MISO low (busy); false on time-out
static bool sd_wait_ready(uint32_t timeout_ms) {
    mp_uint_t start = mp_hal_ticks_ms();
    while (sd_byte(0xFF) != 0xFF) {
        if (mp_hal_ticks_ms() - start > timeout_ms) {
            return false;
        }
    }
    return true;
}

// Sends a command and returns its R1 response (0xFF: none), leaving CS low
// for what follows; extra bytes of a longer response go to `extra`
static int sd_command(k210_sdcard_obj_t *self, uint8_t cmd, uint32_t arg, uint8_t crc, uint8_t *extra, size_t extra_len) {
    sd_cs(self, 0);
    if (cmd != 12) {
        // (STOP_TRANSMISSION interrupts a card that is sending data)
        sd_wait_ready(BUSY_TIMEOUT_MS);
    }
    uint8_t frame[6] = {0x40 | cmd, arg >> 24, arg >> 16, arg >> 8, arg, crc};
    sd_write(frame, sizeof(frame));
    if (cmd == 12) {
        sd_byte(0xFF); // the stuff byte after STOP_TRANSMISSION
    }
    // The response comes within 8 bytes: the first without bit 7 set
    for (int i = 0; i < 10; i++) {
        uint8_t r = sd_byte(0xFF);
        if (!(r & 0x80)) {
            if (extra_len) {
                sd_read(extra, extra_len);
            }
            return r;
        }
    }
    return 0xFF;
}

// Waits for a data block's start token; false on time-out or an error token
static bool sd_wait_token(void) {
    mp_uint_t start = mp_hal_ticks_ms();
    for (;;) {
        uint8_t t = sd_byte(0xFF);
        if (t == TOKEN_DATA) {
            return true;
        }
        if (t != 0xFF || mp_hal_ticks_ms() - start > CMD_TIMEOUT_MS) {
            return false;
        }
    }
}

// Reads one data block (and drops its CRC)
static bool sd_read_block(uint8_t *buf, size_t len) {
    if (!sd_wait_token()) {
        return false;
    }
    sd_read(buf, len);
    uint8_t crc[2];
    sd_read(crc, 2);
    return true;
}

// Writes one data block with the token; true if the card accepted it
static bool sd_write_block(uint8_t token, const uint8_t *buf) {
    sd_byte(token);
    sd_write(buf, SD_BLOCK);
    uint8_t crc[2] = {0xFF, 0xFF};
    sd_write(crc, 2);
    if ((sd_byte(0xFF) & 0x1F) != 0x05) {
        return false;
    }
    return sd_wait_ready(BUSY_TIMEOUT_MS);
}

static void sd_init_card(k210_sdcard_obj_t *self) {
    sd_bus(self, SD_INIT_BAUDRATE);
    // 80 clocks or more with CS high, for the card to enter SPI mode
    sd_cs(self, 1);
    uint8_t ff[16];
    memset(ff, 0xFF, sizeof(ff));
    sd_write(ff, sizeof(ff));

    // GO_IDLE_STATE
    int r = 0xFF;
    for (int i = 0; i < 5 && r != R1_IDLE; i++) {
        r = sd_command(self, 0, 0, 0x95, NULL, 0);
        sd_release(self);
    }
    if (r != R1_IDLE) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("no SD card"));
    }

    // SEND_IF_COND: version 2 cards echo the check pattern
    uint8_t r7[4];
    r = sd_command(self, 8, 0x1AA, 0x87, r7, 4);
    sd_release(self);
    bool v2 = r == R1_IDLE;
    if (v2 && ((r7[2] & 0x0F) != 0x01 || r7[3] != 0xAA)) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("SD card voltage mismatch"));
    } else if (!v2 && !(r & R1_ILLEGAL_COMMAND)) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("SD card not recognised"));
    }

    // SD_SEND_OP_COND (APP_CMD first) until the card leaves idle
    mp_uint_t start = mp_hal_ticks_ms();
    do {
        sd_command(self, 55, 0, 0x65, NULL, 0);
        sd_release(self);
        r = sd_command(self, 41, v2 ? 0x40000000 : 0, 0x77, NULL, 0);
        sd_release(self);
        if (mp_hal_ticks_ms() - start > INIT_TIMEOUT_MS) {
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("SD card didn't start"));
        }
    } while (r != 0);

    // READ_OCR: CCS tells block from byte addressing
    self->block_addressing = false;
    if (v2) {
        uint8_t ocr[4];
        if (sd_command(self, 58, 0, 0xFD, ocr, 4) == 0) {
            self->block_addressing = ocr[0] & 0x40;
        }
        sd_release(self);
    }

    // SEND_CSD: the capacity
    uint8_t csd[16];
    if (sd_command(self, 9, 0, 0xAF, NULL, 0) != 0 || !sd_read_block(csd, sizeof(csd))) {
        sd_release(self);
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("SD card: no CSD"));
    }
    sd_release(self);
    if ((csd[0] >> 6) == 1) {
        // CSD version 2: C_SIZE counts 512 KB
        uint32_t c_size = ((uint32_t)(csd[7] & 0x3F) << 16) | (csd[8] << 8) | csd[9];
        self->sectors = (c_size + 1) * 1024;
    } else {
        uint32_t c_size = ((uint32_t)(csd[6] & 0x03) << 10) | (csd[7] << 2) | (csd[8] >> 6);
        uint32_t c_size_mult = ((csd[9] & 0x03) << 1) | (csd[10] >> 7);
        uint32_t read_bl_len = csd[5] & 0x0F;
        uint64_t bytes = (uint64_t)(c_size + 1) << (c_size_mult + 2 + read_bl_len);
        self->sectors = bytes / SD_BLOCK;
    }

    // SET_BLOCKLEN for byte-addressed cards
    if (!self->block_addressing) {
        r = sd_command(self, 16, SD_BLOCK, 0x15, NULL, 0);
        sd_release(self);
        if (r != 0) {
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("SD card: can't set the block size"));
        }
    }
}

// SDCard(*, baudrate=25000000, sck=11, mosi=10, miso=6, cs=26)
static mp_obj_t k210_sdcard_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum { ARG_baudrate, ARG_sck, ARG_mosi, ARG_miso, ARG_cs };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_baudrate, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = SD_DEFAULT_BAUDRATE} },
        { MP_QSTR_sck, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_INT(11)} },
        { MP_QSTR_mosi, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_INT(10)} },
        { MP_QSTR_miso, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_INT(6)} },
        { MP_QSTR_cs, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_INT(26)} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    k210_sdcard_obj_t *self = mp_obj_malloc(k210_sdcard_obj_t, type);
    self->sck = mp_hal_get_pin_obj(args[ARG_sck].u_obj);
    self->mosi = mp_hal_get_pin_obj(args[ARG_mosi].u_obj);
    self->miso = mp_hal_get_pin_obj(args[ARG_miso].u_obj);
    self->cs = mp_hal_get_pin_obj(args[ARG_cs].u_obj);
    self->baudrate = args[ARG_baudrate].u_int;
    self->cs_channel = machine_pin_gpio_channel(self->cs);
    gpiohs_set_pin(self->cs_channel, GPIO_PV_HIGH);
    gpiohs_set_drive_mode(self->cs_channel, GPIO_DM_OUTPUT);
    sd_init_card(self);
    return MP_OBJ_FROM_PTR(self);
}

// readblocks(block, buf): whole blocks
static mp_obj_t k210_sdcard_readblocks(mp_obj_t self_in, mp_obj_t block_in, mp_obj_t buf_in) {
    k210_sdcard_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint32_t block = mp_obj_get_int(block_in);
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buf_in, &bufinfo, MP_BUFFER_WRITE);
    size_t n = bufinfo.len / SD_BLOCK;
    if (n == 0 || bufinfo.len % SD_BLOCK) {
        mp_raise_ValueError(MP_ERROR_TEXT("buffer must be whole blocks"));
    }
    uint32_t addr = self->block_addressing ? block : block * SD_BLOCK;
    uint8_t *buf = bufinfo.buf;
    bool ok;

    sd_bus(self, self->baudrate);
    if (n == 1) {
        // READ_SINGLE_BLOCK
        ok = sd_command(self, 17, addr, 0, NULL, 0) == 0 && sd_read_block(buf, SD_BLOCK);
    } else {
        // READ_MULTIPLE_BLOCK, then STOP_TRANSMISSION
        ok = sd_command(self, 18, addr, 0, NULL, 0) == 0;
        for (size_t i = 0; ok && i < n; i++) {
            ok = sd_read_block(buf + i * SD_BLOCK, SD_BLOCK);
        }
        ok &= sd_command(self, 12, 0, 0, NULL, 0) == 0 && sd_wait_ready(BUSY_TIMEOUT_MS);
    }
    sd_release(self);
    if (!ok) {
        mp_raise_OSError(MP_EIO);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(k210_sdcard_readblocks_obj, k210_sdcard_readblocks);

// writeblocks(block, buf): whole blocks
static mp_obj_t k210_sdcard_writeblocks(mp_obj_t self_in, mp_obj_t block_in, mp_obj_t buf_in) {
    k210_sdcard_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint32_t block = mp_obj_get_int(block_in);
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buf_in, &bufinfo, MP_BUFFER_READ);
    size_t n = bufinfo.len / SD_BLOCK;
    if (n == 0 || bufinfo.len % SD_BLOCK) {
        mp_raise_ValueError(MP_ERROR_TEXT("buffer must be whole blocks"));
    }
    uint32_t addr = self->block_addressing ? block : block * SD_BLOCK;
    const uint8_t *buf = bufinfo.buf;
    bool ok;

    sd_bus(self, self->baudrate);
    if (n == 1) {
        // WRITE_BLOCK
        ok = sd_command(self, 24, addr, 0, NULL, 0) == 0 && sd_write_block(TOKEN_DATA, buf);
    } else {
        // WRITE_MULTIPLE_BLOCK, ended by the stop token
        ok = sd_command(self, 25, addr, 0, NULL, 0) == 0;
        for (size_t i = 0; ok && i < n; i++) {
            ok = sd_write_block(TOKEN_MULTI_WRITE, buf + i * SD_BLOCK);
        }
        sd_byte(TOKEN_STOP_TRAN);
        sd_byte(0xFF);
        ok &= sd_wait_ready(BUSY_TIMEOUT_MS);
    }
    sd_release(self);
    if (!ok) {
        mp_raise_OSError(MP_EIO);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(k210_sdcard_writeblocks_obj, k210_sdcard_writeblocks);

static mp_obj_t k210_sdcard_ioctl(mp_obj_t self_in, mp_obj_t cmd_in, mp_obj_t arg_in) {
    k210_sdcard_obj_t *self = MP_OBJ_TO_PTR(self_in);
    switch (mp_obj_get_int(cmd_in)) {
        case MP_BLOCKDEV_IOCTL_INIT:
        case MP_BLOCKDEV_IOCTL_DEINIT:
        case MP_BLOCKDEV_IOCTL_SYNC:
            return MP_OBJ_NEW_SMALL_INT(0);
        case MP_BLOCKDEV_IOCTL_BLOCK_COUNT:
            return mp_obj_new_int_from_uint(self->sectors);
        case MP_BLOCKDEV_IOCTL_BLOCK_SIZE:
            return MP_OBJ_NEW_SMALL_INT(SD_BLOCK);
        default:
            return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_3(k210_sdcard_ioctl_obj, k210_sdcard_ioctl);

static const mp_rom_map_elem_t k210_sdcard_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_readblocks), MP_ROM_PTR(&k210_sdcard_readblocks_obj) },
    { MP_ROM_QSTR(MP_QSTR_writeblocks), MP_ROM_PTR(&k210_sdcard_writeblocks_obj) },
    { MP_ROM_QSTR(MP_QSTR_ioctl), MP_ROM_PTR(&k210_sdcard_ioctl_obj) },
};
static MP_DEFINE_CONST_DICT(k210_sdcard_locals_dict, k210_sdcard_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    k210_sdcard_type,
    MP_QSTR_SDCard,
    MP_TYPE_FLAG_NONE,
    make_new, k210_sdcard_make_new,
    locals_dict, &k210_sdcard_locals_dict
    );
