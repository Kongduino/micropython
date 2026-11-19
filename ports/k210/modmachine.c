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

static mp_int_t mp_machine_reset_cause(void) {
    return 0;
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

static void mp_machine_lightsleep(size_t n_args, const mp_obj_t *args) {
    if (n_args == 0) {
        for (;;) {
            mp_machine_idle();
            mp_handle_pending(true);
        }
    }
    mp_hal_delay_ms(mp_obj_get_int(args[0]));
}

MP_NORETURN static void mp_machine_deepsleep(size_t n_args, const mp_obj_t *args) {
    mp_machine_lightsleep(n_args, args);
    mp_machine_reset();
}
