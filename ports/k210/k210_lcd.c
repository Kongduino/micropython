// k210.LCD: the Amigo's 3.5" IPS panel (ILI9481, 320x480), on SPI0 in octal
// mode with DMA. The frozen lcd.py puts a framebuf in front of it.
//
// The bus code is the Meshtastic K210 port's (AmigoLCD.cpp), MaixPy-v1's
// panel set-up. The panel turns the picture itself (MADCTL), so show() only
// swaps each pair of pixels into the order the bus sends them, copying the
// framebuf into one of two uncached frame buffers. The DMA, which reads RAM
// directly, sends it from there while show() returns; the next show() fills
// the other buffer meanwhile, and waits for the transfer before starting its
// own.

#include <string.h>

#include "py/runtime.h"
#include "py/mphal.h"

#include "dmac.h"
#include "fpioa.h"
#include "gpiohs.h"
#include "spi.h"
#include "sysctl.h"

#define LCD_PIN_CS (36)
#define LCD_PIN_RST (37)
#define LCD_PIN_DCX (38)
#define LCD_PIN_WR (39)
#define LCD_SS (3) // SPI0 chip select line
#define LCD_SPI SPI_DEVICE_0
#define LCD_DMA DMAC_CHANNEL5
#define LCD_FREQ (15000000)
#define LCD_FIFO_DEPTH (32)

#define CMD_SOFTWARE_RESET 0x01
#define CMD_SLEEP_IN 0x10
#define CMD_SLEEP_OFF 0x11
#define CMD_NORMAL_DISP_ON 0x13
#define CMD_INVERSION_ON 0x21
#define CMD_DISPLAY_OFF 0x28
#define CMD_DISPLAY_ON 0x29
#define CMD_COLUMN_ADDR_SET 0x2A
#define CMD_PAGE_ADDR_SET 0x2B
#define CMD_MEMORY_WRITE 0x2C
#define CMD_MEMORY_ACCESS 0x36
#define CMD_PIXEL_FORMAT 0x3A
#define CMD_POWER_SETTING 0xD0
#define CMD_VCOM_CONTROL 0xD1

#define PANEL_SHORT 320
#define PANEL_LONG 480

// MADCTL for rotations 0 to 3, a quarter turn each: landscape as MaixPy has it
// on the Amigo (0x28: row/column exchange, BGR), portrait with the camera at
// the top (0x48), and both upside down
static const uint8_t rotation_madctl[4] = {0x28, 0x48, 0xE8, 0x88};

#define FB_WORDS (PANEL_SHORT * PANEL_LONG / 2)
static uint32_t fb_mem[2][FB_WORDS] __attribute__((aligned(64)));

typedef struct _k210_lcd_obj_t {
    mp_obj_base_t base;
} k210_lcd_obj_t;

extern const mp_obj_type_t k210_lcd_type;
static const k210_lcd_obj_t k210_lcd_obj = {{&k210_lcd_type}};

static bool lcd_ready;
static int lcd_rotation;
static int dcx_channel;
static int back; // the frame buffer show() fills next
static bool dma_busy;

static uint32_t *frame_buffer(int i) {
    // The uncached alias (0x8xxxxxxx -> 0x4xxxxxxx), so that the DMA never
    // misses data still in the CPU's cache
    return (uint32_t *)((uintptr_t)fb_mem[i] - 0x40000000);
}

static void route_pins(void) {
    machine_pin_set_function(LCD_PIN_CS, FUNC_SPI0_SS0 + LCD_SS);
    machine_pin_set_function(LCD_PIN_WR, FUNC_SPI0_SCLK);
    k210_spi_owner[LCD_SPI] = &k210_lcd_obj;
}

static void bus_config(bool data, uint8_t bits) {
    if (k210_spi_owner[LCD_SPI] != &k210_lcd_obj) {
        // machine.SPI(0) used the controller since
        route_pins();
    }
    gpiohs_set_pin(dcx_channel, data ? GPIO_PV_HIGH : GPIO_PV_LOW);
    spi_init(LCD_SPI, SPI_WORK_MODE_0, SPI_FF_OCTAL, bits, 0);
    if (data) {
        spi_init_non_standard(LCD_SPI, 0, bits, 0, SPI_AITM_AS_FRAME_FORMAT);
    } else {
        spi_init_non_standard(LCD_SPI, 8, 0, 0, SPI_AITM_AS_FRAME_FORMAT);
    }
}

static void bus_wait_idle(void) {
    volatile spi_t *s = spi[LCD_SPI];
    while ((s->sr & 0x05) != 0x04) { // TX FIFO empty, not busy
    }
    s->ser = 0;
    s->ssienr = 0;
}

// Waits for the frame in flight, if any, to be sent
static void lcd_wait_frame(void) {
    if (dma_busy) {
        dmac_wait_done(LCD_DMA);
        bus_wait_idle();
        dma_busy = false;
    }
}

// Up to LCD_FIFO_DEPTH words from the CPU, the FIFO filled before the transfer
// starts so that it cannot run dry halfway. The SDK's DMA moves 4 words at a
// time, and a shorter transfer (a command) would go out with stray words.
static void bus_fifo(const uint32_t *words, uint32_t len) {
    volatile spi_t *s = spi[LCD_SPI];
    s->ctrlr0 = (s->ctrlr0 & ~(3U << 8)) | (SPI_TMOD_TRANS << 8); // transmit only
    s->dmacr = 0;
    s->ssienr = 1;
    for (uint32_t i = 0; i < len; i++) {
        s->dr[0] = words[i];
    }
    s->ser = 1U << LCD_SS;
    bus_wait_idle();
}

// Starts sending len words (a multiple of 4) by DMA; lcd_wait_frame() ends it
static void bus_dma_start(const uint32_t *words, uint32_t len) {
    volatile spi_t *s = spi[LCD_SPI];
    s->ctrlr0 = (s->ctrlr0 & ~(3U << 8)) | (SPI_TMOD_TRANS << 8);
    s->dmacr = 0x2; // DMA transmit
    s->ssienr = 1;
    sysctl_dma_select((sysctl_dma_channel_t)LCD_DMA, SYSCTL_DMA_SELECT_SSI0_TX_REQ);
    dmac_set_single_mode(LCD_DMA, words, (void *)&s->dr[0], DMAC_ADDR_INCREMENT, DMAC_ADDR_NOCHANGE,
        DMAC_MSIZE_4, DMAC_TRANS_WIDTH_32, len);
    s->ser = 1U << LCD_SS;
    dma_busy = true;
}

static void write_command(uint8_t cmd, const uint8_t *data, uint8_t len) {
    uint32_t words[LCD_FIFO_DEPTH];
    lcd_wait_frame();
    words[0] = cmd;
    bus_config(false, 8);
    bus_fifo(words, 1);
    if (len) {
        for (uint8_t i = 0; i < len; i++) {
            words[i] = data[i];
        }
        bus_config(true, 8);
        bus_fifo(words, len);
    }
}

static int lcd_width(void) {
    return (lcd_rotation & 1) ? PANEL_SHORT : PANEL_LONG;
}

static int lcd_height(void) {
    return (lcd_rotation & 1) ? PANEL_LONG : PANEL_SHORT;
}

static void lcd_set_window(void) {
    uint8_t data[4] = {0, 0, (lcd_width() - 1) >> 8, (lcd_width() - 1) & 0xFF};
    write_command(CMD_COLUMN_ADDR_SET, data, 4);
    data[2] = (lcd_height() - 1) >> 8;
    data[3] = (lcd_height() - 1) & 0xFF;
    write_command(CMD_PAGE_ADDR_SET, data, 4);
}

// Sends frame buffer i, whole
static void lcd_send_frame(int i) {
    lcd_set_window();
    write_command(CMD_MEMORY_WRITE, NULL, 0);
    bus_config(true, 32);
    bus_dma_start(frame_buffer(i), FB_WORDS);
}

static void lcd_init(void) {
    route_pins();
    // The data lines are the DVP's: SPI0 drives them in octal mode
    sysctl_set_spi0_dvp_data(1);

    int rst_channel = machine_pin_gpio_channel(LCD_PIN_RST);
    dcx_channel = machine_pin_gpio_channel(LCD_PIN_DCX);
    gpiohs_set_drive_mode(dcx_channel, GPIO_DM_OUTPUT);
    gpiohs_set_pin(dcx_channel, GPIO_PV_HIGH);
    gpiohs_set_drive_mode(rst_channel, GPIO_DM_OUTPUT);
    gpiohs_set_pin(rst_channel, GPIO_PV_LOW);
    spi_init(LCD_SPI, SPI_WORK_MODE_0, SPI_FF_OCTAL, 8, 0);
    spi_set_clk_rate(LCD_SPI, LCD_FREQ);
    mp_hal_delay_ms(50);
    gpiohs_set_pin(rst_channel, GPIO_PV_HIGH);
    mp_hal_delay_ms(50);

    // MaixPy-v1's sequence for the Amigo IPS panel (its "amigo_ips" config:
    // ILI9481, inverted): power setting, VCOM, sleep out, 16-bit pixels
    static const uint8_t power[] = {0x07, 0x42, 0x1B};
    static const uint8_t vcom[] = {0x00, 0x05, 0x0C};
    static const uint8_t pixfmt = 0x55;
    write_command(CMD_SOFTWARE_RESET, NULL, 0);
    mp_hal_delay_ms(50);
    write_command(CMD_POWER_SETTING, power, sizeof(power));
    write_command(CMD_VCOM_CONTROL, vcom, sizeof(vcom));
    write_command(CMD_SLEEP_OFF, NULL, 0);
    mp_hal_delay_ms(120);
    write_command(CMD_PIXEL_FORMAT, &pixfmt, 1);
    mp_hal_delay_ms(10);
    write_command(CMD_MEMORY_ACCESS, &rotation_madctl[lcd_rotation], 1);
    // The panel shows inverted colors unless the controller's inversion is on
    write_command(CMD_INVERSION_ON, NULL, 0);
    write_command(CMD_NORMAL_DISP_ON, NULL, 0);

    memset(frame_buffer(0), 0, sizeof(fb_mem[0]));
    lcd_send_frame(0);
    write_command(CMD_DISPLAY_ON, NULL, 0);
    back = 1;
    lcd_ready = true;
}

// LCD(rotation=0): rotation 0 to 3, a quarter turn each, 0 being landscape
// (480x320)
static mp_obj_t k210_lcd_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 1, false);
    int rotation = n_args ? mp_obj_get_int(args[0]) & 3 : 0;
    if (!lcd_ready) {
        lcd_rotation = rotation;
        lcd_init();
    } else if (rotation != lcd_rotation) {
        lcd_rotation = rotation;
        write_command(CMD_MEMORY_ACCESS, &rotation_madctl[lcd_rotation], 1);
    }
    return MP_OBJ_FROM_PTR(&k210_lcd_obj);
}

// size(): (width, height) for the rotation
static mp_obj_t k210_lcd_size(mp_obj_t self_in) {
    mp_obj_t size[2] = {MP_OBJ_NEW_SMALL_INT(lcd_width()), MP_OBJ_NEW_SMALL_INT(lcd_height())};
    return mp_obj_new_tuple(2, size);
}
static MP_DEFINE_CONST_FUN_OBJ_1(k210_lcd_size_obj, k210_lcd_size);

// show(buf): sends a whole RGB565 picture (framebuf.RGB565's layout, width x
// height x 2 bytes); returns while the DMA sends it
static mp_obj_t k210_lcd_show(mp_obj_t self_in, mp_obj_t buf_in) {
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buf_in, &bufinfo, MP_BUFFER_READ);
    if (bufinfo.len != sizeof(fb_mem[0])) {
        mp_raise_ValueError(MP_ERROR_TEXT("buffer must be width * height * 2 bytes"));
    }
    // framebuf keeps two pixels to a word, the left one in the low half; the
    // bus sends a word's high half first, each pixel high byte first
    const uint32_t *src = bufinfo.buf;
    uint32_t *dst = frame_buffer(back);
    for (size_t i = 0; i < FB_WORDS; i++) {
        uint32_t w = src[i];
        dst[i] = (w << 16) | (w >> 16);
    }
    lcd_wait_frame();
    lcd_send_frame(back);
    back ^= 1;
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(k210_lcd_show_obj, k210_lcd_show);

// on(): the screen back on after off(), blank until the next show()
static mp_obj_t k210_lcd_on(mp_obj_t self_in) {
    if (!lcd_ready) {
        lcd_init();
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(k210_lcd_on_obj, k210_lcd_on);

// The screen off: the controller asleep, then held in reset, which turns the
// backlight off too (60 mA, half of what the Amigo draws asleep)
void k210_lcd_power_off(void) {
    if (lcd_ready) {
        lcd_wait_frame();
        write_command(CMD_DISPLAY_OFF, NULL, 0);
        write_command(CMD_SLEEP_IN, NULL, 0);
        lcd_ready = false;
    }
    mp_hal_pin_output(LCD_PIN_RST);
    mp_hal_pin_write(LCD_PIN_RST, 0);
}

// off(): the screen and its backlight off, until on()
static mp_obj_t k210_lcd_off(mp_obj_t self_in) {
    k210_lcd_power_off();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(k210_lcd_off_obj, k210_lcd_off);

static const mp_rom_map_elem_t k210_lcd_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_size), MP_ROM_PTR(&k210_lcd_size_obj) },
    { MP_ROM_QSTR(MP_QSTR_show), MP_ROM_PTR(&k210_lcd_show_obj) },
    { MP_ROM_QSTR(MP_QSTR_on), MP_ROM_PTR(&k210_lcd_on_obj) },
    { MP_ROM_QSTR(MP_QSTR_off), MP_ROM_PTR(&k210_lcd_off_obj) },
};
static MP_DEFINE_CONST_DICT(k210_lcd_locals_dict, k210_lcd_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    k210_lcd_type,
    MP_QSTR_LCD,
    MP_TYPE_FLAG_NONE,
    make_new, k210_lcd_make_new,
    locals_dict, &k210_lcd_locals_dict
    );
