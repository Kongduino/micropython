#include <stdio.h>

#include "py/builtin.h"
#include "py/compile.h"
#include "py/gc.h"
#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/runtime.h"
#include "py/stackctrl.h"
#include "shared/runtime/gchelper.h"
#include "shared/runtime/pyexec.h"

#include "sysctl.h"

static char heap[MICROPY_HEAP_SIZE];

int main(void) {
    // 800 MHz PLL0: the CPU at 400 MHz, as Maixduino and MaixPy run it
    sysctl_pll_set_freq(SYSCTL_PLL0, 800000000UL);
    // PLL1 (the KPU's) and PLL2 (I2S audio's), as Maixduino sets them
    sysctl_pll_set_freq(SYSCTL_PLL1, 300000000UL);
    sysctl_pll_set_freq(SYSCTL_PLL2, 45158400UL);
    // IO36-IO47 (the LCD's and the camera's pins) are powered at 1.8 V on the
    // Amigo, as Maixduino and MaixPy set them
    sysctl_set_power_mode(SYSCTL_POWER_BANK6, SYSCTL_POWER_V18);
    sysctl_set_power_mode(SYSCTL_POWER_BANK7, SYSCTL_POWER_V18);
    mp_hal_init();
    k210_reset_cause_init();

soft_reset:
    mp_stack_ctrl_init();
    mp_stack_set_limit(MICROPY_HW_STACK_SIZE - 4096);
    gc_init(heap, heap + sizeof(heap));
    mp_init();
    mp_obj_list_append(mp_sys_path, MP_OBJ_NEW_QSTR(MP_QSTR__slash_lib));

    // Mount the file system, then run boot.py and main.py from it
    pyexec_frozen_module("_boot.py", false);
    int ret = pyexec_file_if_exists("boot.py");
    if (ret & PYEXEC_FORCED_EXIT) {
        goto soft_reset_exit;
    }
    if (pyexec_mode_kind == PYEXEC_MODE_FRIENDLY_REPL) {
        ret = pyexec_file_if_exists("main.py");
        if (ret & PYEXEC_FORCED_EXIT) {
            goto soft_reset_exit;
        }
    }

    for (;;) {
        if (pyexec_mode_kind == PYEXEC_MODE_RAW_REPL) {
            if (pyexec_raw_repl() != 0) {
                break;
            }
        } else {
            if (pyexec_friendly_repl() != 0) {
                break;
            }
        }
    }

soft_reset_exit:
    mp_printf(&mp_plat_print, "MPY: soft reboot\n");
    machine_pin_deinit();
    machine_uart_deinit_all();
    machine_timer_deinit_all();
    machine_pwm_deinit_all();
    machine_i2s_deinit_all();
    k210_camera_deinit();
    gc_sweep_all();
    mp_deinit();
    goto soft_reset;
}

void gc_collect(void) {
    gc_collect_start();
    gc_helper_collect_regs_and_stack();
    gc_collect_end();
}

void nlr_jump_fail(void *val) {
    mp_printf(&mp_plat_print, "FATAL: uncaught NLR %p\n", val);
    for (;;) {
    }
}

#ifndef NDEBUG
void MP_WEAK __assert_func(const char *file, int line, const char *func, const char *expr) {
    mp_printf(&mp_plat_print, "Assertion '%s' failed, at file %s:%d\n", expr, file, line);
    for (;;) {
    }
}
#endif
