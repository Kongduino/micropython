// The Amigo's 16 MB SPI flash (the chip the K210 boots from), on SPI3
#ifndef MICROPY_INCLUDED_K210_K210_FLASH_H
#define MICROPY_INCLUDED_K210_K210_FLASH_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define K210_FLASH_PAGE_SIZE 256
#define K210_FLASH_SECTOR_SIZE 4096

bool k210_flash_init(void);
uint32_t k210_flash_jedec_id(void);
bool k210_flash_read(uint32_t addr, void *buf, size_t len);
bool k210_flash_program(uint32_t addr, const void *buf, size_t len);
bool k210_flash_erase_sector(uint32_t addr);

#endif // MICROPY_INCLUDED_K210_K210_FLASH_H
