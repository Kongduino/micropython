// machine.SPI: the K210's SPI0 and SPI1 (DesignWare) as masters, full
// duplex. Chip select is up to the caller, with a Pin: the controller's own
// select line isn't routed to any pin.

#include "py/runtime.h"
#include "py/mphal.h"
#include "extmod/modmachine.h"

#include "fpioa.h"
#include "spi.h"

#define SPI_FIFO_DEPTH (32)
#define SPI_TMOD_OFFSET (8) // in ctrlr0, for SPI0 and SPI1
#define SPI_DEFAULT_BAUDRATE (1000000)

typedef struct _machine_spi_obj_t {
    mp_obj_base_t base;
    uint8_t id;
    uint8_t polarity;
    uint8_t phase;
    uint8_t bits;
    uint8_t sck;
    uint8_t mosi;
    uint8_t miso;
    uint32_t baudrate;
} machine_spi_obj_t;

#define NO_PIN (0xFF)

// SPI1 defaults to the SD card slot's pins
static machine_spi_obj_t machine_spi_obj[2] = {
    {{&machine_spi_type}, 0, 0, 0, 8, NO_PIN, NO_PIN, NO_PIN, SPI_DEFAULT_BAUDRATE},
    {{&machine_spi_type}, 1, 0, 0, 8, 11, 10, 6, SPI_DEFAULT_BAUDRATE},
};

static const uint8_t spi_sck_function[2] = {FUNC_SPI0_SCLK, FUNC_SPI1_SCLK};
static const uint8_t spi_mosi_function[2] = {FUNC_SPI0_D0, FUNC_SPI1_D0};
static const uint8_t spi_miso_function[2] = {FUNC_SPI0_D1, FUNC_SPI1_D1};

static void machine_spi_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    machine_spi_obj_t *self = MP_OBJ_TO_PTR(self_in);
    mp_printf(print, "SPI(%u, baudrate=%u, polarity=%u, phase=%u, bits=%u, sck=%u, mosi=%u, miso=%u)",
        self->id, self->baudrate, self->polarity, self->phase, self->bits, self->sck, self->mosi, self->miso);
}

static void machine_spi_init(mp_obj_base_t *self_in, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    machine_spi_obj_t *self = (machine_spi_obj_t *)self_in;
    enum { ARG_baudrate, ARG_polarity, ARG_phase, ARG_bits, ARG_firstbit, ARG_sck, ARG_mosi, ARG_miso };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_baudrate, MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_polarity, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_phase, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_bits, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = -1} },
        { MP_QSTR_firstbit, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = MICROPY_PY_MACHINE_SPI_MSB} },
        { MP_QSTR_sck, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_mosi, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
        { MP_QSTR_miso, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_NONE} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_baudrate].u_int > 0) {
        self->baudrate = args[ARG_baudrate].u_int;
    }
    if (args[ARG_polarity].u_int >= 0) {
        self->polarity = args[ARG_polarity].u_int & 1;
    }
    if (args[ARG_phase].u_int >= 0) {
        self->phase = args[ARG_phase].u_int & 1;
    }
    if (args[ARG_bits].u_int >= 0) {
        if (args[ARG_bits].u_int != 8) {
            mp_raise_ValueError(MP_ERROR_TEXT("only 8 bits supported"));
        }
        self->bits = 8;
    }
    if (args[ARG_firstbit].u_int != MICROPY_PY_MACHINE_SPI_MSB) {
        mp_raise_ValueError(MP_ERROR_TEXT("only MSB first supported"));
    }
    if (args[ARG_sck].u_obj != mp_const_none) {
        self->sck = mp_hal_get_pin_obj(args[ARG_sck].u_obj);
    }
    if (args[ARG_mosi].u_obj != mp_const_none) {
        self->mosi = mp_hal_get_pin_obj(args[ARG_mosi].u_obj);
    }
    if (args[ARG_miso].u_obj != mp_const_none) {
        self->miso = mp_hal_get_pin_obj(args[ARG_miso].u_obj);
    }
    if (self->sck == NO_PIN || (self->mosi == NO_PIN && self->miso == NO_PIN)) {
        mp_raise_ValueError(MP_ERROR_TEXT("sck and mosi or miso pins needed"));
    }

    machine_pin_set_function(self->sck, spi_sck_function[self->id]);
    if (self->mosi != NO_PIN) {
        machine_pin_set_function(self->mosi, spi_mosi_function[self->id]);
    }
    if (self->miso != NO_PIN) {
        machine_pin_set_function(self->miso, spi_miso_function[self->id]);
    }
    spi_init(self->id, (self->polarity << 1) | self->phase, SPI_FF_STANDARD, self->bits, 0);
    self->baudrate = spi_set_clk_rate(self->id, self->baudrate);
    volatile spi_t *regs = spi[self->id];
    regs->ctrlr0 = (regs->ctrlr0 & ~(3U << SPI_TMOD_OFFSET)) | (SPI_TMOD_TRANS_RECV << SPI_TMOD_OFFSET);
}

// SPI(id, baudrate=1000000, *, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck, mosi, miso)
static mp_obj_t machine_spi_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 1, MP_OBJ_FUN_ARGS_MAX, true);
    mp_int_t id = mp_obj_get_int(args[0]);
    if (id < 0 || id >= MP_ARRAY_SIZE(machine_spi_obj)) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("SPI(%d) doesn't exist"), id);
    }
    machine_spi_obj_t *self = &machine_spi_obj[id];
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    machine_spi_init(&self->base, n_args - 1, args + 1, &kw_args);
    return MP_OBJ_FROM_PTR(self);
}

static void machine_spi_transfer(mp_obj_base_t *self_in, size_t len, const uint8_t *src, uint8_t *dest) {
    machine_spi_obj_t *self = (machine_spi_obj_t *)self_in;
    volatile spi_t *regs = spi[self->id];

    regs->ssienr = 1;
    regs->ser = 1;
    size_t sent = 0, received = 0;
    while (received < len) {
        // Keep no more bytes in flight than the receive FIFO holds
        while (sent < len && sent - received < SPI_FIFO_DEPTH && regs->txflr < SPI_FIFO_DEPTH) {
            regs->dr[0] = src ? src[sent] : 0xFF;
            sent++;
        }
        while (regs->rxflr) {
            uint8_t byte = regs->dr[0];
            if (dest) {
                dest[received] = byte;
            }
            received++;
        }
    }
    regs->ser = 0;
    regs->ssienr = 0;
}

static const mp_machine_spi_p_t machine_spi_p = {
    .init = machine_spi_init,
    .transfer = machine_spi_transfer,
};

MP_DEFINE_CONST_OBJ_TYPE(
    machine_spi_type,
    MP_QSTR_SPI,
    MP_TYPE_FLAG_NONE,
    make_new, machine_spi_make_new,
    print, machine_spi_print,
    protocol, &machine_spi_p,
    locals_dict, &mp_machine_spi_locals_dict
    );
