// The port's part of machine.WDT, included by extmod/machine_wdt.c: the
// K210's two watchdogs (DesignWare), set to reset the chip at the first
// time-out. A time-out is 2^(16 + top) cycles of the watchdog's clock, so
// the one asked for is rounded up to the next of those. Once started, a
// watchdog can't be stopped (but by a reset).

#include "py/mphal.h"

#include "platform.h"
#include "sysctl.h"
#include "wdt.h"

typedef struct _machine_wdt_obj_t {
    mp_obj_base_t base;
    uint8_t id;
} machine_wdt_obj_t;

static const machine_wdt_obj_t machine_wdt_obj[2] = {
    {{&machine_wdt_type}, 0},
    {{&machine_wdt_type}, 1},
};

static volatile wdt_t *const wdt_regs[2] = {
    (volatile wdt_t *)WDT0_BASE_ADDR,
    (volatile wdt_t *)WDT1_BASE_ADDR,
};

static machine_wdt_obj_t *mp_machine_wdt_make_new_instance(mp_obj_t id_in, mp_int_t timeout_ms) {
    mp_int_t id = mp_obj_get_int(id_in);
    if (id < 0 || id > 1) {
        mp_raise_ValueError(MP_ERROR_TEXT("WDT id must be 0 or 1"));
    }
    if (timeout_ms <= 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("timeout must be positive"));
    }

    sysctl_reset(id ? SYSCTL_RESET_WDT1 : SYSCTL_RESET_WDT0);
    sysctl_clock_set_threshold(id ? SYSCTL_THRESHOLD_WDT1 : SYSCTL_THRESHOLD_WDT0, 0);
    sysctl_clock_enable(id ? SYSCTL_CLOCK_WDT1 : SYSCTL_CLOCK_WDT0);
    uint64_t clk = sysctl_clock_get_freq(id ? SYSCTL_CLOCK_WDT1 : SYSCTL_CLOCK_WDT0);

    // The smallest time-out at least as long as the one asked for
    int top = 0;
    while (top < 15 && ((1ULL << (16 + top)) * 1000 / clk) < (uint64_t)timeout_ms) {
        top++;
    }
    if (((1ULL << (16 + top)) * 1000 / clk) < (uint64_t)timeout_ms) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("timeout too long: %u ms at most"),
            (unsigned)((1ULL << 31) * 1000 / clk));
    }

    volatile wdt_t *regs = wdt_regs[id];
    regs->torr = WDT_TORR_TOP(top);
    regs->cr = (regs->cr & ~WDT_CR_RMOD_MASK) | WDT_CR_RMOD_RESET | WDT_CR_ENABLE;
    regs->crr = WDT_CRR_MASK;
    return (machine_wdt_obj_t *)&machine_wdt_obj[id];
}

static void mp_machine_wdt_feed(machine_wdt_obj_t *self) {
    wdt_regs[self->id]->crr = WDT_CRR_MASK;
}
