// k210.AES: the K210's AES accelerator, ECB, CBC and GCM with 128, 192 and
// 256-bit keys, through the SDK's driver. ECB and CBC take the same calls as
// cryptolib.aes, GCM the ones of PyCryptodome:
//
//   k210.AES(key, k210.AES.MODE_CBC, iv).encrypt(data)
//   ct, tag = k210.AES(key, k210.AES.MODE_GCM, nonce).encrypt_and_digest(data, aad)
//   data = k210.AES(key, k210.AES.MODE_GCM, nonce).decrypt_and_verify(ct, tag, aad)
//
// The hardware runs one job at a time from a key and an IV; across calls,
// the object carries CBC's chaining (the last ciphertext block) itself. The
// SDK reads keys, IVs and data as 32-bit words, so they go through aligned
// buffers. A GCM object does one job, so that its nonce isn't used twice.

#include <string.h>

#include "py/runtime.h"

#include "aes.h"

#define MODE_ECB (1) // cryptolib's numbering
#define MODE_CBC (2)
#define MODE_GCM (11) // PyCryptodome's
#define GCM_NONCE (12)
#define GCM_TAG (16)
#define AES_BLOCK (16)
#define CHUNK (1024) // bytes through the aligned buffer at a time

typedef struct _k210_aes_obj_t {
    mp_obj_base_t base;
    uint8_t mode;
    uint8_t key_len;
    bool used; // GCM: the job is done
    uint32_t key[8];
    uint32_t iv[4];
} k210_aes_obj_t;

extern const mp_obj_type_t k210_aes_type;

// AES(key, mode, IV=None)
static mp_obj_t k210_aes_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 2, 3, false);
    k210_aes_obj_t *self = mp_obj_malloc(k210_aes_obj_t, type);

    mp_buffer_info_t keyinfo;
    mp_get_buffer_raise(args[0], &keyinfo, MP_BUFFER_READ);
    if (keyinfo.len != 16 && keyinfo.len != 24 && keyinfo.len != 32) {
        mp_raise_ValueError(MP_ERROR_TEXT("key must be 16, 24 or 32 bytes"));
    }
    self->key_len = keyinfo.len;
    memcpy(self->key, keyinfo.buf, keyinfo.len);

    self->mode = mp_obj_get_int(args[1]);
    if (self->mode != MODE_ECB && self->mode != MODE_CBC && self->mode != MODE_GCM) {
        mp_raise_ValueError(MP_ERROR_TEXT("mode must be MODE_ECB, MODE_CBC or MODE_GCM"));
    }
    self->used = false;
    memset(self->iv, 0, sizeof(self->iv));
    if (self->mode == MODE_GCM) {
        if (n_args < 3) {
            mp_raise_ValueError(MP_ERROR_TEXT("GCM needs a nonce"));
        }
        mp_buffer_info_t ivinfo;
        mp_get_buffer_raise(args[2], &ivinfo, MP_BUFFER_READ);
        if (ivinfo.len != GCM_NONCE) {
            mp_raise_ValueError(MP_ERROR_TEXT("nonce must be 12 bytes"));
        }
        memcpy(self->iv, ivinfo.buf, GCM_NONCE);
    } else if (self->mode == MODE_CBC) {
        if (n_args < 3) {
            mp_raise_ValueError(MP_ERROR_TEXT("CBC needs an IV"));
        }
        mp_buffer_info_t ivinfo;
        mp_get_buffer_raise(args[2], &ivinfo, MP_BUFFER_READ);
        if (ivinfo.len != AES_BLOCK) {
            mp_raise_ValueError(MP_ERROR_TEXT("IV must be 16 bytes"));
        }
        memcpy(self->iv, ivinfo.buf, AES_BLOCK);
    }
    return MP_OBJ_FROM_PTR(self);
}

// Feeds the job its data. Unaligned data goes through an aligned buffer,
// CHUNK bytes at a time: a job takes its data in any number of pieces.
static void run_data(const uint8_t *in, uint8_t *out, size_t len, aes_cipher_mode_t mode) {
    if ((((uintptr_t)in | (uintptr_t)out) & 3) == 0) {
        aes_process((uint8_t *)in, out, len, mode);
        return;
    }
    uint32_t buf[CHUNK / 4];
    for (size_t done = 0; done < len; done += CHUNK) {
        size_t n = len - done < CHUNK ? len - done : CHUNK;
        memcpy(buf, in + done, n);
        aes_process((uint8_t *)buf, (uint8_t *)buf, n, mode);
        memcpy(out + done, buf, n);
    }
}

static mp_obj_t aes_process_obj(size_t n_args, const mp_obj_t *args, bool encrypt) {
    k210_aes_obj_t *self = MP_OBJ_TO_PTR(args[0]);
    if (self->mode == MODE_GCM) {
        mp_raise_ValueError(MP_ERROR_TEXT("GCM: use encrypt_and_digest() or decrypt_and_verify()"));
    }
    mp_buffer_info_t in;
    mp_get_buffer_raise(args[1], &in, MP_BUFFER_READ);
    if (in.len % AES_BLOCK) {
        mp_raise_ValueError(MP_ERROR_TEXT("data must be a multiple of 16 bytes"));
    }

    // Into a new bytes object, or into the buffer given
    vstr_t vstr;
    uint8_t *out;
    if (n_args > 2) {
        mp_buffer_info_t outinfo;
        mp_get_buffer_raise(args[2], &outinfo, MP_BUFFER_WRITE);
        if (outinfo.len != in.len) {
            mp_raise_ValueError(MP_ERROR_TEXT("output must be the input's length"));
        }
        out = outinfo.buf;
    } else {
        vstr_init_len(&vstr, in.len);
        out = (uint8_t *)vstr.buf;
    }
    if (in.len == 0) {
        return n_args > 2 ? mp_const_none : mp_obj_new_bytes_from_vstr(&vstr);
    }

    // One hardware job for the whole input
    aes_cipher_mode_t mode = self->mode == MODE_CBC ? AES_CBC : AES_ECB;
    uint32_t next_iv[4];
    if (self->mode == MODE_CBC && !encrypt) {
        memcpy(next_iv, (const uint8_t *)in.buf + in.len - AES_BLOCK, AES_BLOCK);
    }
    aes_init((uint8_t *)self->key, self->key_len, (uint8_t *)self->iv, self->mode == MODE_CBC ? IV_LEN_128 : 0,
        NULL, mode, encrypt ? AES_HARD_ENCRYPTION : AES_HARD_DECRYPTION, 0, in.len);
    run_data(in.buf, out, in.len, mode);
    if (self->mode == MODE_CBC) {
        if (encrypt) {
            memcpy(self->iv, out + in.len - AES_BLOCK, AES_BLOCK);
        } else {
            memcpy(self->iv, next_iv, AES_BLOCK);
        }
    }
    return n_args > 2 ? mp_const_none : mp_obj_new_bytes_from_vstr(&vstr);
}

// encrypt(data[, out]) and decrypt(data[, out])
static mp_obj_t k210_aes_encrypt(size_t n_args, const mp_obj_t *args) {
    return aes_process_obj(n_args, args, true);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(k210_aes_encrypt_obj, 2, 3, k210_aes_encrypt);

static mp_obj_t k210_aes_decrypt(size_t n_args, const mp_obj_t *args) {
    return aes_process_obj(n_args, args, false);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(k210_aes_decrypt_obj, 2, 3, k210_aes_decrypt);


// A GCM job: data (any length) through the hardware with the AAD, the tag
// into tag. Returns the output as bytes.
static mp_obj_t gcm_job(k210_aes_obj_t *self, mp_obj_t data_in, mp_obj_t aad_in, bool encrypt, uint8_t *tag) {
    if (self->used) {
        mp_raise_ValueError(MP_ERROR_TEXT("a GCM object does one job (a new nonce for each)"));
    }
    self->used = true;
    mp_buffer_info_t in;
    mp_get_buffer_raise(data_in, &in, MP_BUFFER_READ);
    mp_buffer_info_t aad = {.buf = NULL, .len = 0};
    if (aad_in != mp_const_none) {
        mp_get_buffer_raise(aad_in, &aad, MP_BUFFER_READ);
    }
    if (in.len == 0) {
        // The hardware waits forever for data that never comes (GMAC, a tag
        // over AAD alone, isn't possible)
        mp_raise_ValueError(MP_ERROR_TEXT("GCM needs at least one byte of data"));
    }
    // The SDK reads the AAD as 32-bit words (one word even with no AAD)
    uint32_t *aad_words = m_new(uint32_t, (aad.len + 3) / 4 + 1);
    memcpy(aad_words, aad.buf, aad.len);

    vstr_t vstr;
    vstr_init_len(&vstr, in.len);
    aes_init((uint8_t *)self->key, self->key_len, (uint8_t *)self->iv, IV_LEN_96, (uint8_t *)aad_words,
        AES_GCM, encrypt ? AES_HARD_ENCRYPTION : AES_HARD_DECRYPTION, aad.len, in.len);
    run_data(in.buf, (uint8_t *)vstr.buf, in.len, AES_GCM);
    // Reading the tag also hands it to the hardware's checker, which ends
    // the job
    uint32_t tag_words[GCM_TAG / 4];
    gcm_get_tag((uint8_t *)tag_words);
    memcpy(tag, tag_words, GCM_TAG);
    m_del(uint32_t, aad_words, (aad.len + 3) / 4 + 1);
    return mp_obj_new_bytes_from_vstr(&vstr);
}

static mp_obj_t gcm_check_mode(mp_obj_t self_in) {
    k210_aes_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->mode != MODE_GCM) {
        mp_raise_ValueError(MP_ERROR_TEXT("only for MODE_GCM"));
    }
    return self_in;
}

// encrypt_and_digest(data, aad): (ciphertext, tag)
static mp_obj_t k210_aes_encrypt_and_digest(size_t n_args, const mp_obj_t *args) {
    k210_aes_obj_t *self = MP_OBJ_TO_PTR(gcm_check_mode(args[0]));
    uint8_t tag[GCM_TAG];
    mp_obj_t ct = gcm_job(self, args[1], n_args > 2 ? args[2] : mp_const_none, true, tag);
    mp_obj_t result[2] = {ct, mp_obj_new_bytes(tag, GCM_TAG)};
    return mp_obj_new_tuple(2, result);
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(k210_aes_encrypt_and_digest_obj, 2, 3, k210_aes_encrypt_and_digest);

// decrypt_and_verify(data, tag, aad): the plaintext, or ValueError when the
// tag doesn't match (the data or the AAD isn't what was sent)
static mp_obj_t k210_aes_decrypt_and_verify(size_t n_args, const mp_obj_t *args) {
    k210_aes_obj_t *self = MP_OBJ_TO_PTR(gcm_check_mode(args[0]));
    mp_buffer_info_t taginfo;
    mp_get_buffer_raise(args[2], &taginfo, MP_BUFFER_READ);
    if (taginfo.len != GCM_TAG) {
        mp_raise_ValueError(MP_ERROR_TEXT("tag must be 16 bytes"));
    }
    uint8_t tag[GCM_TAG];
    mp_obj_t pt = gcm_job(self, args[1], n_args > 3 ? args[3] : mp_const_none, false, tag);
    // In constant time
    uint8_t diff = 0;
    for (int i = 0; i < GCM_TAG; i++) {
        diff |= tag[i] ^ ((const uint8_t *)taginfo.buf)[i];
    }
    if (diff) {
        mp_raise_ValueError(MP_ERROR_TEXT("MAC check failed"));
    }
    return pt;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(k210_aes_decrypt_and_verify_obj, 3, 4, k210_aes_decrypt_and_verify);

static const mp_rom_map_elem_t k210_aes_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_encrypt), MP_ROM_PTR(&k210_aes_encrypt_obj) },
    { MP_ROM_QSTR(MP_QSTR_decrypt), MP_ROM_PTR(&k210_aes_decrypt_obj) },
    { MP_ROM_QSTR(MP_QSTR_encrypt_and_digest), MP_ROM_PTR(&k210_aes_encrypt_and_digest_obj) },
    { MP_ROM_QSTR(MP_QSTR_decrypt_and_verify), MP_ROM_PTR(&k210_aes_decrypt_and_verify_obj) },
    { MP_ROM_QSTR(MP_QSTR_MODE_ECB), MP_ROM_INT(MODE_ECB) },
    { MP_ROM_QSTR(MP_QSTR_MODE_CBC), MP_ROM_INT(MODE_CBC) },
    { MP_ROM_QSTR(MP_QSTR_MODE_GCM), MP_ROM_INT(MODE_GCM) },
};
static MP_DEFINE_CONST_DICT(k210_aes_locals_dict, k210_aes_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    k210_aes_type,
    MP_QSTR_AES,
    MP_TYPE_FLAG_NONE,
    make_new, k210_aes_make_new,
    locals_dict, &k210_aes_locals_dict
    );
