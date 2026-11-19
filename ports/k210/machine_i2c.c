// machine.I2C: the K210's three I2C controllers (DesignWare), as masters
//
// The controller has no STOP bit per byte: it ends a transfer with a STOP when
// its 8-byte transmit FIFO runs empty, and turns from writing to reading with
// a repeated START. So a transfer's bytes are fed without a gap, a write then
// a read (readfrom_mem) becoming one transfer with a repeated START. It can't
// send an address without data either: a write of nothing (scan, or
// writeto(addr, b'')) probes with a 1-byte read instead.

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "extmod/modmachine.h"

#include "fpioa.h"
#include "i2c.h"
#include "sysctl.h"

#define I2C_FIFO_DEPTH (8)
#define I2C_DEFAULT_FREQ (400000)
#define I2C_DEFAULT_TIMEOUT_US (50000)

typedef struct _machine_i2c_obj_t {
    mp_obj_base_t base;
    uint8_t id;
    uint8_t scl;
    uint8_t sda;
    uint32_t freq;
    uint32_t timeout_us;
} machine_i2c_obj_t;

// The Amigo's internal bus (touch, power, accelerometer) is on IO24/IO27; the
// other two controllers have no default pins
static machine_i2c_obj_t machine_i2c_obj[3] = {
    {{&machine_i2c_type}, 0, 24, 27, I2C_DEFAULT_FREQ, I2C_DEFAULT_TIMEOUT_US},
    {{&machine_i2c_type}, 1, 0xFF, 0xFF, I2C_DEFAULT_FREQ, I2C_DEFAULT_TIMEOUT_US},
    {{&machine_i2c_type}, 2, 0xFF, 0xFF, I2C_DEFAULT_FREQ, I2C_DEFAULT_TIMEOUT_US},
};

static void machine_i2c_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    machine_i2c_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_printf(print, "I2C(%u, scl=%u, sda=%u, freq=%u, timeout=%u)",
        self->id, self->scl, self->sda, self->freq, self->timeout_us);
}

static void machine_i2c_init(machine_i2c_obj_t *self) {
    machine_pin_set_function(self->scl, FUNC_I2C0_SCLK + 2 * self->id);
    machine_pin_set_function(self->sda, FUNC_I2C0_SDA + 2 * self->id);
    fpioa_set_io_pull(self->scl, FPIOA_PULL_UP);
    fpioa_set_io_pull(self->sda, FPIOA_PULL_UP);
    i2c_init(self->id, 0, 7, self->freq);
    volatile i2c_t *regs = i2c[self->id];
    regs->enable = 0;
    regs->dma_cr = 0; // the SDK turns DMA requests on
    regs->rx_tl = 0;
    regs->tx_tl = 0;
    regs->enable = I2C_ENABLE_ENABLE;
}

// I2C(id, *, scl, sda, freq=400000, timeout=50000)
mp_obj_t machine_i2c_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum { ARG_id, ARG_scl, ARG_sda, ARG_freq, ARG_timeout };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_id, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_scl, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_sda, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_freq, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_timeout, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    mp_int_t id = args[ARG_id].u_int;
    if (id < 0 || id >= MP_ARRAY_SIZE(machine_i2c_obj)) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("I2C(%d) doesn't exist"), id);
    }
    machine_i2c_obj_t *self = &machine_i2c_obj[id];
    if (args[ARG_scl].u_obj != mp_const_none) {
        self->scl = mp_hal_get_pin_obj(args[ARG_scl].u_obj);
    }
    if (args[ARG_sda].u_obj != mp_const_none) {
        self->sda = mp_hal_get_pin_obj(args[ARG_sda].u_obj);
    }
    if (self->scl == 0xFF || self->sda == 0xFF) {
        mp_raise_ValueError(MP_ERROR_TEXT("scl and sda pins needed"));
    }
    if (args[ARG_freq].u_int > 0) {
        self->freq = args[ARG_freq].u_int;
    }
    if (args[ARG_timeout].u_int >= 0) {
        self->timeout_us = args[ARG_timeout].u_int;
    }
    machine_i2c_init(self);
    return MP_OBJ_FROM_PTR(self);
}

// After an abort the controller flushes its FIFOs; returns the error for it
static int abort_error(volatile i2c_t *regs) {
    uint32_t source = regs->tx_abrt_source;
    (void)regs->clr_tx_abrt;
    return (source & I2C_TX_ABRT_SOURCE_7B_ADDR_NOACK) ? -MP_ENODEV : -MP_EIO;
}

static bool is_read(size_t i, unsigned int flags) {
    #if MICROPY_PY_MACHINE_I2C_TRANSFER_WRITE1
    if (i == 0 && (flags & MP_MACHINE_I2C_FLAG_WRITE1)) {
        return false;
    }
    #endif
    return flags & MP_MACHINE_I2C_FLAG_READ;
}

static int machine_i2c_transfer(mp_obj_base_t *self_in, uint16_t addr, size_t n, mp_machine_i2c_buf_t *bufs, unsigned int flags) {
    machine_i2c_obj_t *self = (machine_i2c_obj_t *)self_in;
    volatile i2c_t *regs = i2c[self->id];

    size_t total = 0;
    for (size_t i = 0; i < n; i++) {
        total += bufs[i].len;
    }
    // Nothing to send: probe with a 1-byte read
    uint8_t probe;
    mp_machine_i2c_buf_t probe_buf = {.len = 1, .buf = &probe};
    if (total == 0) {
        n = 1;
        bufs = &probe_buf;
        flags = MP_MACHINE_I2C_FLAG_READ | MP_MACHINE_I2C_FLAG_STOP;
    }

    // Wait out anything still on the bus, and start from empty FIFOs
    mp_uint_t start = mp_hal_ticks_us();
    while (regs->status & I2C_STATUS_ACTIVITY) {
        if (mp_hal_ticks_us() - start > self->timeout_us) {
            return -MP_ETIMEDOUT;
        }
    }
    while (regs->rxflr) {
        (void)regs->data_cmd;
    }
    (void)regs->clr_tx_abrt;
    regs->tar = I2C_TAR_ADDRESS(addr);

    // Feed commands (a byte to write, or a read) from buffer `in`, and take
    // the bytes read into buffer `out`. No more reads are outstanding than
    // the receive FIFO holds, and the transmit FIFO stays fed meanwhile.
    size_t in = 0, in_pos = 0, out = 0, out_pos = 0, reads_pending = 0;
    start = mp_hal_ticks_us();
    for (;;) {
        while (in < n && in_pos == bufs[in].len) {
            in++;
            in_pos = 0;
        }
        while (out < n && (!is_read(out, flags) || out_pos == bufs[out].len)) {
            out++;
            out_pos = 0;
        }
        if (in == n && reads_pending == 0) {
            break;
        }
        while (in < n && in_pos < bufs[in].len && regs->txflr < I2C_FIFO_DEPTH) {
            if (is_read(in, flags)) {
                if (reads_pending == I2C_FIFO_DEPTH) {
                    break;
                }
                regs->data_cmd = I2C_DATA_CMD_CMD;
                reads_pending++;
            } else {
                regs->data_cmd = I2C_DATA_CMD_DATA(bufs[in].buf[in_pos]);
            }
            in_pos++;
        }
        if (reads_pending && regs->rxflr) {
            bufs[out].buf[out_pos++] = regs->data_cmd;
            reads_pending--;
        }
        if (regs->tx_abrt_source) {
            return abort_error(regs);
        }
        if (mp_hal_ticks_us() - start > self->timeout_us) {
            return -MP_ETIMEDOUT;
        }
    }

    // Wait for the last bytes to go out and the STOP
    while ((regs->status & I2C_STATUS_ACTIVITY) || !(regs->status & I2C_STATUS_TFE)) {
        if (regs->tx_abrt_source) {
            return abort_error(regs);
        }
        if (mp_hal_ticks_us() - start > self->timeout_us) {
            return -MP_ETIMEDOUT;
        }
    }
    if (regs->tx_abrt_source) {
        return abort_error(regs);
    }
    return total;
}

static const mp_machine_i2c_p_t machine_i2c_p = {
    #if MICROPY_PY_MACHINE_I2C_TRANSFER_WRITE1
    .transfer_supports_write1 = true,
    #endif
    .transfer = machine_i2c_transfer,
};

MP_DEFINE_CONST_OBJ_TYPE(
    machine_i2c_type,
    MP_QSTR_I2C,
    MP_TYPE_FLAG_NONE,
    make_new, machine_i2c_make_new,
    print, machine_i2c_print,
    protocol, &machine_i2c_p,
    locals_dict, &mp_machine_i2c_locals_dict
    );
