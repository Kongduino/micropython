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
    mp_hal_init();

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
