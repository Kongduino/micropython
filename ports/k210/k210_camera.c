// k210.Camera: the Amigo's rear camera (OmniVision OV7740) or its front one
// (GalaxyCore GC0328) on the K210's DVP camera interface, QVGA (320x240). The
// frozen camera.py puts framebufs in front of it.
//
// The rear camera's driver is the Meshtastic K210 port's (AmigoCamera.cpp).
// Both cameras sit on the DVP's data lines and on I2C2 (IO40/IO41), at the
// same address; the DVP's PWDN line powers one and holds the other down, so
// one runs at a time. The DVP writes each frame twice, into RAM behind the
// CPU's cache: RGB565 (for the screen) and planar R, G, B (the G plane serves
// as greyscale). Frames are read through the uncached alias, and turned as
// they're copied out so they're upright with the Amigo held upright.

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
#define GC0328_REG_ID (0xF0)
#define GC0328_ID (0x9D)
#define GC0328_XCLK (24000000) // MaixPy's default rate

// DVP control bits, named as in the SDK. On the Amigo, with the PWDN bit set
// the OV7740 runs and the GC0328 is held powered down, and the other way
// round with it clear; the OV7740 runs with the RESET bit set.
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

// GC0328 setup from MaixPy-v1's gc0328.c (Canaan, Apache licence): its
// default registers (with the gamma curves it builds with), then its QVGA
// window, subsampled by 2 from VGA
static const uint8_t gc0328_regs[][2] = {
    {0xFE, 0x80}, {0xFE, 0x80}, {0xFC, 0x16}, {0xFC, 0x16}, {0xFC, 0x16}, {0xFC, 0x16}, {0xFE, 0x00}, {0x4F, 0x00},
    {0x42, 0x00}, {0x03, 0x00}, {0x04, 0xC0}, {0x77, 0x62}, {0x78, 0x40}, {0x79, 0x4D}, {0x05, 0x00}, {0x06, 0x80},
    {0x07, 0x00}, {0x08, 0x10}, {0xFE, 0x01}, {0x29, 0x00}, {0x2A, 0x96}, {0x2B, 0x02}, {0x2C, 0x00}, {0x2D, 0x02},
    {0x2E, 0x00}, {0x2F, 0x02}, {0x30, 0x00}, {0x31, 0x02}, {0x32, 0x00}, {0xFE, 0x00}, {0xFE, 0x01}, {0x4F, 0x00},
    {0x4C, 0x01}, {0xFE, 0x00}, {0xFE, 0x01}, {0x51, 0x80}, {0x52, 0x12}, {0x53, 0x80}, {0x54, 0x60}, {0x55, 0x01},
    {0x56, 0x06}, {0x5B, 0x02}, {0x61, 0xDC}, {0x62, 0xDC}, {0x7C, 0x71}, {0x7D, 0x00}, {0x76, 0x00}, {0x79, 0x20},
    {0x7B, 0x00}, {0x70, 0xFF}, {0x71, 0x00}, {0x72, 0x10}, {0x73, 0x40}, {0x74, 0x40}, {0x50, 0x00}, {0xFE, 0x01},
    {0x4F, 0x00}, {0x4C, 0x01}, {0x4F, 0x00}, {0x4F, 0x00}, {0x4F, 0x00}, {0x4D, 0x36}, {0x4E, 0x02}, {0x4E, 0x02},
    {0x4D, 0x44}, {0x4E, 0x02}, {0x4E, 0x02}, {0x4E, 0x02}, {0x4E, 0x02}, {0x4D, 0x53}, {0x4E, 0x08}, {0x4E, 0x08},
    {0x4E, 0x02}, {0x4D, 0x63}, {0x4E, 0x08}, {0x4E, 0x08}, {0x4D, 0x73}, {0x4E, 0x20}, {0x4D, 0x83}, {0x4E, 0x20},
    {0x4F, 0x01}, {0x50, 0x88}, {0xFE, 0x00}, {0x27, 0x00}, {0x2A, 0x40}, {0x2B, 0x40}, {0x2C, 0x40}, {0x2D, 0x40},
    {0xFE, 0x00}, {0x0D, 0x01}, {0x0E, 0xE8}, {0x0F, 0x02}, {0x10, 0x88}, {0x09, 0x00}, {0x0A, 0x00}, {0x0B, 0x00},
    {0x0C, 0x00}, {0x16, 0x00}, {0x17, 0x14}, {0x18, 0x0E}, {0x19, 0x06}, {0x1B, 0x48}, {0x1F, 0xC8}, {0x20, 0x01},
    {0x21, 0x78}, {0x22, 0xB0}, {0x23, 0x04}, {0x24, 0x11}, {0x26, 0x00}, {0x50, 0x01}, {0x51, 0x00}, {0x52, 0x00},
    {0x53, 0x00}, {0x54, 0x00}, {0x55, 0x00}, {0x56, 0xF0}, {0x57, 0x01}, {0x58, 0x40}, {0x59, 0x22}, {0x5A, 0x03},
    {0x5B, 0x00}, {0x5C, 0x00}, {0x5D, 0x00}, {0x5E, 0x00}, {0x5F, 0x00}, {0x60, 0x00}, {0x61, 0x00}, {0x62, 0x00},
    {0x70, 0x85}, {0x40, 0x7F}, {0x41, 0x26}, {0x42, 0xFF}, {0x45, 0x00}, {0x44, 0x00}, {0x46, 0x03}, {0x4B, 0x01},
    {0x50, 0x01}, {0x7E, 0x0A}, {0x7F, 0x03}, {0x80, 0x27}, {0x81, 0x15}, {0x82, 0x90}, {0x83, 0x02}, {0x84, 0x23},
    {0x90, 0x2C}, {0x92, 0x02}, {0x94, 0x02}, {0x95, 0x35}, {0xD1, 0x32}, {0xD2, 0x32}, {0xDD, 0x18}, {0xDE, 0x32},
    {0xE4, 0x88}, {0xE5, 0x40}, {0xD7, 0x0E}, {0xFE, 0x00}, {0xBF, 0x0E}, {0xC0, 0x1C}, {0xC1, 0x34}, {0xC2, 0x48},
    {0xC3, 0x5A}, {0xC4, 0x6B}, {0xC5, 0x7B}, {0xC6, 0x95}, {0xC7, 0xAB}, {0xC8, 0xBF}, {0xC9, 0xCE}, {0xCA, 0xD9},
    {0xCB, 0xE4}, {0xCC, 0xEC}, {0xCD, 0xF7}, {0xCE, 0xFD}, {0xCF, 0xFF}, {0xFE, 0x00}, {0x63, 0x00}, {0x64, 0x49},
    {0x65, 0x68}, {0x66, 0x80}, {0x67, 0x93}, {0x68, 0xA5}, {0x69, 0xB5}, {0x6A, 0xC3}, {0x6B, 0xD1}, {0x6C, 0xDD},
    {0x6D, 0xE9}, {0x6E, 0xF5}, {0x6F, 0xFF}, {0xFE, 0x01}, {0x18, 0x02}, {0xFE, 0x00}, {0x98, 0x00}, {0x9B, 0x20},
    {0x9C, 0x80}, {0xA4, 0x10}, {0xA8, 0xB0}, {0xAA, 0x40}, {0xA2, 0x23}, {0xAD, 0x01}, {0xFE, 0x01}, {0x9C, 0x02},
    {0x08, 0xA0}, {0x09, 0xE8}, {0x10, 0x00}, {0x11, 0x11}, {0x12, 0x10}, {0x13, 0x80}, {0x15, 0xFC}, {0x18, 0x03},
    {0x21, 0xC0}, {0x22, 0x60}, {0x23, 0x30}, {0x25, 0x00}, {0x24, 0x14}, {0xFE, 0x01}, {0xC0, 0x10}, {0xC1, 0x0C},
    {0xC2, 0x0A}, {0xC6, 0x0E}, {0xC7, 0x0B}, {0xC8, 0x0A}, {0xBA, 0x26}, {0xBB, 0x1C}, {0xBC, 0x1D}, {0xB4, 0x23},
    {0xB5, 0x1C}, {0xB6, 0x1A}, {0xC3, 0x00}, {0xC4, 0x00}, {0xC5, 0x00}, {0xC9, 0x00}, {0xCA, 0x00}, {0xCB, 0x00},
    {0xBD, 0x00}, {0xBE, 0x00}, {0xBF, 0x00}, {0xB7, 0x07}, {0xB8, 0x05}, {0xB9, 0x05}, {0xA8, 0x07}, {0xA9, 0x06},
    {0xAA, 0x00}, {0xAB, 0x04}, {0xAC, 0x00}, {0xAD, 0x02}, {0xAE, 0x0D}, {0xAF, 0x05}, {0xB0, 0x00}, {0xB1, 0x07},
    {0xB2, 0x03}, {0xB3, 0x00}, {0xA4, 0x00}, {0xA5, 0x00}, {0xA6, 0x00}, {0xA7, 0x00}, {0xA1, 0x3C}, {0xA2, 0x50},
    {0xFE, 0x00}, {0xB1, 0x04}, {0xB2, 0xFD}, {0xB3, 0xFC}, {0xB4, 0xF0}, {0xB5, 0x05}, {0xB6, 0xF0}, {0xFE, 0x00},
    {0x27, 0xF7}, {0x28, 0x7F}, {0x29, 0x20}, {0x33, 0x20}, {0x34, 0x20}, {0x35, 0x20}, {0x36, 0x20}, {0x32, 0x08},
    {0x47, 0x00}, {0x48, 0x00}, {0xFE, 0x01}, {0x79, 0x00}, {0x7D, 0x00}, {0x50, 0x88}, {0x5B, 0x0C}, {0x76, 0x8F},
    {0x80, 0x70}, {0x81, 0x70}, {0x82, 0xB0}, {0x70, 0xFF}, {0x71, 0x00}, {0x72, 0x28}, {0x73, 0x0B}, {0x74, 0x0B},
    {0xFE, 0x00}, {0x70, 0x45}, {0x4F, 0x01}, {0xF1, 0x07}, {0xF2, 0x01},
    {0xFE, 0x00}, {0x09, 0x00}, {0x0A, 0x00}, {0x0B, 0x00}, {0x0C, 0x00}, {0x0D, 0x01}, {0x0E, 0xE8}, {0x0F, 0x02},
    {0x10, 0x88}, {0x50, 0x01}, {0x59, 0x22}, {0x5A, 0x00}, {0x5B, 0x00}, {0x5C, 0x00}, {0x5D, 0x00}, {0x5E, 0x00},
    {0x5F, 0x00}, {0x60, 0x00}, {0x61, 0x00}, {0x62, 0x00},
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
static bool camera_front; // the camera running: the GC0328, else the OV7740

// How a frame is turned as it's copied out, so it's upright with the Amigo
// held upright: the sensor's pixel each output pixel takes, at start +
// x * step_x + y * step_y, and the output's size
typedef struct _camera_view_t {
    int32_t start, step_x, step_y;
    uint16_t width, height;
} camera_view_t;
static const camera_view_t camera_views[] = {
    // The rear camera, a quarter turn and upside down: 240x320
    {WIDTH - 1, WIDTH, -1, HEIGHT, WIDTH},
    // The front camera, flipped top to bottom: 320x240
    {(HEIGHT - 1) * WIDTH, 1, -WIDTH, WIDTH, HEIGHT},
};
static const camera_view_t *camera_view;

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

static void camera_write_regs(const uint8_t (*regs)[2], size_t n) {
    for (size_t i = 0; i < n; i++) {
        sccb_write(regs[i][0], regs[i][1]);
        mp_hal_delay_ms(2); // MaixPy waits between writes to a sensor
    }
}

static void camera_start(bool front) {
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
    dvp_set_xclk_rate(front ? GC0328_XCLK : OV7740_XCLK);
    // The DVP's data lines are the pads the screen's octal SPI0 uses; the
    // pixels come through with them given to SPI0, as the screen's driver
    // sets it (the Meshtastic port's camera always ran after the screen)
    sysctl_set_spi0_dvp_data(1);

    // Select the camera, power it up and take it out of reset
    if (front) {
        CAM_SELECT_GC0328();
    } else {
        CAM_SELECT_OV7740();
    }
    CAM_RESET_LOW();
    mp_hal_delay_ms(10);
    CAM_RESET_HIGH();
    mp_hal_delay_ms(30);

    if (front) {
        sccb_write(0xFE, 0x00); // register page 0
        if (sccb_read(GC0328_REG_ID) != GC0328_ID) {
            CAM_SELECT_OV7740();
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("no GC0328 camera"));
        }
        camera_write_regs(gc0328_regs, MP_ARRAY_SIZE(gc0328_regs));
        camera_view = &camera_views[1];
    } else {
        if (sccb_read(OV7740_REG_PID) != OV7740_PID) {
            CAM_SELECT_GC0328();
            mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("no OV7740 camera"));
        }
        sccb_write(0x12, 0x80); // reset all registers
        mp_hal_delay_ms(10);
        camera_write_regs(ov7740_regs, MP_ARRAY_SIZE(ov7740_regs));
        // The sensor's own mirror and flip shift its colour filter pattern
        // (green comes out magenta), so frames are turned as they're copied
        // out instead
        camera_view = &camera_views[0];
    }

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
    camera_front = front;
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

// Camera(front=False): powers the rear camera up, or the front one (OSError
// if it doesn't answer); the other one, if running, is turned off
static mp_obj_t k210_camera_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum { ARG_front };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_front, MP_ARG_BOOL, {.u_bool = false} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    bool front = args[ARG_front].u_bool;
    if (camera_on && camera_front != front) {
        camera_stop();
    }
    if (!camera_on) {
        camera_start(front);
    }
    return MP_OBJ_FROM_PTR(&k210_camera_obj);
}

static void get_out(mp_obj_t buf_in, size_t len, mp_buffer_info_t *bufinfo) {
    mp_get_buffer_raise(buf_in, bufinfo, MP_BUFFER_WRITE);
    if (bufinfo->len != len) {
        mp_raise_ValueError(MP_ERROR_TEXT("wrong buffer size"));
    }
}

// rgb565(buf): the next frame into buf, in framebuf.RGB565's layout, at the
// size size() gives
static mp_obj_t k210_camera_rgb565(mp_obj_t self_in, mp_obj_t buf_in) {
    const camera_view_t *v = camera_view;
    mp_buffer_info_t bufinfo;
    get_out(buf_in, v->width * v->height * 2, &bufinfo);
    camera_capture();
    // The DVP puts the left pixel of a pair in a word's high half: pixel i
    // is half i ^ 1
    const uint16_t *src = (const uint16_t *)UNCACHED(display_mem);
    uint16_t *dst = bufinfo.buf;
    for (int y = 0; y < v->height; y++) {
        int32_t i = v->start + y * v->step_y;
        for (int x = 0; x < v->width; x++, i += v->step_x) {
            *dst++ = src[i ^ 1];
        }
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(k210_camera_rgb565_obj, k210_camera_rgb565);

// grey(buf): the next frame's green plane into buf, one byte a pixel
// (framebuf.GS8's layout), at the size size() gives
static mp_obj_t k210_camera_grey(mp_obj_t self_in, mp_obj_t buf_in) {
    const camera_view_t *v = camera_view;
    mp_buffer_info_t bufinfo;
    get_out(buf_in, v->width * v->height, &bufinfo);
    camera_capture();
    const uint8_t *src = (const uint8_t *)UNCACHED(ai_mem) + WIDTH * HEIGHT;
    uint8_t *dst = bufinfo.buf;
    for (int y = 0; y < v->height; y++) {
        int32_t i = v->start + y * v->step_y;
        for (int x = 0; x < v->width; x++, i += v->step_x) {
            *dst++ = src[i];
        }
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(k210_camera_grey_obj, k210_camera_grey);

// size(): the frames' (width, height)
static mp_obj_t k210_camera_size(mp_obj_t self_in) {
    mp_obj_t t[2] = {MP_OBJ_NEW_SMALL_INT(camera_view->width), MP_OBJ_NEW_SMALL_INT(camera_view->height)};
    return mp_obj_new_tuple(2, t);
}
static MP_DEFINE_CONST_FUN_OBJ_1(k210_camera_size_obj, k210_camera_size);

// reg(addr[, value]): reads or writes one of the running camera's registers
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
    { MP_ROM_QSTR(MP_QSTR_size), MP_ROM_PTR(&k210_camera_size_obj) },
};
static MP_DEFINE_CONST_DICT(k210_camera_locals_dict, k210_camera_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    k210_camera_type,
    MP_QSTR_Camera,
    MP_TYPE_FLAG_NONE,
    make_new, k210_camera_make_new,
    locals_dict, &k210_camera_locals_dict
    );
