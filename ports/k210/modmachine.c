// The port's part of the machine module, included by extmod/modmachine.c

#include "py/mperrno.h"

#include "encoding.h"
#include "sysctl.h"
#include "k210_flash.h"

static void mp_machine_idle(void) {
    asm volatile ("wfi");
}

MP_NORETURN static void mp_machine_reset(void) {
    sysctl->soft_reset.soft_reset = 1;
    for (;;) {
    }
}

// Why the chip started. The SDK's start-up code reads (and clears) the
// system controller's reset status, and keeps it: a watchdog, a software
// reset, or else a power-on or the reset line, which it doesn't tell apart
// (PWRON_RESET, as rp2 reports its RUN pin). A deep sleep's reset is told
// from machine.reset() by a mark it leaves in one of the power chip's data
// registers, which keep their value while it has power.
enum {
    PWRON_RESET = 1,
    WDT_RESET = 3,
    DEEPSLEEP_RESET,
    SOFT_RESET,
};
#define AXP173_ADDR (0x34)
#define AXP173_REG_SHUTDOWN (0x32) // bit 7: power off
#define AXP173_REG_DATA (0x0B) // the last of the data buffer, 0x06-0x0B
#define DEEPSLEEP_MARK (0xD5)

static uint8_t reset_cause;

void k210_reset_cause_init(void) {
    switch (sysctl_get_reset_status()) {
        case SYSCTL_RESET_STATUS_WDT0:
        case SYSCTL_RESET_STATUS_WDT1:
            reset_cause = WDT_RESET;
            break;
        case SYSCTL_RESET_STATUS_SOFT:
            reset_cause = SOFT_RESET;
            break;
        default:
            reset_cause = PWRON_RESET;
            break;
    }
    if (k210_i2c0_read_reg(AXP173_ADDR, AXP173_REG_DATA) == DEEPSLEEP_MARK) {
        k210_i2c0_write_reg(AXP173_ADDR, AXP173_REG_DATA, 0);
        if (reset_cause == SOFT_RESET) {
            reset_cause = DEEPSLEEP_RESET;
        }
    }
}

static mp_int_t mp_machine_reset_cause(void) {
    return reset_cause;
}

// The flash chip's 64-bit unique ID: the K210 has none of its own that the
// SDK reads
static mp_obj_t mp_machine_unique_id(void) {
    uint8_t uid[8];
    if (!k210_flash_unique_id(uid)) {
        mp_raise_OSError(MP_EIO);
    }
    return mp_obj_new_bytes(uid, sizeof(uid));
}

static mp_obj_t mp_machine_get_freq(void) {
    return mp_obj_new_int(sysctl_clock_get_freq(SYSCTL_CLOCK_CPU));
}

static void mp_machine_set_freq(size_t n_args, const mp_obj_t *args) {
    mp_raise_NotImplementedError(NULL);
}

// lightsleep([ms]): the CPU slowed to the oscillator until the time is up
// or an interrupt (a pin, a Timer, the REPL's UART...) comes; its handler
// then runs, and lightsleep() returns
static void mp_machine_lightsleep(size_t n_args, const mp_obj_t *args) {
    mp_int_t ms = n_args ? mp_obj_get_int(args[0]) : -1;
    if (ms == 0) {
        return;
    }
    k210_lightsleep(ms < 0 ? K210_SLEEP_FOREVER : (uint64_t)ms, true);
    mp_handle_pending(true);
}

// deepsleep([ms]): the screen (and its backlight) and the camera off, then
// a light sleep that interrupts don't end, then a reset (reset_cause() gives
// DEEPSLEEP_RESET). With no time, the power chip turns the Amigo off (the
// power button turns it on); if it stays on (as it may on USB power), it
// sleeps until a reset.
MP_NORETURN static void mp_machine_deepsleep(size_t n_args, const mp_obj_t *args) {
    mp_int_t ms = n_args ? mp_obj_get_int(args[0]) : -1;
    k210_lcd_power_off();
    k210_camera_deinit();
    if (ms < 0) {
        int reg = k210_i2c0_read_reg(AXP173_ADDR, AXP173_REG_SHUTDOWN);
        if (reg >= 0) {
            k210_i2c0_write_reg(AXP173_ADDR, AXP173_REG_SHUTDOWN, reg | 0x80);
            mp_hal_delay_ms(500);
        }
        k210_lightsleep(K210_SLEEP_FOREVER, false);
    } else {
        k210_i2c0_write_reg(AXP173_ADDR, AXP173_REG_DATA, DEEPSLEEP_MARK);
        k210_lightsleep(ms, false);
    }
    mp_machine_reset();
}
