// The port's part of machine.PWM, included by extmod/machine_pwm.c: the four
// channels of the K210's TIMER2, each given to a pin through the FPIOA as
// PWM objects are made (Timer has TIMER0 and TIMER1). The timer counts at its
// full clock, so the duty cycle is fine-grained at any useful frequency.
//
// The timer can't hold its output low or high for a whole period (a count
// of 0 becomes 1), so a duty of 0 or 65535 drives the pin as a GPIO instead.

#include "py/mphal.h"

#include "fpioa.h"
#include "pwm.h"
#include "sysctl.h"

#define PWM_DEVICE PWM_DEVICE_2
#define PWM_CHANNELS (4)
#define PWM_DEFAULT_FREQ (1000)
#define NO_PIN (0xFF)

typedef struct _machine_pwm_obj_t {
    mp_obj_base_t base;
    uint8_t pin;
    uint8_t channel;
    bool invert;
    bool duty_is_ns; // set by duty_ns (kept in ns as freq changes), else u16
    uint32_t freq;
    uint32_t duty; // u16 or ns
} machine_pwm_obj_t;

// The pin each channel drives
static uint8_t channel_pin[PWM_CHANNELS] = {NO_PIN, NO_PIN, NO_PIN, NO_PIN};

static void mp_machine_pwm_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    machine_pwm_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_printf(print, "PWM(Pin(%u), freq=%u, duty_%s=%u%s)", self->pin, self->freq,
        self->duty_is_ns ? "ns" : "u16", self->duty, self->invert ? ", invert=True" : "");
}

static uint32_t duty_u16(machine_pwm_obj_t *self) {
    if (!self->duty_is_ns) {
        return self->duty;
    }
    uint64_t u16 = (uint64_t)self->duty * self->freq * 65535 / 1000000000;
    return u16 > 65535 ? 65535 : u16;
}

// Sets the timer (or the pin, at 0 and 100%) from freq and duty
static void pwm_apply(machine_pwm_obj_t *self) {
    uint32_t u16 = duty_u16(self);
    bool high = u16 == 65535, low = u16 == 0;
    if (self->invert) {
        bool t = high;
        high = low;
        low = t;
    }
    if (high || low) {
        pwm_set_enable(PWM_DEVICE, self->channel, 0);
        mp_hal_pin_output(self->pin);
        mp_hal_pin_write(self->pin, high);
        return;
    }
    pwm_init(PWM_DEVICE);
    double actual = pwm_set_frequency(PWM_DEVICE, self->channel, self->freq, (double)u16 / (double)65535);
    self->freq = (uint32_t)(actual + (double)0.5);
    machine_pin_set_function(self->pin, FUNC_TIMER2_TOGGLE1 + self->channel);
    fpioa->io[self->pin].do_inv = self->invert;
    pwm_set_enable(PWM_DEVICE, self->channel, 1);
}

static void mp_machine_pwm_init_helper(machine_pwm_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_freq, ARG_duty_u16, ARG_duty_ns, ARG_invert };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_freq, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_duty_u16, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_duty_ns, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_invert, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_freq].u_int > 0) {
        // The timer counts at most 2^31 clock cycles a period
        uint32_t clk = sysctl_clock_get_freq(SYSCTL_CLOCK_TIMER2);
        if ((uint64_t)args[ARG_freq].u_int > clk / 2 || clk / args[ARG_freq].u_int > INT32_MAX) {
            mp_raise_ValueError(MP_ERROR_TEXT("freq out of range"));
        }
        self->freq = args[ARG_freq].u_int;
    }
    if (args[ARG_duty_u16].u_int >= 0) {
        self->duty = args[ARG_duty_u16].u_int > 65535 ? 65535 : args[ARG_duty_u16].u_int;
        self->duty_is_ns = false;
    } else if (args[ARG_duty_ns].u_int >= 0) {
        self->duty = args[ARG_duty_ns].u_int;
        self->duty_is_ns = true;
    }
    if (args[ARG_invert].u_int >= 0) {
        self->invert = args[ARG_invert].u_int;
    }
    pwm_apply(self);
}

// PWM(pin, freq=1000, duty_u16=32768, duty_ns, *, invert=False)
static mp_obj_t mp_machine_pwm_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);
    uint8_t pin = mp_hal_get_pin_obj(args[0]);

    // The pin's channel if it has one, else a free one
    int channel = -1;
    for (int i = 0; i < PWM_CHANNELS && channel < 0; i++) {
        if (channel_pin[i] == pin) {
            channel = i;
        }
    }
    for (int i = 0; i < PWM_CHANNELS && channel < 0; i++) {
        if (channel_pin[i] == NO_PIN) {
            channel = i;
        }
    }
    if (channel < 0) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("all 4 PWM channels in use"));
    }
    channel_pin[channel] = pin;

    machine_pwm_obj_t *self = mp_obj_malloc(machine_pwm_obj_t, &machine_pwm_type);
    self->pin = pin;
    self->channel = channel;
    self->invert = false;
    self->duty_is_ns = false;
    self->freq = PWM_DEFAULT_FREQ;
    self->duty = 32768;
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    mp_machine_pwm_init_helper(self, n_args - 1, args + 1, &kw_args);
    return MP_OBJ_FROM_PTR(self);
}

static void mp_machine_pwm_deinit(machine_pwm_obj_t *self) {
    pwm_set_enable(PWM_DEVICE, self->channel, 0);
    fpioa->io[self->pin].do_inv = 0;
    mp_hal_pin_input(self->pin);
    if (channel_pin[self->channel] == self->pin) {
        channel_pin[self->channel] = NO_PIN;
    }
}

// Frees all channels at a soft reset
void machine_pwm_deinit_all(void) {
    for (int i = 0; i < PWM_CHANNELS; i++) {
        if (channel_pin[i] != NO_PIN) {
            pwm_set_enable(PWM_DEVICE, i, 0);
            fpioa->io[channel_pin[i]].do_inv = 0;
            channel_pin[i] = NO_PIN;
        }
    }
}

static mp_obj_t mp_machine_pwm_freq_get(machine_pwm_obj_t *self) {
    return MP_OBJ_NEW_SMALL_INT(self->freq);
}

static void mp_machine_pwm_freq_set(machine_pwm_obj_t *self, mp_int_t freq) {
    mp_obj_t args[2] = {MP_OBJ_NEW_QSTR(MP_QSTR_freq), MP_OBJ_NEW_SMALL_INT(freq)};
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, 1, args);
    mp_machine_pwm_init_helper(self, 0, NULL, &kw_args);
}

static mp_obj_t mp_machine_pwm_duty_get_u16(machine_pwm_obj_t *self) {
    return MP_OBJ_NEW_SMALL_INT(duty_u16(self));
}

static void mp_machine_pwm_duty_set_u16(machine_pwm_obj_t *self, mp_int_t duty_u16) {
    self->duty = duty_u16 < 0 ? 0 : duty_u16 > 65535 ? 65535 : duty_u16;
    self->duty_is_ns = false;
    pwm_apply(self);
}

static mp_obj_t mp_machine_pwm_duty_get_ns(machine_pwm_obj_t *self) {
    if (self->duty_is_ns) {
        return mp_obj_new_int_from_uint(self->duty);
    }
    return mp_obj_new_int_from_uint((uint64_t)self->duty * 1000000000 / 65535 / self->freq);
}

static void mp_machine_pwm_duty_set_ns(machine_pwm_obj_t *self, mp_int_t duty_ns) {
    self->duty = duty_ns < 0 ? 0 : duty_ns;
    self->duty_is_ns = true;
    pwm_apply(self);
}
