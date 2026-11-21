// The port's part of machine.I2S, included by extmod/machine_i2s.c: the
// K210's three I2S controllers (DesignWare), as controller (they drive SCK,
// WS and MCK), with the pins given through the FPIOA. TX goes out on the
// controller's channel 2 and RX comes in on channel 0, as MaixPy has them.
//
// The samples go through a DMA channel per controller, into or out of a
// buffer in two halves: while the DMA moves one, the interrupt at its end
// starts the other and refills (or empties) the one done, from (or into)
// the ring buffer the shared code fills (or reads). The buffers are used
// through their uncached alias, as the DMA reads and writes RAM.
//
// The DMA moves a 32-bit word a sample, left then right. The controller
// always works in 32-bit samples (a 16-bit sample is the top half of one,
// the low half zero), so a 16-bit codec sees its 16 bits first, as I2S has
// them. (Set to 16-bit samples, the transmitter would send a word's top
// half anyway, while the receiver gives its low half.)
//
// The pins are set to the weakest drive: at full drive, MCK and SCK disturb
// the Amigo's internal I2C bus (IO24/IO27), which then loses arbitration in
// one transfer in a few.
//
// The clocks come from PLL2, set for each rate so that MCK is 256 times the
// rate (what codecs such as the Amigo's ES8374 want) and SCK 64 times (32
// cycles a sample): PLL2 is 512 * rate * n, MCK PLL2 / (2 * n), SCK
// PLL2 / (8 * n). PLL2 is one for the three controllers: all run at the
// last rate set.

#include <string.h>

#include "py/mphal.h"

#include "dmac.h"
#include "fpioa.h"
#include "i2s.h"
#include "sysctl.h"

#define MAX_I2S_K210 (3)
#define SIZEOF_DMA_BUFFER_IN_BYTES (2048)
#define SIZEOF_HALF_DMA_BUFFER_IN_BYTES (SIZEOF_DMA_BUFFER_IN_BYTES / 2)
#define DMA_FRAME_SIZE_IN_BYTES (8)

// For non-blocking mode, to avoid underflow/overflow, sample data is written/read to/from the ring buffer at a rate faster
// than the DMA transfer rate
#define NON_BLOCKING_RATE_MULTIPLIER (4)
#define SIZEOF_NON_BLOCKING_COPY_IN_BYTES (SIZEOF_HALF_DMA_BUFFER_IN_BYTES * NON_BLOCKING_RATE_MULTIPLIER)

#define FUNC_I2S_STRIDE (FUNC_I2S1_MCLK - FUNC_I2S0_MCLK)
#define DMA_PRIORITY (3)
#define TX_CHANNEL (I2S_CHANNEL_2)
#define RX_CHANNEL (I2S_CHANNEL_0)

typedef enum {
    RX,
    TX
} i2s_mode_t;

typedef struct _machine_i2s_obj_t {
    mp_obj_base_t base;
    uint8_t i2s_id;
    bool active;
    mp_hal_pin_obj_t sck;
    mp_hal_pin_obj_t ws;
    mp_hal_pin_obj_t sd;
    mp_hal_pin_obj_t mck;
    i2s_mode_t mode;
    int8_t bits;
    format_t format;
    int32_t rate;
    int32_t ibuf;
    mp_obj_t callback_for_non_blocking;
    io_mode_t io_mode;
    uint8_t dma_half; // the half the DMA is moving
    ring_buf_t ring_buffer;
    uint8_t *ring_buffer_storage;
    non_blocking_descriptor_t non_blocking_descriptor;
} machine_i2s_obj_t;

// The DMA's buffers, one per controller
static uint8_t dma_mem[MAX_I2S_K210][SIZEOF_DMA_BUFFER_IN_BYTES] __attribute__((aligned(64)));

static const dmac_channel_number_t dma_channel[MAX_I2S_K210] = {
    DMAC_CHANNEL2, DMAC_CHANNEL3, DMAC_CHANNEL4, // DMAC_CHANNEL5 is the screen's
};

// The frame map is used with the readinto() method to transform the audio
// sample data coming from DMA memory (a 32-bit word a sample, left then
// right) to the format specified in the I2S constructor, e.g. 16-bit mono
static const int8_t i2s_frame_map[NUM_I2S_USER_FORMATS][I2S_RX_FRAME_SIZE_IN_BYTES] = {
    {-1, -1,  0,  1, -1, -1, -1, -1 },  // Mono, 16-bits
    { 0,  1,  2,  3, -1, -1, -1, -1 },  // Mono, 32-bits
    {-1, -1,  0,  1, -1, -1,  2,  3 },  // Stereo, 16-bits
    { 0,  1,  2,  3,  4,  5,  6,  7 },  // Stereo, 32-bits
};

static uint8_t *dma_buffer(machine_i2s_obj_t *self, int half) {
    return (uint8_t *)((uintptr_t)dma_mem[self->i2s_id] - 0x40000000) + half * SIZEOF_HALF_DMA_BUFFER_IN_BYTES;
}

static int8_t get_frame_mapping_index(int8_t bits, format_t format) {
    if (format == MONO) {
        return bits == 16 ? 0 : 1;
    } else {
        return bits == 16 ? 2 : 3;
    }
}

// function is used in IRQ context
static void empty_dma(machine_i2s_obj_t *self, uint8_t *dma_buffer_p) {
    // when space exists, copy samples into ring buffer
    if (ringbuf_available_space(&self->ring_buffer) >= SIZEOF_HALF_DMA_BUFFER_IN_BYTES) {
        for (uint32_t i = 0; i < SIZEOF_HALF_DMA_BUFFER_IN_BYTES; i++) {
            ringbuf_push(&self->ring_buffer, dma_buffer_p[i]);
        }
    }
}

// function is used in IRQ context
static void feed_dma(machine_i2s_obj_t *self, uint8_t *dma_buffer_p) {
    // when data exists, copy samples from ring buffer: a frame of the DMA
    // buffer (8 bytes) takes 2, 4 or 8 bytes of the app's samples, a mono
    // sample going to both channels
    uint32_t sample_bytes = self->bits / 8;
    uint32_t frame_bytes = sample_bytes * (self->format == STEREO ? 2 : 1);
    uint32_t frames = SIZEOF_HALF_DMA_BUFFER_IN_BYTES / DMA_FRAME_SIZE_IN_BYTES;
    uint32_t *words = (uint32_t *)dma_buffer_p;
    if (ringbuf_available_data(&self->ring_buffer) < frames * frame_bytes) {
        // underflow: silence
        memset(dma_buffer_p, 0, SIZEOF_HALF_DMA_BUFFER_IN_BYTES);
        return;
    }
    for (uint32_t i = 0; i < frames; i++) {
        uint32_t sample[2] = {0, 0};
        for (int ch = 0; ch < (self->format == STEREO ? 2 : 1); ch++) {
            uint8_t *b = (uint8_t *)&sample[ch];
            for (uint32_t k = 0; k < sample_bytes; k++) {
                ringbuf_pop(&self->ring_buffer, &b[k]);
            }
        }
        if (sample_bytes == 2) {
            sample[0] <<= 16;
            sample[1] <<= 16;
        }
        words[2 * i] = sample[0];
        words[2 * i + 1] = self->format == STEREO ? sample[1] : sample[0];
    }
}

static void dma_start(machine_i2s_obj_t *self, int half) {
    volatile i2s_t *regs = i2s[self->i2s_id];
    dmac_channel_number_t ch = dma_channel[self->i2s_id];
    self->dma_half = half;
    if (self->mode == TX) {
        dmac_set_single_mode(ch, dma_buffer(self, half), (void *)&regs->txdma, DMAC_ADDR_INCREMENT,
            DMAC_ADDR_NOCHANGE, DMAC_MSIZE_1, DMAC_TRANS_WIDTH_32, SIZEOF_HALF_DMA_BUFFER_IN_BYTES / 4);
    } else {
        dmac_set_single_mode(ch, (void *)&regs->rxdma, dma_buffer(self, half), DMAC_ADDR_NOCHANGE,
            DMAC_ADDR_INCREMENT, DMAC_MSIZE_1, DMAC_TRANS_WIDTH_32, SIZEOF_HALF_DMA_BUFFER_IN_BYTES / 4);
    }
}

// The end of a half: the DMA goes on with the other, and the one done is
// refilled (TX) or emptied (RX)
static int dma_irq_handler(void *ctx) {
    machine_i2s_obj_t *self = ctx;
    int done = self->dma_half;
    dma_start(self, done ^ 1);
    if (self->mode == TX) {
        // for non-blocking operation handle the write() method requests.
        if ((self->io_mode == NON_BLOCKING) && (self->non_blocking_descriptor.copy_in_progress)) {
            copy_appbuf_to_ringbuf_non_blocking(self);
        }
        feed_dma(self, dma_buffer(self, done));
    } else {
        empty_dma(self, dma_buffer(self, done));
        // for non-blocking operation handle the readinto() method requests.
        if ((self->io_mode == NON_BLOCKING) && (self->non_blocking_descriptor.copy_in_progress)) {
            fill_appbuf_from_ringbuf_non_blocking(self);
        }
    }
    return 0;
}

// PLL2 and the dividers for a rate; returns the rate they give. PLL2 makes
// 26 MHz * nf / no (its reference can't be divided: 13 MHz is below its
// least), nf 14 to 64 (the VCO 364 MHz to 1.66 GHz), no 1 to 16; the rate is
// PLL2 / (512 * n). The closest of those, PLL2 up to 400 MHz: within 0.1% at
// the usual rates.
static uint32_t set_rate(machine_i2s_obj_t *self, uint32_t rate) {
    const uint64_t fin = 26000000;
    uint64_t best_err = UINT64_MAX;
    uint32_t best_n = 1, best_freq = 0;
    for (uint32_t n = 1; n <= 64; n++) {
        for (uint32_t no = 1; no <= 16; no++) {
            for (uint32_t nf = 14; nf <= 64; nf++) {
                uint64_t fout = fin * nf / no;
                if (fout > 400000000) {
                    break;
                }
                uint64_t want = (uint64_t)rate * 512 * n;
                uint64_t err = fout > want ? fout - want : want - fout;
                // relative to the rate: err / want, compared across n
                err = err * 1000000 / want;
                if (err < best_err) {
                    best_err = err;
                    best_n = n;
                    best_freq = fout;
                }
            }
        }
    }
    uint32_t pll2 = sysctl_pll_set_freq(SYSCTL_PLL2, best_freq);
    sysctl_clock_set_threshold(SYSCTL_THRESHOLD_I2S0_M + self->i2s_id, best_n - 1);
    sysctl_clock_set_threshold(SYSCTL_THRESHOLD_I2S0 + self->i2s_id, 4 * best_n - 1);
    return (pll2 + 256 * best_n) / (512 * best_n);
}

static void mp_machine_i2s_init_helper(machine_i2s_obj_t *self, mp_arg_val_t *args) {
    mp_hal_pin_obj_t sck = mp_hal_get_pin_obj(args[ARG_sck].u_obj);
    mp_hal_pin_obj_t ws = mp_hal_get_pin_obj(args[ARG_ws].u_obj);
    mp_hal_pin_obj_t sd = mp_hal_get_pin_obj(args[ARG_sd].u_obj);
    mp_hal_pin_obj_t mck = args[ARG_mck].u_obj == mp_const_none ? 0xFF : mp_hal_get_pin_obj(args[ARG_mck].u_obj);

    i2s_mode_t i2s_mode = args[ARG_mode].u_int;
    if (i2s_mode != RX && i2s_mode != TX) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid mode"));
    }
    int8_t i2s_bits = args[ARG_bits].u_int;
    if (i2s_bits != 16 && i2s_bits != 32) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid bits"));
    }
    format_t i2s_format = args[ARG_format].u_int;
    if (i2s_format != MONO && i2s_format != STEREO) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid format"));
    }
    int32_t rate = args[ARG_rate].u_int;
    if (rate < 4000 || rate > 192000) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid rate"));
    }
    int32_t ring_buffer_len = args[ARG_ibuf].u_int;
    if (ring_buffer_len <= 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid ibuf"));
    }
    self->ring_buffer_storage = m_new(uint8_t, ring_buffer_len);
    ringbuf_init(&self->ring_buffer, self->ring_buffer_storage, ring_buffer_len);

    self->sck = sck;
    self->ws = ws;
    self->sd = sd;
    self->mck = mck;
    self->mode = i2s_mode;
    self->bits = i2s_bits;
    self->format = i2s_format;
    self->ibuf = ring_buffer_len;
    self->callback_for_non_blocking = MP_OBJ_NULL;
    self->non_blocking_descriptor.copy_in_progress = false;
    self->io_mode = BLOCKING;

    // The controller, its channel 0, and the clocks
    int id = self->i2s_id;
    i2s_init(id, i2s_mode == TX ? I2S_TRANSMITTER : I2S_RECEIVER,
        0x3 << (2 * (i2s_mode == TX ? TX_CHANNEL : RX_CHANNEL)));
    i2s_word_length_t word_length = RESOLUTION_32_BIT;
    if (i2s_mode == TX) {
        i2s_tx_channel_config(id, TX_CHANNEL, word_length, SCLK_CYCLES_32, TRIGGER_LEVEL_4, STANDARD_MODE);
    } else {
        i2s_rx_channel_config(id, RX_CHANNEL, word_length, SCLK_CYCLES_32, TRIGGER_LEVEL_4, STANDARD_MODE);
    }
    self->rate = set_rate(self, rate);

    int func = FUNC_I2S_STRIDE * id;
    machine_pin_set_function(sck, FUNC_I2S0_SCLK + func);
    machine_pin_set_function(ws, FUNC_I2S0_WS + func);
    machine_pin_set_function(sd, (i2s_mode == TX ? FUNC_I2S0_OUT_D0 + TX_CHANNEL : FUNC_I2S0_IN_D0 + RX_CHANNEL) + func);
    fpioa_set_io_driving(sck, FPIOA_DRIVING_0);
    fpioa_set_io_driving(ws, FPIOA_DRIVING_0);
    fpioa_set_io_driving(sd, FPIOA_DRIVING_0);
    if (mck != 0xFF) {
        machine_pin_set_function(mck, FUNC_I2S0_MCLK + func);
        fpioa_set_io_driving(mck, FPIOA_DRIVING_0);
    }

    // The DMA: both halves silent to start with, then the first half
    memset(dma_buffer(self, 0), 0, SIZEOF_DMA_BUFFER_IN_BYTES);
    dmac_channel_number_t ch = dma_channel[id];
    sysctl_dma_select((sysctl_dma_channel_t)ch,
        (i2s_mode == TX ? SYSCTL_DMA_SELECT_I2S0_TX_REQ : SYSCTL_DMA_SELECT_I2S0_RX_REQ) + 2 * id);
    dmac_irq_register(ch, dma_irq_handler, self, DMA_PRIORITY);
    self->active = true;
    dma_start(self, 0);
}

static machine_i2s_obj_t *mp_machine_i2s_make_new_instance(mp_int_t i2s_id) {
    if (i2s_id < 0 || i2s_id >= MAX_I2S_K210) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid id"));
    }
    machine_i2s_obj_t *self;
    if (MP_STATE_PORT(machine_i2s_obj[i2s_id]) == NULL) {
        self = mp_obj_malloc(machine_i2s_obj_t, &machine_i2s_type);
        MP_STATE_PORT(machine_i2s_obj[i2s_id]) = self;
        self->i2s_id = i2s_id;
        self->active = false;
    } else {
        self = MP_STATE_PORT(machine_i2s_obj[i2s_id]);
        mp_machine_i2s_deinit(self);
    }
    return self;
}

static void mp_machine_i2s_deinit(machine_i2s_obj_t *self) {
    if (!self->active) {
        return;
    }
    dmac_channel_number_t ch = dma_channel[self->i2s_id];
    dmac_irq_unregister(ch);
    dmac_channel_disable(ch);
    volatile i2s_t *regs = i2s[self->i2s_id];
    regs->iter = 0; // transmitter off
    regs->irer = 0; // receiver off
    regs->ier = 0; // the controller off
    sysctl_clock_disable(SYSCTL_CLOCK_I2S0 + self->i2s_id);
    m_free(self->ring_buffer_storage);
    self->active = false;
}

static void mp_machine_i2s_irq_update(machine_i2s_obj_t *self) {
    (void)self;
}

// Stops the I2S controllers at a soft reset
void machine_i2s_deinit_all(void) {
    for (int i = 0; i < MAX_I2S_K210; i++) {
        machine_i2s_obj_t *self = MP_STATE_PORT(machine_i2s_obj[i]);
        if (self != NULL) {
            mp_machine_i2s_deinit(self);
            MP_STATE_PORT(machine_i2s_obj[i]) = NULL;
        }
    }
}

MP_REGISTER_ROOT_POINTER(void *machine_i2s_obj[3]);
