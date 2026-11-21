// The k210 module: k210.Flash, the file system's block device, k210.AES
// (k210_aes.c), k210.LCD (k210_lcd.c) and k210.SDCard (k210_sdcard.c)

#include "py/runtime.h"
#include "py/mperrno.h"
#include "extmod/vfs.h"
#include "k210_flash.h"

// The file system's part of the flash: the 1 MB at 0xC00000, clear of
// Meshtastic's LittleFS (0x400000-0x5FFFFF) and MaixPy's SPIFFS
// (0xD00000-0xFFFFFF), so both stay as they are (see the Maix_Amigo repo's
// docs/app-launcher.md for the flash layout)
#define FS_FLASH_BASE 0xC00000
#define FS_FLASH_SIZE (1024 * 1024)
#define BLOCK_SIZE K210_FLASH_SECTOR_SIZE

typedef struct _k210_flash_obj_t {
    mp_obj_base_t base;
} k210_flash_obj_t;

static const mp_obj_type_t k210_flash_type;
static const k210_flash_obj_t k210_flash_obj = {{&k210_flash_type}};

static mp_obj_t k210_flash_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 0, 0, false);
    if (!k210_flash_init()) {
        mp_raise_OSError(MP_EIO);
    }
    return MP_OBJ_FROM_PTR(&k210_flash_obj);
}

// readblocks(block, buf[, offset]) and writeblocks(block, buf[, offset]): the
// extended block device protocol, which littlefs uses. writeblocks without an
// offset erases the blocks first.
static mp_obj_t k210_flash_readblocks(size_t n_args, const mp_obj_t *args) {
    uint32_t addr = FS_FLASH_BASE + mp_obj_get_int(args[1]) * BLOCK_SIZE;
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[2], &bufinfo, MP_BUFFER_WRITE);
    if (n_args == 4) {
        addr += mp_obj_get_int(args[3]);
    }
    if (addr + bufinfo.len > FS_FLASH_BASE + FS_FLASH_SIZE || !k210_flash_read(addr, bufinfo.buf, bufinfo.len)) {
        mp_raise_OSError(MP_EIO);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(k210_flash_readblocks_obj, 3, 4, k210_flash_readblocks);

static mp_obj_t k210_flash_writeblocks(size_t n_args, const mp_obj_t *args) {
    uint32_t addr = FS_FLASH_BASE + mp_obj_get_int(args[1]) * BLOCK_SIZE;
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[2], &bufinfo, MP_BUFFER_READ);
    if (n_args == 4) {
        addr += mp_obj_get_int(args[3]);
    }
    if (addr + bufinfo.len > FS_FLASH_BASE + FS_FLASH_SIZE) {
        mp_raise_OSError(MP_EIO);
    }
    if (n_args == 3) {
        for (uint32_t a = addr; a < addr + bufinfo.len; a += BLOCK_SIZE) {
            if (!k210_flash_erase_sector(a)) {
                mp_raise_OSError(MP_EIO);
            }
        }
    }
    if (!k210_flash_program(addr, bufinfo.buf, bufinfo.len)) {
        mp_raise_OSError(MP_EIO);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(k210_flash_writeblocks_obj, 3, 4, k210_flash_writeblocks);

static mp_obj_t k210_flash_ioctl(mp_obj_t self_in, mp_obj_t cmd_in, mp_obj_t arg_in) {
    switch (mp_obj_get_int(cmd_in)) {
        case MP_BLOCKDEV_IOCTL_INIT:
        case MP_BLOCKDEV_IOCTL_DEINIT:
        case MP_BLOCKDEV_IOCTL_SYNC:
            return MP_OBJ_NEW_SMALL_INT(0);
        case MP_BLOCKDEV_IOCTL_BLOCK_COUNT:
            return MP_OBJ_NEW_SMALL_INT(FS_FLASH_SIZE / BLOCK_SIZE);
        case MP_BLOCKDEV_IOCTL_BLOCK_SIZE:
            return MP_OBJ_NEW_SMALL_INT(BLOCK_SIZE);
        case MP_BLOCKDEV_IOCTL_BLOCK_ERASE: {
            uint32_t block = mp_obj_get_int(arg_in);
            if (block >= FS_FLASH_SIZE / BLOCK_SIZE || !k210_flash_erase_sector(FS_FLASH_BASE + block * BLOCK_SIZE)) {
                return MP_OBJ_NEW_SMALL_INT(-MP_EIO);
            }
            return MP_OBJ_NEW_SMALL_INT(0);
        }
        default:
            return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_3(k210_flash_ioctl_obj, k210_flash_ioctl);

static const mp_rom_map_elem_t k210_flash_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_readblocks), MP_ROM_PTR(&k210_flash_readblocks_obj) },
    { MP_ROM_QSTR(MP_QSTR_writeblocks), MP_ROM_PTR(&k210_flash_writeblocks_obj) },
    { MP_ROM_QSTR(MP_QSTR_ioctl), MP_ROM_PTR(&k210_flash_ioctl_obj) },
};
static MP_DEFINE_CONST_DICT(k210_flash_locals_dict, k210_flash_locals_dict_table);

static MP_DEFINE_CONST_OBJ_TYPE(
    k210_flash_type,
    MP_QSTR_Flash,
    MP_TYPE_FLAG_NONE,
    make_new, k210_flash_make_new,
    locals_dict, &k210_flash_locals_dict
    );

extern const mp_obj_type_t k210_aes_type;
extern const mp_obj_type_t k210_lcd_type;
extern const mp_obj_type_t k210_sdcard_type;

static const mp_rom_map_elem_t k210_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_k210) },
    { MP_ROM_QSTR(MP_QSTR_AES), MP_ROM_PTR(&k210_aes_type) },
    { MP_ROM_QSTR(MP_QSTR_Flash), MP_ROM_PTR(&k210_flash_type) },
    { MP_ROM_QSTR(MP_QSTR_LCD), MP_ROM_PTR(&k210_lcd_type) },
    { MP_ROM_QSTR(MP_QSTR_SDCard), MP_ROM_PTR(&k210_sdcard_type) },
};
static MP_DEFINE_CONST_DICT(k210_module_globals, k210_module_globals_table);

const mp_obj_module_t k210_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&k210_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_k210, k210_module);
