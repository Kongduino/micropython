// k210.Camera: the Amigo's rear camera (OmniVision OV7740) on the K210's DVP
// camera interface, QVGA (320x240). The frozen camera.py puts framebufs in
// front of it.
//
// The driver is the Meshtastic K210 port's (AmigoCamera.cpp): the OV7740's
// registers go through I2C2 (IO40/IO41), as the DVP's own SCCB controller
// reaches only the front camera (GC0328), and the DVP's PWDN line picks one or
// the other. The DVP writes each frame twice, into RAM behind the CPU's cache:
// RGB565 (for the screen) and planar R, G, B (the G plane serves as
// greyscale). Frames are read through the uncached alias.

#include <string.h>

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"

#include "dvp.h"
#include "fpioa.h"
#include "i2c.h"
#include "plic.h"
#include "sysctl.h"

#define WIDTH (320)
#define HEIGHT (240)
#define CAPTURE_TIMEOUT_MS (300)

// The DVP's pins (MaixPy-v1's, which the Amigo uses)
#define CAM_PIN_SDA (40)
#define CAM_PIN_SCL (41)
#define CAM_PIN_RST (42)
#define CAM_PIN_VSYNC (43)
#define CAM_PIN_PWDN (44)
#define CAM_PIN_HREF (45)
#define CAM_PIN_XCLK (46)
#define CAM_PIN_PCLK (47)

#define OV7740_ADDR (0x21)
#define OV7740_REG_PID (0x0A)
#define OV7740_REG_VER (0x0B)
#define OV7740_PID (0x77)
#define OV7740_XCLK (22000000) // MaixPy's rate for the OV7740

// DVP control bits, named as in the SDK. On the Amigo, with the PWDN bit set
// the OV7740 runs and the GC0328 is held powered down; the OV7740 runs with
// the RESET bit set.
#define CAM_RESET_LOW() (dvp->cmos_cfg &= ~DVP_CMOS_RESET)
#define CAM_RESET_HIGH() (dvp->cmos_cfg |= DVP_CMOS_RESET)
#define CAM_SELECT_OV7740() (dvp->cmos_cfg |= DVP_CMOS_POWER_DOWN)
#define CAM_SELECT_GC0328() (dvp->cmos_cfg &= ~DVP_CMOS_POWER_DOWN)

// OV7740 setup from MaixPy-v1's ov7740.c (OpenMV, MIT licence): YUYV, QVGA
static const uint8_t ov7740_regs[][2] = {
    {0x47, 0x02}, {0x17, 0x27}, {0x04, 0x40}, {0x1B, 0x81}, {0x29, 0x17}, {0x5F, 0x03}, {0x3A, 0x09}, {0x33, 0x44},
    {0x68, 0x1A}, {0x14, 0x38}, {0x5F, 0x04}, {0x64, 0x00}, {0x67, 0x90}, {0x27, 0x80}, {0x45, 0x41}, {0x4B, 0x40},
    {0x36, 0x2f}, {0x11, 0x00}, {0x36, 0x3f}, {0x12, 0x00}, {0x17, 0x25}, {0x18, 0xa0}, {0x1a, 0xf0}, {0x31, 0x50},
    {0x32, 0x78}, {0x82, 0x3f}, {0x85, 0x08}, {0x86, 0x02}, {0x87, 0x01}, {0xd5, 0x10}, {0x0d, 0x34}, {0x19, 0x03},
    {0x2b, 0xf8}, {0x2c, 0x01}, {0x53, 0x00}, {0x89, 0x30}, {0x8d, 0x30}, {0x8f, 0x85}, {0x93, 0x30}, {0x95, 0x85},
    {0x99, 0x30}, {0x9b, 0x85}, {0xac, 0x6E}, {0xbe, 0xff}, {0xbf, 0x00}, {0x38, 0x14}, {0xe9, 0x00}, {0x3D, 0x08},
    {0x3E, 0x80}, {0x3F, 0x40}, {0x40, 0x7F}, {0x41, 0x6A}, {0x42, 0x29}, {0x49, 0x64}, {0x4A, 0xA1}, {0x4E, 0x13},
    {0x4D, 0x50}, {0x44, 0x58}, {0x4C, 0x1A}, {0x4E, 0x14}, {0x38, 0x11}, {0x84, 0x70},
};

static uint32_t display_mem[WIDTH * HEIGHT / 2] __attribute__((aligned(64)));
static uint8_t ai_mem[WIDTH * HEIGHT * 3] __attribute__((aligned(64)));
#define UNCACHED(p) ((uintptr_t)(p) - 0x40000000)

// Capture state: a frame is converted from the start of the next one after
// it's wanted, and done at that frame's end
enum {
    CAPTURE_IDLE,
    CAPTURE_WANTED,
    CAPTURE_CONVERTING,
    CAPTURE_DONE,
};
static volatile uint8_t capture_state = CAPTURE_IDLE;
static bool camera_on;

typedef struct _k210_camera_obj_t {
    mp_obj_base_t base;
} k210_camera_obj_t;

extern const mp_obj_type_t k210_camera_type;
static const k210_camera_obj_t k210_camera_obj = {{&k210_camera_type}};

static int dvp_irq(void *ctx) {
    if (dvp_get_interrupt(DVP_STS_FRAME_FINISH)) {
        dvp_clear_interrupt(DVP_STS_FRAME_FINISH);
        if (capture_state == CAPTURE_CONVERTING) {
            capture_state = CAPTURE_DONE;
        }
    } else {
        if (capture_state == CAPTURE_WANTED) {
            dvp_start_convert();
            capture_state = CAPTURE_CONVERTING;
        }
        dvp_clear_interrupt(DVP_STS_FRAME_START);
    }
    return 0;
}

static void sccb_write(uint8_t reg, uint8_t value) {
    uint8_t buf[2] = {reg, value};
    i2c_send_data(I2C_DEVICE_2, buf, sizeof(buf));
}

static int sccb_read(uint8_t reg) {
    uint8_t value;
    if (i2c_send_data(I2C_DEVICE_2, &reg, 1) != 0 || i2c_recv_data(I2C_DEVICE_2, NULL, 0, &value, 1) != 0) {
        return -1;
    }
    return value;
}

static void camera_stop(void) {
    if (!camera_on) {
        return;
    }
    plic_irq_disable(IRQN_DVP_INTERRUPT);
    dvp_config_interrupt(DVP_CFG_START_INT_ENABLE | DVP_CFG_FINISH_INT_ENABLE, 0);
    dvp_clear_interrupt(DVP_STS_FRAME_START | DVP_STS_FRAME_FINISH);
    CAM_SELECT_GC0328(); // the OV7740 powered down
    capture_state = CAPTURE_IDLE;
    camera_on = false;
}

// Turns the camera off at a soft reset
void k210_camera_deinit(void) {
    camera_stop();
}

static void camera_start(void) {
    machine_pin_set_function(CAM_PIN_PCLK, FUNC_CMOS_PCLK);
    machine_pin_set_function(CAM_PIN_XCLK, FUNC_CMOS_XCLK);
    machine_pin_set_function(CAM_PIN_HREF, FUNC_CMOS_HREF);
    machine_pin_set_function(CAM_PIN_PWDN, FUNC_CMOS_PWDN);
    machine_pin_set_function(CAM_PIN_VSYNC, FUNC_CMOS_VSYNC);
    machine_pin_set_function(CAM_PIN_RST, FUNC_CMOS_RST);
    machine_pin_set_function(CAM_PIN_SCL, FUNC_I2C2_SCLK);
    machine_pin_set_function(CAM_PIN_SDA, FUNC_I2C2_SDA);
    i2c_init(I2C_DEVICE_2, OV7740_ADDR, 7, 100000);

    dvp_init(8);
    dvp_set_xclk_rate(OV7740_XCLK);
    // The DVP's data lines are the pads the screen's octal SPI0 uses; the
    // pixels come through with them given to SPI0, as the screen's driver
    // sets it (the Meshtastic port's camera always ran after the screen)
    sysctl_set_spi0_dvp_data(1);

    // Select the OV7740, power it up and take it out of reset
    CAM_SELECT_OV7740();
    CAM_RESET_LOW();
    mp_hal_delay_ms(10);
    CAM_RESET_HIGH();
    mp_hal_delay_ms(30);
    int pid = sccb_read(OV7740_REG_PID);
    if (pid != OV7740_PID) {
        CAM_SELECT_GC0328();
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("no OV7740 camera"));
    }

    sccb_write(0x12, 0x80); // reset all registers
    mp_hal_delay_ms(10);
    for (size_t i = 0; i < MP_ARRAY_SIZE(ov7740_regs); i++) {
        sccb_write(ov7740_regs[i][0], ov7740_regs[i][1]);
        mp_hal_delay_ms(2); // MaixPy waits between writes to an OV sensor
    }
    // The camera is mounted upside down, but the sensor's own mirror and flip
    // shift its colour filter pattern (green comes out magenta), so frames
    // are turned the right way up as they're copied out instead

    dvp_set_image_format(DVP_CFG_YUV_FORMAT);
    dvp_disable_burst();
    dvp_disable_auto();
    dvp_set_output_enable(DVP_OUTPUT_AI, 1);
    dvp_set_output_enable(DVP_OUTPUT_DISPLAY, 1);
    dvp_set_image_size(WIDTH, HEIGHT);
    // The buffers' cached addresses, as the Meshtastic port gives them, set
    // directly (this SDK's dvp_set_ai_addr() refuses them)
    uint32_t ai = (uint32_t)(uintptr_t)ai_mem;
    dvp->r_addr = ai;
    dvp->g_addr = ai + WIDTH * HEIGHT;
    dvp->b_addr = ai + WIDTH * HEIGHT * 2;
    dvp->rgb_addr = (uint32_t)(uintptr_t)display_mem;

    dvp_config_interrupt(DVP_CFG_START_INT_ENABLE | DVP_CFG_FINISH_INT_ENABLE, 0);
    plic_set_priority(IRQN_DVP_INTERRUPT, 2);
    plic_irq_register(IRQN_DVP_INTERRUPT, dvp_irq, NULL);
    dvp_clear_interrupt(DVP_STS_FRAME_START | DVP_STS_FRAME_FINISH);
    dvp_config_interrupt(DVP_CFG_START_INT_ENABLE | DVP_CFG_FINISH_INT_ENABLE, 1);
    plic_irq_enable(IRQN_DVP_INTERRUPT);
    camera_on = true;
}

// Waits for the next whole frame
static void camera_capture(void) {
    if (!camera_on) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("camera is off"));
    }
    capture_state = CAPTURE_WANTED;
    mp_uint_t start = mp_hal_ticks_ms();
    while (capture_state != CAPTURE_DONE) {
        if (mp_hal_ticks_ms() - start > CAPTURE_TIMEOUT_MS) {
            capture_state = CAPTURE_IDLE;
            mp_raise_OSError(MP_ETIMEDOUT);
        }
        mp_handle_pending(true);
    }
    capture_state = CAPTURE_IDLE;
}

// Camera(): powers the camera up (OSError if it doesn't answer)
static mp_obj_t k210_camera_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 0, false);
    if (!camera_on) {
        camera_start();
    }
    return MP_OBJ_FROM_PTR(&k210_camera_obj);
}

static void get_out(mp_obj_t buf_in, size_t len, mp_buffer_info_t *bufinfo) {
    mp_get_buffer_raise(buf_in, bufinfo, MP_BUFFER_WRITE);
    if (bufinfo->len != len) {
        mp_raise_ValueError(MP_ERROR_TEXT("wrong buffer size"));
    }
}

// rgb565(buf): the next frame into buf, 320x240 in framebuf.RGB565's layout
static mp_obj_t k210_camera_rgb565(mp_obj_t self_in, mp_obj_t buf_in) {
    mp_buffer_info_t bufinfo;
    get_out(buf_in, WIDTH * HEIGHT * 2, &bufinfo);
    camera_capture();
    // Turned by 180 degrees: the pixels in reverse order. The DVP puts the
    // left pixel of a pair in a word's high half, framebuf in the low half,
    // so the words go in reverse order as they are
    const uint32_t *src = (const uint32_t *)UNCACHED(display_mem);
    uint32_t *dst = (uint32_t *)bufinfo.buf + WIDTH * HEIGHT / 2;
    for (size_t i = 0; i < WIDTH * HEIGHT / 2; i++) {
        *--dst = src[i];
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(k210_camera_rgb565_obj, k210_camera_rgb565);

// grey(buf): the next frame's green plane into buf, 320x240, one byte a pixel
// (framebuf.GS8's layout)
static mp_obj_t k210_camera_grey(mp_obj_t self_in, mp_obj_t buf_in) {
    mp_buffer_info_t bufinfo;
    get_out(buf_in, WIDTH * HEIGHT, &bufinfo);
    camera_capture();
    // Turned by 180 degrees, as rgb565()
    const uint8_t *src = (const uint8_t *)UNCACHED(ai_mem) + WIDTH * HEIGHT;
    uint8_t *dst = (uint8_t *)bufinfo.buf + WIDTH * HEIGHT;
    for (size_t i = 0; i < WIDTH * HEIGHT; i++) {
        *--dst = src[i];
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(k210_camera_grey_obj, k210_camera_grey);

// reg(addr[, value]): reads or writes one of the OV7740's registers
static mp_obj_t k210_camera_reg(size_t n_args, const mp_obj_t *args) {
    uint8_t reg = mp_obj_get_int(args[1]);
    if (n_args == 3) {
        sccb_write(reg, mp_obj_get_int(args[2]));
        return mp_const_none;
    }
    int value = sccb_read(reg);
    if (value < 0) {
        mp_raise_OSError(MP_EIO);
    }
    return MP_OBJ_NEW_SMALL_INT(value);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(k210_camera_reg_obj, 2, 3, k210_camera_reg);

static mp_obj_t k210_camera_off(mp_obj_t self_in) {
    camera_stop();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(k210_camera_off_obj, k210_camera_off);

static const mp_rom_map_elem_t k210_camera_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_rgb565), MP_ROM_PTR(&k210_camera_rgb565_obj) },
    { MP_ROM_QSTR(MP_QSTR_grey), MP_ROM_PTR(&k210_camera_grey_obj) },
    { MP_ROM_QSTR(MP_QSTR_reg), MP_ROM_PTR(&k210_camera_reg_obj) },
    { MP_ROM_QSTR(MP_QSTR_off), MP_ROM_PTR(&k210_camera_off_obj) },
    { MP_ROM_QSTR(MP_QSTR_WIDTH), MP_ROM_INT(WIDTH) },
    { MP_ROM_QSTR(MP_QSTR_HEIGHT), MP_ROM_INT(HEIGHT) },
};
static MP_DEFINE_CONST_DICT(k210_camera_locals_dict, k210_camera_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    k210_camera_type,
    MP_QSTR_Camera,
    MP_TYPE_FLAG_NONE,
    make_new, k210_camera_make_new,
    locals_dict, &k210_camera_locals_dict
    );
