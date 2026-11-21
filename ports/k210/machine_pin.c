// machine.Pin: IO0 to IO47, each routed to one of the 32 high-speed GPIO
// channels when it's first used as a pin

#include "py/runtime.h"
#include "py/mphal.h"
#include "extmod/modmachine.h"
#include "extmod/virtpin.h"

#include "fpioa.h"
#include "gpiohs.h"
#include "plic.h"

#define GPIOHS_CHANNELS (32)

enum {
    PIN_MODE_IN,
    PIN_MODE_OUT,
    PIN_MODE_OPEN_DRAIN,
};

enum {
    PIN_PULL_NONE,
    PIN_PULL_UP,
    PIN_PULL_DOWN,
};

typedef struct _machine_pin_obj_t {
    mp_obj_base_t base;
    uint8_t id;
} machine_pin_obj_t;

#define PIN(n) {{&machine_pin_type}, n}
static const machine_pin_obj_t machine_pin_obj[MICROPY_HW_PIN_COUNT] = {
    PIN(0), PIN(1), PIN(2), PIN(3), PIN(4), PIN(5), PIN(6), PIN(7),
    PIN(8), PIN(9), PIN(10), PIN(11), PIN(12), PIN(13), PIN(14), PIN(15),
    PIN(16), PIN(17), PIN(18), PIN(19), PIN(20), PIN(21), PIN(22), PIN(23),
    PIN(24), PIN(25), PIN(26), PIN(27), PIN(28), PIN(29), PIN(30), PIN(31),
    PIN(32), PIN(33), PIN(34), PIN(35), PIN(36), PIN(37), PIN(38), PIN(39),
    PIN(40), PIN(41), PIN(42), PIN(43), PIN(44), PIN(45), PIN(46), PIN(47),
};

// The channel each pin holds, plus one (0: none), and the pin each channel
// serves, plus one (0: free)
static uint8_t pin_channel[MICROPY_HW_PIN_COUNT];
static uint8_t channel_pin[GPIOHS_CHANNELS];
static uint8_t pin_mode[MICROPY_HW_PIN_COUNT];
static uint8_t pin_pull[MICROPY_HW_PIN_COUNT];
static uint8_t channel_trigger[GPIOHS_CHANNELS];

MP_REGISTER_ROOT_POINTER(mp_obj_t machine_pin_irq_handler[32]);

static void channel_irq_off(int ch) {
    gpiohs_set_pin_edge(ch, GPIO_PE_NONE);
    plic_irq_disable(IRQN_GPIOHS0_INTERRUPT + ch);
    MP_STATE_PORT(machine_pin_irq_handler)[ch] = MP_OBJ_NULL;
}

// The pin's channel, taking a free one and routing the pin to it if it has
// none
static int pin_get_channel(uint32_t pin) {
    if (pin_channel[pin]) {
        return pin_channel[pin] - 1;
    }
    for (int ch = 0; ch < GPIOHS_CHANNELS; ch++) {
        if (!channel_pin[ch]) {
            channel_pin[ch] = pin + 1;
            pin_channel[pin] = ch + 1;
            fpioa_set_function(pin, FUNC_GPIOHS0 + ch);
            return ch;
        }
    }
    mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("no free GPIO channel"));
}

int machine_pin_gpio_channel(mp_hal_pin_obj_t pin) {
    return pin_get_channel(pin);
}

void machine_pin_set_function(mp_hal_pin_obj_t pin, int function) {
    if (pin_channel[pin]) {
        int ch = pin_channel[pin] - 1;
        channel_irq_off(ch);
        channel_pin[ch] = 0;
        pin_channel[pin] = 0;
    }
    fpioa_set_function(pin, function);
}

void machine_pin_deinit(void) {
    for (int ch = 0; ch < GPIOHS_CHANNELS; ch++) {
        if (channel_pin[ch]) {
            channel_irq_off(ch);
        }
    }
}

static gpio_drive_mode_t input_drive_mode(uint32_t pin) {
    switch (pin_pull[pin]) {
        case PIN_PULL_UP:
            return GPIO_DM_INPUT_PULL_UP;
        case PIN_PULL_DOWN:
            return GPIO_DM_INPUT_PULL_DOWN;
        default:
            return GPIO_DM_INPUT;
    }
}

// The level a pin drives, for outputs
static int pin_output_level(int ch) {
    return (gpiohs->output_val.u32[0] >> ch) & 1;
}

static void pin_set(uint32_t pin, int value) {
    int ch = pin_get_channel(pin);
    if (pin_mode[pin] == PIN_MODE_OPEN_DRAIN) {
        // Open drain: driven low, or let go (an input) to be pulled high
        if (value) {
            gpiohs_set_drive_mode(ch, input_drive_mode(pin));
        } else {
            gpiohs_set_pin(ch, GPIO_PV_LOW);
            gpiohs_set_drive_mode(ch, GPIO_DM_OUTPUT);
        }
    } else {
        gpiohs_set_pin(ch, value ? GPIO_PV_HIGH : GPIO_PV_LOW);
    }
}

static int pin_get(uint32_t pin) {
    int ch = pin_get_channel(pin);
    if (pin_mode[pin] == PIN_MODE_OUT) {
        return pin_output_level(ch);
    }
    if (pin_mode[pin] == PIN_MODE_OPEN_DRAIN && (gpiohs->output_en.u32[0] >> ch) & 1) {
        return 0; // driven low
    }
    return gpiohs_get_pin(ch);
}

static void pin_configure(uint32_t pin, int mode, int pull) {
    int ch = pin_get_channel(pin);
    pin_mode[pin] = mode;
    pin_pull[pin] = pull;
    switch (mode) {
        case PIN_MODE_IN:
            gpiohs_set_drive_mode(ch, input_drive_mode(pin));
            break;
        case PIN_MODE_OUT:
            gpiohs_set_drive_mode(ch, GPIO_DM_OUTPUT);
            break;
        case PIN_MODE_OPEN_DRAIN:
            // Starts released, unless value= says otherwise
            gpiohs_set_drive_mode(ch, input_drive_mode(pin));
            break;
    }
}

// The HAL functions SoftI2C and SoftSPI use

mp_hal_pin_obj_t mp_hal_get_pin_obj(mp_obj_t pin_in) {
    if (mp_obj_is_type(pin_in, &machine_pin_type)) {
        machine_pin_obj_t *self = MP_OBJ_TO_PTR(pin_in);
        return self->id;
    }
    mp_int_t pin = mp_obj_get_int(pin_in);
    if (pin < 0 || pin >= MICROPY_HW_PIN_COUNT) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid pin"));
    }
    return pin;
}

void mp_hal_pin_input(mp_hal_pin_obj_t pin) {
    pin_configure(pin, PIN_MODE_IN, pin_pull[pin]);
}

void mp_hal_pin_output(mp_hal_pin_obj_t pin) {
    pin_configure(pin, PIN_MODE_OUT, PIN_PULL_NONE);
}

void mp_hal_pin_open_drain(mp_hal_pin_obj_t pin) {
    pin_configure(pin, PIN_MODE_OPEN_DRAIN, PIN_PULL_UP);
}

void mp_hal_pin_od_low(mp_hal_pin_obj_t pin) {
    pin_set(pin, 0);
}

void mp_hal_pin_od_high(mp_hal_pin_obj_t pin) {
    pin_set(pin, 1);
}

int mp_hal_pin_read(mp_hal_pin_obj_t pin) {
    return pin_get(pin);
}

void mp_hal_pin_write(mp_hal_pin_obj_t pin, int value) {
    pin_set(pin, value);
}

// The Pin class

static void machine_pin_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    machine_pin_obj_t *self = MP_OBJ_TO_PTR(self_in);
    static const char *const modes[] = {"IN", "OUT", "OPEN_DRAIN"};
    static const char *const pulls[] = {"", ", pull=PULL_UP", ", pull=PULL_DOWN"};
    if (pin_channel[self->id]) {
        mp_printf(print, "Pin(%u, mode=%s%s)", self->id, modes[pin_mode[self->id]], pulls[pin_pull[self->id]]);
    } else {
        mp_printf(print, "Pin(%u)", self->id);
    }
}

// init(mode=-1, pull=-1, *, value=None)
static mp_obj_t machine_pin_obj_init_helper(const machine_pin_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_mode, ARG_pull, ARG_value };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_mode, MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_pull, MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_value, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    uint32_t pin = self->id;
    int mode = pin_channel[pin] ? pin_mode[pin] : PIN_MODE_IN;
    if (args[ARG_mode].u_obj != mp_const_none) {
        mode = mp_obj_get_int(args[ARG_mode].u_obj);
        if (mode < PIN_MODE_IN || mode > PIN_MODE_OPEN_DRAIN) {
            mp_raise_ValueError(MP_ERROR_TEXT("invalid pin mode"));
        }
    }
    int pull = pin_channel[pin] ? pin_pull[pin] : PIN_PULL_NONE;
    if (args[ARG_pull].u_obj != mp_const_none) {
        pull = mp_obj_get_int(args[ARG_pull].u_obj);
        if (pull < PIN_PULL_NONE || pull > PIN_PULL_DOWN) {
            mp_raise_ValueError(MP_ERROR_TEXT("invalid pin pull"));
        }
    } else if (args[ARG_mode].u_obj != mp_const_none) {
        pull = PIN_PULL_NONE;
    }

    // Set the level before the pin starts driving it
    if (args[ARG_value].u_obj != mp_const_none) {
        pin_get_channel(pin);
        pin_mode[pin] = mode;
        pin_pull[pin] = pull;
        pin_set(pin, mp_obj_is_true(args[ARG_value].u_obj));
    }
    if (mode != PIN_MODE_OPEN_DRAIN || args[ARG_value].u_obj == mp_const_none) {
        pin_configure(pin, mode, pull);
    }
    return mp_const_none;
}

// Pin(id, mode=-1, pull=-1, *, value=None)
mp_obj_t mp_pin_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);
    const machine_pin_obj_t *self = &machine_pin_obj[mp_hal_get_pin_obj(args[0])];
    if (n_args > 1 || n_kw > 0 || !pin_channel[self->id]) {
        mp_map_t kw_args;
        mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
        machine_pin_obj_init_helper(self, n_args - 1, args + 1, &kw_args);
    }
    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t machine_pin_call(mp_obj_t self_in, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 1, false);
    machine_pin_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (n_args == 0) {
        return MP_OBJ_NEW_SMALL_INT(pin_get(self->id));
    }
    pin_set(self->id, mp_obj_is_true(args[0]));
    return mp_const_none;
}

static mp_obj_t machine_pin_obj_init(size_t n_args, const mp_obj_t *args, mp_map_t *kw_args) {
    return machine_pin_obj_init_helper(MP_OBJ_TO_PTR(args[0]), n_args - 1, args + 1, kw_args);
}
MP_DEFINE_CONST_FUN_OBJ_KW(machine_pin_init_obj, 1, machine_pin_obj_init);

static mp_obj_t machine_pin_value(size_t n_args, const mp_obj_t *args) {
    return machine_pin_call(args[0], n_args - 1, 0, args + 1);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(machine_pin_value_obj, 1, 2, machine_pin_value);

static mp_obj_t machine_pin_off(mp_obj_t self_in) {
    machine_pin_obj_t *self = MP_OBJ_TO_PTR(self_in);
    pin_set(self->id, 0);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(machine_pin_off_obj, machine_pin_off);

static mp_obj_t machine_pin_on(mp_obj_t self_in) {
    machine_pin_obj_t *self = MP_OBJ_TO_PTR(self_in);
    pin_set(self->id, 1);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(machine_pin_on_obj, machine_pin_on);

static mp_obj_t machine_pin_toggle(mp_obj_t self_in) {
    machine_pin_obj_t *self = MP_OBJ_TO_PTR(self_in);
    pin_set(self->id, !pin_get(self->id));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(machine_pin_toggle_obj, machine_pin_toggle);

// The interrupt runs the handler through the scheduler (a soft interrupt).
// The GPIO interrupts fire on both edges whichever edge is enabled, so both
// are, and the level after the edge tells which it was.
static int machine_pin_isr(void *ctx) {
    uint32_t pin = (uintptr_t)ctx;
    int ch = pin_channel[pin] - 1;
    if (ch >= 0) {
        mp_obj_t handler = MP_STATE_PORT(machine_pin_irq_handler)[ch];
        int edge = gpiohs_get_pin(ch) ? GPIO_PE_RISING : GPIO_PE_FALLING;
        if (handler != MP_OBJ_NULL && (channel_trigger[ch] & edge)) {
            mp_sched_schedule(handler, MP_OBJ_FROM_PTR(&machine_pin_obj[pin]));
        }
    }
    return 0;
}

// irq(handler=None, trigger=IRQ_FALLING|IRQ_RISING)
static mp_obj_t machine_pin_irq(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_handler, ARG_trigger, ARG_hard };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_handler, MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_trigger, MP_ARG_INT, {.u_int = GPIO_PE_BOTH} },
        { MP_QSTR_hard, MP_ARG_BOOL, {.u_bool = false} },
    };
    machine_pin_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    if (args[ARG_hard].u_bool) {
        mp_raise_ValueError(MP_ERROR_TEXT("hard IRQs not supported"));
    }

    int ch = pin_get_channel(self->id);
    channel_irq_off(ch);
    mp_obj_t handler = args[ARG_handler].u_obj;
    int trigger = args[ARG_trigger].u_int & GPIO_PE_BOTH;
    if (handler != mp_const_none && trigger) {
        MP_STATE_PORT(machine_pin_irq_handler)[ch] = handler;
        channel_trigger[ch] = trigger;
        gpiohs_irq_register(ch, 1, machine_pin_isr, (void *)(uintptr_t)self->id);
        gpiohs_set_pin_edge(ch, GPIO_PE_BOTH);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(machine_pin_irq_obj, 1, machine_pin_irq);

static const mp_rom_map_elem_t machine_pin_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&machine_pin_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_value), MP_ROM_PTR(&machine_pin_value_obj) },
    { MP_ROM_QSTR(MP_QSTR_off), MP_ROM_PTR(&machine_pin_off_obj) },
    { MP_ROM_QSTR(MP_QSTR_on), MP_ROM_PTR(&machine_pin_on_obj) },
    { MP_ROM_QSTR(MP_QSTR_low), MP_ROM_PTR(&machine_pin_off_obj) },
    { MP_ROM_QSTR(MP_QSTR_high), MP_ROM_PTR(&machine_pin_on_obj) },
    { MP_ROM_QSTR(MP_QSTR_toggle), MP_ROM_PTR(&machine_pin_toggle_obj) },
    { MP_ROM_QSTR(MP_QSTR_irq), MP_ROM_PTR(&machine_pin_irq_obj) },

    { MP_ROM_QSTR(MP_QSTR_IN), MP_ROM_INT(PIN_MODE_IN) },
    { MP_ROM_QSTR(MP_QSTR_OUT), MP_ROM_INT(PIN_MODE_OUT) },
    { MP_ROM_QSTR(MP_QSTR_OPEN_DRAIN), MP_ROM_INT(PIN_MODE_OPEN_DRAIN) },
    { MP_ROM_QSTR(MP_QSTR_PULL_UP), MP_ROM_INT(PIN_PULL_UP) },
    { MP_ROM_QSTR(MP_QSTR_PULL_DOWN), MP_ROM_INT(PIN_PULL_DOWN) },
    { MP_ROM_QSTR(MP_QSTR_IRQ_FALLING), MP_ROM_INT(GPIO_PE_FALLING) },
    { MP_ROM_QSTR(MP_QSTR_IRQ_RISING), MP_ROM_INT(GPIO_PE_RISING) },
};
static MP_DEFINE_CONST_DICT(machine_pin_locals_dict, machine_pin_locals_dict_table);

// The pin protocol, for machine.Signal
static mp_uint_t machine_pin_ioctl(mp_obj_t self_in, mp_uint_t request, uintptr_t arg, int *errcode) {
    machine_pin_obj_t *self = MP_OBJ_TO_PTR(self_in);
    switch (request) {
        case MP_PIN_READ:
            return pin_get(self->id);
        case MP_PIN_WRITE:
            pin_set(self->id, arg);
            return 0;
    }
    return -1;
}

static const mp_pin_p_t machine_pin_pin_p = {
    .ioctl = machine_pin_ioctl,
};

MP_DEFINE_CONST_OBJ_TYPE(
    machine_pin_type,
    MP_QSTR_Pin,
    MP_TYPE_FLAG_NONE,
    make_new, mp_pin_make_new,
    print, machine_pin_print,
    call, machine_pin_call,
    protocol, &machine_pin_pin_p,
    locals_dict, &machine_pin_locals_dict
    );
