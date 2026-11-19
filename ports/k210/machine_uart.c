// The port's part of machine.UART, included by extmod/machine_uart.c: the
// K210's UART1 to UART3 (16550-style), with an interrupt filling a receive
// buffer

#include "py/mphal.h"
#include "py/ringbuf.h"
#include "py/stream.h"

#include "fpioa.h"
#include "uart.h"

#define UART_COUNT (3)

// The registers, defined in the SDK's uart.c but not declared in its header
extern volatile uart_t *const uart[UART_COUNT];

#define UART_DEFAULT_RXBUF (256)
#define UART_LSR_DATA_READY (0x01)
#define UART_LSR_TX_EMPTY (0x40) // the transmitter is idle
#define UART_LCR_BREAK (0x40)

#define MICROPY_PY_MACHINE_UART_CLASS_CONSTANTS

typedef struct _machine_uart_obj_t {
    mp_obj_base_t base;
    uint8_t id; // 1 to 3
    uint8_t tx;
    uint8_t rx;
    uint8_t bits;
    uint8_t parity; // UART_PARITY_*
    uint8_t stop;
    uint32_t baudrate;
    uint16_t timeout; // ms, before the first byte
    uint16_t timeout_char; // ms, between bytes
    ringbuf_t rxbuf;
} machine_uart_obj_t;

MP_REGISTER_ROOT_POINTER(struct _machine_uart_obj_t *machine_uart_obj_all[3]);

static const uint8_t uart_tx_function[UART_COUNT] = {FUNC_UART1_TX, FUNC_UART2_TX, FUNC_UART3_TX};
static const uint8_t uart_rx_function[UART_COUNT] = {FUNC_UART1_RX, FUNC_UART2_RX, FUNC_UART3_RX};

static const char *const parity_name[] = {"None", "1", "0"};

static void mp_machine_uart_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    machine_uart_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_printf(print, "UART(%u, baudrate=%u, bits=%u, parity=%s, stop=%u, tx=%u, rx=%u, timeout=%u, timeout_char=%u, rxbuf=%u)",
        self->id, self->baudrate, self->bits, parity_name[self->parity], self->stop,
        self->tx, self->rx, self->timeout, self->timeout_char, self->rxbuf.size - 1);
}

static int uart_rx_isr(void *ctx) {
    machine_uart_obj_t *self = ctx;
    volatile uart_t *regs = uart[self->id - 1];
    while (regs->LSR & UART_LSR_DATA_READY) {
        ringbuf_put(&self->rxbuf, regs->RBR & 0xFF); // dropped when full
    }
    return 0;
}

static void mp_machine_uart_init_helper(machine_uart_obj_t *self, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_baudrate, ARG_bits, ARG_parity, ARG_stop, ARG_tx, ARG_rx, ARG_timeout, ARG_timeout_char, ARG_rxbuf };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_baudrate, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_bits, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_parity, MP_ARG_OBJ, {.u_rom_obj = MP_ROM_INT(-1)} },
        { MP_QSTR_stop, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_tx, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_rx, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_timeout, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_timeout_char, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_rxbuf, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_baudrate].u_int > 0) {
        self->baudrate = args[ARG_baudrate].u_int;
    }
    if (args[ARG_bits].u_int >= 0) {
        if (args[ARG_bits].u_int < 5 || args[ARG_bits].u_int > 8) {
            mp_raise_ValueError(MP_ERROR_TEXT("invalid bits"));
        }
        self->bits = args[ARG_bits].u_int;
    }
    if (args[ARG_parity].u_obj != MP_OBJ_NEW_SMALL_INT(-1)) {
        if (args[ARG_parity].u_obj == mp_const_none) {
            self->parity = UART_PARITY_NONE;
        } else {
            self->parity = (mp_obj_get_int(args[ARG_parity].u_obj) & 1) ? UART_PARITY_ODD : UART_PARITY_EVEN;
        }
    }
    if (args[ARG_stop].u_int >= 0) {
        if (args[ARG_stop].u_int != 1 && args[ARG_stop].u_int != 2) {
            mp_raise_ValueError(MP_ERROR_TEXT("invalid stop bits"));
        }
        self->stop = args[ARG_stop].u_int;
    }
    if (args[ARG_tx].u_obj != mp_const_none) {
        self->tx = mp_hal_get_pin_obj(args[ARG_tx].u_obj);
    }
    if (args[ARG_rx].u_obj != mp_const_none) {
        self->rx = mp_hal_get_pin_obj(args[ARG_rx].u_obj);
    }
    if (self->tx == 0xFF && self->rx == 0xFF) {
        mp_raise_ValueError(MP_ERROR_TEXT("tx or rx pin needed"));
    }
    if (args[ARG_timeout].u_int >= 0) {
        self->timeout = args[ARG_timeout].u_int;
    }
    if (args[ARG_timeout_char].u_int >= 0) {
        self->timeout_char = args[ARG_timeout_char].u_int;
    }
    if (args[ARG_rxbuf].u_int > 0 || self->rxbuf.buf == NULL) {
        size_t size = args[ARG_rxbuf].u_int > 0 ? args[ARG_rxbuf].u_int : UART_DEFAULT_RXBUF;
        ringbuf_alloc(&self->rxbuf, size + 1);
    }

    int ch = self->id - 1;
    if (self->tx != 0xFF) {
        machine_pin_set_function(self->tx, uart_tx_function[ch]);
    }
    if (self->rx != 0xFF) {
        machine_pin_set_function(self->rx, uart_rx_function[ch]);
    }
    uart_init(ch);
    uart_configure(ch, self->baudrate, self->bits, self->stop == 2 ? UART_STOP_2 : UART_STOP_1, self->parity);
    uart_irq_register(ch, UART_RECEIVE, uart_rx_isr, self, 1);
}

// UART(id, baudrate=115200, bits=8, parity=None, stop=1, *, tx, rx, timeout=0, timeout_char=1, rxbuf=256)
static mp_obj_t mp_machine_uart_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);
    mp_int_t id = mp_obj_get_int(args[0]);
    if (id < 1 || id > UART_COUNT) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("UART(%d) doesn't exist"), id);
    }
    machine_uart_obj_t *self = MP_STATE_PORT(machine_uart_obj_all)[id - 1];
    if (self == NULL) {
        self = mp_obj_malloc(machine_uart_obj_t, &machine_uart_type);
        self->id = id;
        self->tx = 0xFF;
        self->rx = 0xFF;
        self->bits = 8;
        self->parity = UART_PARITY_NONE;
        self->stop = 1;
        self->baudrate = 115200;
        self->timeout = 0;
        self->timeout_char = 1;
        self->rxbuf.buf = NULL;
        MP_STATE_PORT(machine_uart_obj_all)[id - 1] = self;
    }
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    mp_machine_uart_init_helper(self, n_args - 1, args + 1, &kw_args);
    return MP_OBJ_FROM_PTR(self);
}

static void mp_machine_uart_deinit(machine_uart_obj_t *self) {
    uart_irq_unregister(self->id - 1, UART_RECEIVE);
    plic_irq_disable(IRQN_UART1_INTERRUPT + self->id - 1);
}

// Turns the UARTs' interrupts off at a soft reset (their objects go)
void machine_uart_deinit_all(void) {
    for (int i = 0; i < UART_COUNT; i++) {
        if (MP_STATE_PORT(machine_uart_obj_all)[i]) {
            mp_machine_uart_deinit(MP_STATE_PORT(machine_uart_obj_all)[i]);
            MP_STATE_PORT(machine_uart_obj_all)[i] = NULL;
        }
    }
}

static mp_int_t mp_machine_uart_any(machine_uart_obj_t *self) {
    return ringbuf_avail(&self->rxbuf);
}

static bool mp_machine_uart_txdone(machine_uart_obj_t *self) {
    return uart[self->id - 1]->LSR & UART_LSR_TX_EMPTY;
}

static void mp_machine_uart_sendbreak(machine_uart_obj_t *self) {
    volatile uart_t *regs = uart[self->id - 1];
    while (!(regs->LSR & UART_LSR_TX_EMPTY)) {
    }
    regs->LCR |= UART_LCR_BREAK;
    // At least 13 bit times
    mp_hal_delay_us(13000000 / self->baudrate + 1);
    regs->LCR &= ~UART_LCR_BREAK;
}

static mp_uint_t mp_machine_uart_read(mp_obj_t self_in, void *buf_in, mp_uint_t size, int *errcode) {
    machine_uart_obj_t *self = MP_OBJ_TO_PTR(self_in);
    uint8_t *buf = buf_in;
    // Timed in microseconds: a 1 ms timeout counted in ms ticks can end at the
    // next tick, microseconds away. Between bytes, wait at least two
    // characters' time (10 bits each).
    mp_uint_t timeout_us = self->timeout * 1000;
    mp_uint_t timeout_char_us = self->timeout_char * 1000;
    mp_uint_t two_chars_us = 20000000 / self->baudrate + 1;
    if (timeout_char_us < two_chars_us) {
        timeout_char_us = two_chars_us;
    }
    size_t n = 0;
    mp_uint_t start = mp_hal_ticks_us();
    while (n < size) {
        int c = ringbuf_get(&self->rxbuf);
        if (c >= 0) {
            buf[n++] = c;
            start = mp_hal_ticks_us();
            continue;
        }
        if (mp_hal_ticks_us() - start >= (n ? timeout_char_us : timeout_us)) {
            break;
        }
        mp_handle_pending(true);
    }
    if (n == 0 && size > 0) {
        *errcode = MP_EAGAIN;
        return MP_STREAM_ERROR;
    }
    return n;
}

static mp_uint_t mp_machine_uart_write(mp_obj_t self_in, const void *buf_in, mp_uint_t size, int *errcode) {
    machine_uart_obj_t *self = MP_OBJ_TO_PTR(self_in);
    return uart_send_data(self->id - 1, buf_in, size);
}

static mp_uint_t mp_machine_uart_ioctl(mp_obj_t self_in, mp_uint_t request, uintptr_t arg, int *errcode) {
    machine_uart_obj_t *self = MP_OBJ_TO_PTR(self_in);
    switch (request) {
        case MP_STREAM_POLL: {
            mp_uint_t ret = 0;
            if ((arg & MP_STREAM_POLL_RD) && ringbuf_avail(&self->rxbuf)) {
                ret |= MP_STREAM_POLL_RD;
            }
            if (arg & MP_STREAM_POLL_WR) {
                ret |= MP_STREAM_POLL_WR;
            }
            return ret;
        }
        case MP_STREAM_FLUSH:
            while (!mp_machine_uart_txdone(self)) {
                mp_handle_pending(true);
            }
            return 0;
    }
    *errcode = MP_EINVAL;
    return MP_STREAM_ERROR;
}
