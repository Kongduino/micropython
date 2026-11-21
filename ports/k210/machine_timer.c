// machine.Timer: the channels of the K210's TIMER0 and TIMER1, Timer(0) to
// Timer(7) (TIMER2 is PWM's). Both run at 1 MHz (the 26 MHz oscillator
// divided by 26), so periods go from 1 us to 71 minutes. Callbacks run
// through the scheduler, with the timer as their argument.

#include "py/runtime.h"
#include "py/mphal.h"

#include "plic.h"
#include "sysctl.h"
#include "timer.h"

#define TIMER_COUNT (8)
#define TIMER_CLOCK_HZ (1000000)
#define TIMER_CLOCK_THRESHOLD (12) // 26 MHz / ((12 + 1) * 2)

enum {
    MODE_ONE_SHOT,
    MODE_PERIODIC,
};

typedef struct _machine_timer_obj_t {
    mp_obj_base_t base;
    uint8_t id;
    uint8_t mode;
    uint32_t period_us;
} machine_timer_obj_t;

extern const mp_obj_type_t machine_timer_type;

static machine_timer_obj_t machine_timer_obj[TIMER_COUNT];

MP_REGISTER_ROOT_POINTER(mp_obj_t machine_timer_callback[8]);

static bool clock_ready[2];

static void timer_clock_init(int device) {
    if (!clock_ready[device]) {
        sysctl_clock_set_clock_select(SYSCTL_CLOCK_SELECT_TIMER0 + device, 0); // the oscillator
        sysctl_clock_set_threshold(SYSCTL_THRESHOLD_TIMER0 + device, TIMER_CLOCK_THRESHOLD);
        sysctl_clock_enable(SYSCTL_CLOCK_TIMER0 + device);
        clock_ready[device] = true;
    }
}

static int machine_timer_isr(void *ctx) {
    machine_timer_obj_t *self = ctx;
    mp_obj_t callback = MP_STATE_PORT(machine_timer_callback)[self->id];
    if (callback != MP_OBJ_NULL && callback != mp_const_none) {
        mp_sched_schedule(callback, MP_OBJ_FROM_PTR(self));
    }
    return 0;
}

static void machine_timer_stop(machine_timer_obj_t *self) {
    int device = self->id / 4, channel = self->id % 4;
    if (clock_ready[device]) {
        timer_set_enable(device, channel, 0);
    }
}

static void machine_timer_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    machine_timer_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_printf(print, "Timer(%u, mode=%s, period=%u us)", self->id,
        self->mode == MODE_PERIODIC ? "PERIODIC" : "ONE_SHOT", self->period_us);
}

// init(*, mode=Timer.PERIODIC, period=-1, tick_hz=1000, freq=-1, callback=None)
static mp_obj_t machine_timer_init_helper(machine_timer_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_mode, ARG_callback, ARG_period, ARG_tick_hz, ARG_freq };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_mode, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = MODE_PERIODIC} },
        { MP_QSTR_callback, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_period, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_tick_hz, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 1000} },
        { MP_QSTR_freq, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    uint64_t period_us;
    if (args[ARG_freq].u_obj != mp_const_none) {
        mp_float_t freq = mp_obj_get_float(args[ARG_freq].u_obj);
        if (freq <= 0) {
            mp_raise_ValueError(MP_ERROR_TEXT("freq must be positive"));
        }
        period_us = (uint64_t)(TIMER_CLOCK_HZ / freq);
    } else if (args[ARG_period].u_int > 0 && args[ARG_tick_hz].u_int > 0) {
        period_us = (uint64_t)args[ARG_period].u_int * TIMER_CLOCK_HZ / args[ARG_tick_hz].u_int;
    } else {
        mp_raise_ValueError(MP_ERROR_TEXT("period or freq needed"));
    }
    if (period_us < 1 || period_us > UINT32_MAX) {
        mp_raise_ValueError(MP_ERROR_TEXT("period out of range (1 us to 71 min)"));
    }

    int device = self->id / 4, channel = self->id % 4;
    machine_timer_stop(self);
    timer_clock_init(device);
    self->mode = args[ARG_mode].u_int == MODE_ONE_SHOT ? MODE_ONE_SHOT : MODE_PERIODIC;
    self->period_us = period_us;
    MP_STATE_PORT(machine_timer_callback)[self->id] = args[ARG_callback].u_obj;
    timer[device]->channel[channel].load_count = (uint32_t)period_us;
    timer_irq_register(device, channel, self->mode == MODE_ONE_SHOT, 1, machine_timer_isr, self);
    timer_set_enable(device, channel, 1);
    return mp_const_none;
}

// Timer(id, ...)
static mp_obj_t machine_timer_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);
    mp_int_t id = mp_obj_get_int(args[0]);
    if (id < 0 || id >= TIMER_COUNT) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("Timer(%d) doesn't exist (0 to 7)"), id);
    }
    machine_timer_obj_t *self = &machine_timer_obj[id];
    self->base.type = &machine_timer_type;
    self->id = id;
    if (n_args > 1 || n_kw > 0) {
        mp_map_t kw_args;
        mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
        machine_timer_init_helper(self, n_args - 1, args + 1, &kw_args);
    }
    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t machine_timer_init(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    return machine_timer_init_helper(MP_OBJ_TO_PTR(args[0]), n_args - 1, args + 1, kw_args);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(machine_timer_init_obj, 1, machine_timer_init);

static mp_obj_t machine_timer_deinit(mp_obj_t self_in) {
    machine_timer_obj_t *self = MP_OBJ_TO_PTR(self_in);
    machine_timer_stop(self);
    MP_STATE_PORT(machine_timer_callback)[self->id] = MP_OBJ_NULL;
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(machine_timer_deinit_obj, machine_timer_deinit);

// Stops all timers at a soft reset
void machine_timer_deinit_all(void) {
    for (int i = 0; i < TIMER_COUNT; i++) {
        machine_timer_obj[i].id = i;
        machine_timer_stop(&machine_timer_obj[i]);
        MP_STATE_PORT(machine_timer_callback)[i] = MP_OBJ_NULL;
    }
}

static const mp_rom_map_elem_t machine_timer_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&machine_timer_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&machine_timer_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_ONE_SHOT), MP_ROM_INT(MODE_ONE_SHOT) },
    { MP_ROM_QSTR(MP_QSTR_PERIODIC), MP_ROM_INT(MODE_PERIODIC) },
};
static MP_DEFINE_CONST_DICT(machine_timer_locals_dict, machine_timer_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    machine_timer_type,
    MP_QSTR_Timer,
    MP_TYPE_FLAG_NONE,
    make_new, machine_timer_make_new,
    print, machine_timer_print,
    locals_dict, &machine_timer_locals_dict
    );
