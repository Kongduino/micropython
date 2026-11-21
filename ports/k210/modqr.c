// qr: QR codes found in a greyscale picture, with quirc (Daniel Beer's QR
// code library, ISC licence, in quirc/), built with single precision floats,
// which the K210's FPU has.
//
//   import qr
//   qr.decode(buf, width, height)       # [b'payload', ...]
//   qr.decode(buf, w, h, corners=True)  # [(b'payload', ((x, y), ...)), ...]
//
// buf holds a byte a pixel (framebuf.GS8's layout, as Camera.grey() gives).
// A code that is found but can't be read (blurred, cut off) is left out; a
// mirrored one is read too.

#include <string.h>

#include "py/runtime.h"

#include "quirc/quirc.h"

// The decoder, kept from one call to the next (its buffers are the
// picture's size); in the SDK's heap, not MicroPython's
static struct quirc *decoder;

static mp_obj_t qr_decode(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_buf, ARG_width, ARG_height, ARG_corners };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_buf, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_width, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_height, MP_ARG_REQUIRED | MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_corners, MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = false} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    mp_int_t w = args[ARG_width].u_int, h = args[ARG_height].u_int;
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[ARG_buf].u_obj, &bufinfo, MP_BUFFER_READ);
    if (w <= 0 || h <= 0 || bufinfo.len < (size_t)(w * h)) {
        mp_raise_ValueError(MP_ERROR_TEXT("buffer smaller than width * height"));
    }

    if (decoder == NULL) {
        decoder = quirc_new();
        if (decoder == NULL) {
            mp_raise_msg(&mp_type_MemoryError, NULL);
        }
    }
    int qw, qh;
    quirc_begin(decoder, &qw, &qh);
    if (qw != w || qh != h) {
        if (quirc_resize(decoder, w, h) < 0) {
            mp_raise_msg(&mp_type_MemoryError, NULL);
        }
    }
    uint8_t *image = quirc_begin(decoder, NULL, NULL);
    memcpy(image, bufinfo.buf, w * h);
    quirc_end(decoder);

    mp_obj_t found = mp_obj_new_list(0, NULL);
    int count = quirc_count(decoder);
    for (int i = 0; i < count; i++) {
        // Static: struct quirc_data is about 9 KB, much for the stack
        static struct quirc_code code;
        static struct quirc_data data;
        quirc_extract(decoder, i, &code);
        quirc_decode_error_t err = quirc_decode(&code, &data);
        if (err == QUIRC_ERROR_DATA_ECC) {
            quirc_flip(&code);
            err = quirc_decode(&code, &data);
        }
        if (err != QUIRC_SUCCESS) {
            continue;
        }
        mp_obj_t payload = mp_obj_new_bytes(data.payload, data.payload_len);
        if (args[ARG_corners].u_bool) {
            mp_obj_t corners[4];
            for (int k = 0; k < 4; k++) {
                mp_obj_t xy[2] = {MP_OBJ_NEW_SMALL_INT(code.corners[k].x), MP_OBJ_NEW_SMALL_INT(code.corners[k].y)};
                corners[k] = mp_obj_new_tuple(2, xy);
            }
            mp_obj_t item[2] = {payload, mp_obj_new_tuple(4, corners)};
            payload = mp_obj_new_tuple(2, item);
        }
        mp_obj_list_append(found, payload);
    }
    return found;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(qr_decode_obj, 3, qr_decode);

static const mp_rom_map_elem_t qr_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_qr) },
    { MP_ROM_QSTR(MP_QSTR_decode), MP_ROM_PTR(&qr_decode_obj) },
};
static MP_DEFINE_CONST_DICT(qr_module_globals, qr_module_globals_table);

const mp_obj_module_t qr_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&qr_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_qr, qr_module);
