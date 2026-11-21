// hashlib for the K210: sha256 on the chip's hash unit, with MicroPython's
// software SHA-256 (lib/crypto-algorithms) where the unit can't serve.
//
// The unit wants the message's length in 64-byte blocks up front, which a
// hash fed by update() doesn't know. It compares its count with the blocks
// done only as they arrive, so the count starts at its largest and is set to
// the real one at digest(), before the padding goes in. There is one unit:
// the first sha256 object takes it until digest() (or until it's freed), and
// any other made meanwhile hashes in software. The count has 16 bits (4 MB):
// a hash that grows past it carries on in software from the unit's
// intermediate state.

#include <string.h>

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"

// The SDK's header, with its functions under the names the Makefile gives
// them, which leaves sha256_init, _update and _final to the software SHA-256
#define sha256_init k210_sha256_init
#define sha256_update k210_sha256_update
#define sha256_final k210_sha256_final
#include "sha256.h"
#undef sha256_init
#undef sha256_update
#undef sha256_final
#include "sysctl.h"

// The software SHA-256
#include "lib/crypto-algorithms/sha256.c"

// The unit's registers, defined in the SDK's sha256.c but not declared in its
// header
extern volatile sha256_t *const sha256;

#define BLOCK (64)
#define MAX_BLOCKS (0xFFFF)
#define DIGEST_LEN (32)
#define FINISH_TIMEOUT_MS (100)

typedef struct _hashlib_sha256_obj_t {
    mp_obj_base_t base;
    bool final;
    bool hw; // on the unit, else in software
    uint64_t total; // bytes so far (the unit)
    size_t buffered; // bytes in block, not yet fed (the unit)
    uint32_t block[BLOCK / 4];
    CRYAL_SHA256_CTX sw;
} hashlib_sha256_obj_t;

static hashlib_sha256_obj_t *hw_owner;

static void hw_feed_block(const uint32_t *words) {
    for (int i = 0; i < BLOCK / 4; i++) {
        while (sha256->sha_function_reg_1.fifo_in_full) {
        }
        sha256->sha_data_in1 = words[i];
    }
}

static void hw_feed(hashlib_sha256_obj_t *self, const uint8_t *data, size_t len) {
    while (len) {
        size_t n = BLOCK - self->buffered;
        if (n > len) {
            n = len;
        }
        memcpy((uint8_t *)self->block + self->buffered, data, n);
        self->buffered += n;
        data += n;
        len -= n;
        if (self->buffered == BLOCK) {
            hw_feed_block(self->block);
            self->buffered = 0;
        }
    }
}

static void hw_release(hashlib_sha256_obj_t *self) {
    if (hw_owner == self) {
        hw_owner = NULL;
    }
    self->hw = false;
}

// Waits for the unit to have hashed the given number of blocks
static void hw_wait_blocks(hashlib_sha256_obj_t *self, uint32_t blocks) {
    mp_uint_t start = mp_hal_ticks_ms();
    while (sha256->sha_num_reg.sha_data_num != (blocks & 0xFFFF)) {
        if (mp_hal_ticks_ms() - start > FINISH_TIMEOUT_MS) {
            hw_release(self);
            mp_raise_OSError(MP_ETIMEDOUT);
        }
    }
}

// Carries the hash on in software from the unit's state: the blocks hashed
// so far, and the bytes not yet fed
static void hw_to_sw(hashlib_sha256_obj_t *self) {
    uint32_t blocks = (self->total - self->buffered) / BLOCK;
    hw_wait_blocks(self, blocks);
    sha256_init(&self->sw);
    for (int i = 0; i < 8; i++) {
        self->sw.state[i] = __builtin_bswap32(sha256->sha_result[7 - i]);
    }
    self->sw.bitlen = (unsigned long long)blocks * BLOCK * 8;
    memcpy(self->sw.data, self->block, self->buffered);
    self->sw.datalen = self->buffered;
    hw_release(self);
}

static mp_obj_t hashlib_sha256_update(mp_obj_t self_in, mp_obj_t arg);

static mp_obj_t hashlib_sha256_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 1, false);
    hashlib_sha256_obj_t *self = mp_obj_malloc_with_finaliser(hashlib_sha256_obj_t, type);
    self->final = false;
    self->total = 0;
    self->buffered = 0;
    if (hw_owner == NULL) {
        hw_owner = self;
        self->hw = true;
        sysctl_clock_enable(SYSCTL_CLOCK_SHA);
        sysctl_reset(SYSCTL_RESET_SHA);
        sha256->sha_num_reg.sha_data_cnt = MAX_BLOCKS;
        sha256->sha_function_reg_1.dma_en = 0;
        sha256->sha_function_reg_0.sha_endian = SHA256_BIG_ENDIAN;
        sha256->sha_function_reg_0.sha_en = ENABLE_SHA;
    } else {
        self->hw = false;
        sha256_init(&self->sw);
    }
    if (n_args == 1) {
        hashlib_sha256_update(MP_OBJ_FROM_PTR(self), args[0]);
    }
    return MP_OBJ_FROM_PTR(self);
}

static void ensure_not_final(hashlib_sha256_obj_t *self) {
    if (self->final) {
        mp_raise_ValueError(MP_ERROR_TEXT("hash is final"));
    }
}

static mp_obj_t hashlib_sha256_update(mp_obj_t self_in, mp_obj_t arg) {
    hashlib_sha256_obj_t *self = MP_OBJ_TO_PTR(self_in);
    ensure_not_final(self);
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(arg, &bufinfo, MP_BUFFER_READ);
    // The padding (9 bytes or more) must fit the unit's count too
    if (self->hw && (self->total + bufinfo.len + 9 + BLOCK - 1) / BLOCK > MAX_BLOCKS) {
        hw_to_sw(self);
    }
    if (self->hw) {
        self->total += bufinfo.len;
        hw_feed(self, bufinfo.buf, bufinfo.len);
    } else {
        sha256_update(&self->sw, bufinfo.buf, bufinfo.len);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(hashlib_sha256_update_obj, hashlib_sha256_update);

static mp_obj_t hashlib_sha256_digest(mp_obj_t self_in) {
    hashlib_sha256_obj_t *self = MP_OBJ_TO_PTR(self_in);
    ensure_not_final(self);
    self->final = true;
    vstr_t vstr;
    vstr_init_len(&vstr, DIGEST_LEN);
    if (!self->hw) {
        sha256_final(&self->sw, (uint8_t *)vstr.buf);
        return mp_obj_new_bytes_from_vstr(&vstr);
    }

    // The real count, then the padding: 0x80, zeros, the length in bits
    uint32_t blocks = (self->total + 9 + BLOCK - 1) / BLOCK;
    sha256->sha_num_reg.sha_data_cnt = blocks;
    static const uint8_t pad[BLOCK] = {0x80};
    hw_feed(self, pad, (self->buffered < BLOCK - 8 ? BLOCK - 8 : 2 * BLOCK - 8) - self->buffered);
    uint64_t bits = self->total * 8;
    uint8_t length[8];
    for (int i = 0; i < 8; i++) {
        length[i] = bits >> (56 - 8 * i);
    }
    hw_feed(self, length, sizeof(length));
    mp_uint_t start = mp_hal_ticks_ms();
    while (!sha256->sha_function_reg_0.sha_en) { // reads 1 when done
        if (mp_hal_ticks_ms() - start > FINISH_TIMEOUT_MS) {
            hw_release(self);
            mp_raise_OSError(MP_ETIMEDOUT);
        }
    }
    uint32_t *out = (uint32_t *)vstr.buf;
    for (int i = 0; i < 8; i++) {
        out[i] = sha256->sha_result[7 - i];
    }
    hw_release(self);
    return mp_obj_new_bytes_from_vstr(&vstr);
}
static MP_DEFINE_CONST_FUN_OBJ_1(hashlib_sha256_digest_obj, hashlib_sha256_digest);

// Frees the unit when an object is dropped before its digest()
static mp_obj_t hashlib_sha256_del(mp_obj_t self_in) {
    hw_release(MP_OBJ_TO_PTR(self_in));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(hashlib_sha256_del_obj, hashlib_sha256_del);

static const mp_rom_map_elem_t hashlib_sha256_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_update), MP_ROM_PTR(&hashlib_sha256_update_obj) },
    { MP_ROM_QSTR(MP_QSTR_digest), MP_ROM_PTR(&hashlib_sha256_digest_obj) },
    { MP_ROM_QSTR(MP_QSTR___del__), MP_ROM_PTR(&hashlib_sha256_del_obj) },
};
static MP_DEFINE_CONST_DICT(hashlib_sha256_locals_dict, hashlib_sha256_locals_dict_table);

static MP_DEFINE_CONST_OBJ_TYPE(
    hashlib_sha256_type,
    MP_QSTR_sha256,
    MP_TYPE_FLAG_NONE,
    make_new, hashlib_sha256_make_new,
    locals_dict, &hashlib_sha256_locals_dict
    );

static const mp_rom_map_elem_t hashlib_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_hashlib) },
    { MP_ROM_QSTR(MP_QSTR_sha256), MP_ROM_PTR(&hashlib_sha256_type) },
};
static MP_DEFINE_CONST_DICT(hashlib_module_globals, hashlib_module_globals_table);

const mp_obj_module_t k210_hashlib_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&hashlib_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_hashlib, k210_hashlib_module);
