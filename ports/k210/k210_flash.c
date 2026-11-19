#include "py/mphal.h"
#include "k210_flash.h"

#include "encoding.h"
#include "spi.h"

// SPI3 and chip select 0, at 25 MHz in standard (single-line) mode, as
// MaixPy's flash driver uses them (taken from the Meshtastic K210 port)

#define FLASH_SPI SPI_DEVICE_3
#define FLASH_CS SPI_CHIP_SELECT_0
#define FLASH_CLOCK 25000000

#define CMD_WRITE_ENABLE 0x06
#define CMD_READ_STATUS1 0x05
#define CMD_READ_DATA 0x03
#define CMD_PAGE_PROGRAM 0x02
#define CMD_SECTOR_ERASE 0x20
#define CMD_JEDEC_ID 0x9F
#define CMD_UNIQUE_ID 0x4B
#define STATUS_BUSY 0x01

#define READ_CHUNK 256
#define ERASE_TIMEOUT_MS 1000 // a 4 KB sector erase takes up to 400 ms
#define PROGRAM_TIMEOUT_MS 10 // a page program takes up to 3 ms

static bool initialized = false;

// The SDK feeds the SPI FIFO from the CPU. An interrupt in the middle of a
// command could let the FIFO run dry and end the command early, so each
// transfer runs with interrupts masked (a page program is about 100 us).
static uint64_t irq_mask(void) {
    uint64_t saved = read_csr(mstatus);
    clear_csr(mstatus, MSTATUS_MIE);
    return saved;
}

static void irq_restore(uint64_t saved) {
    if (saved & MSTATUS_MIE) {
        set_csr(mstatus, MSTATUS_MIE);
    }
}

static void spi_setup(void) {
    spi_init(FLASH_SPI, SPI_WORK_MODE_0, SPI_FF_STANDARD, 8, 0);
}

static void send(const uint8_t *cmd, size_t cmd_len, const uint8_t *data, size_t data_len) {
    uint64_t saved = irq_mask();
    spi_setup();
    spi_send_data_standard(FLASH_SPI, FLASH_CS, cmd, cmd_len, data, data_len);
    irq_restore(saved);
}

static void receive(const uint8_t *cmd, size_t cmd_len, uint8_t *data, size_t data_len) {
    uint64_t saved = irq_mask();
    spi_setup();
    spi_receive_data_standard(FLASH_SPI, FLASH_CS, cmd, cmd_len, data, data_len);
    irq_restore(saved);
}

static uint8_t read_status(void) {
    uint8_t cmd = CMD_READ_STATUS1, status = 0;
    receive(&cmd, 1, &status, 1);
    return status;
}

static bool wait_ready(uint32_t timeout_ms) {
    mp_uint_t start = mp_hal_ticks_ms();
    while (read_status() & STATUS_BUSY) {
        if (mp_hal_ticks_ms() - start > timeout_ms) {
            return false;
        }
    }
    return true;
}

static void write_enable(void) {
    uint8_t cmd = CMD_WRITE_ENABLE;
    send(&cmd, 1, NULL, 0);
}

static void address_command(uint8_t *cmd, uint8_t op, uint32_t addr) {
    cmd[0] = op;
    cmd[1] = addr >> 16;
    cmd[2] = addr >> 8;
    cmd[3] = addr;
}

bool k210_flash_init(void) {
    if (initialized) {
        return true;
    }
    spi_setup();
    spi_set_clk_rate(FLASH_SPI, FLASH_CLOCK);
    uint32_t id = k210_flash_jedec_id();
    // No chip, or nothing answering: all ones or all zeros
    initialized = id != 0 && id != 0xFFFFFF;
    return initialized;
}

uint32_t k210_flash_jedec_id(void) {
    uint8_t cmd = CMD_JEDEC_ID, id[3] = {0};
    receive(&cmd, 1, id, sizeof(id));
    return ((uint32_t)id[0] << 16) | ((uint32_t)id[1] << 8) | id[2];
}

bool k210_flash_unique_id(uint8_t uid[8]) {
    if (!k210_flash_init()) {
        return false;
    }
    uint8_t cmd[5] = {CMD_UNIQUE_ID, 0, 0, 0, 0}; // 4 dummy bytes
    receive(cmd, sizeof(cmd), uid, 8);
    bool all_ones = true, all_zeros = true;
    for (int i = 0; i < 8; i++) {
        all_ones &= uid[i] == 0xFF;
        all_zeros &= uid[i] == 0x00;
    }
    return !all_ones && !all_zeros;
}

bool k210_flash_read(uint32_t addr, void *buf, size_t len) {
    if (!k210_flash_init()) {
        return false;
    }
    uint8_t *dst = buf;
    while (len) {
        size_t n = len < READ_CHUNK ? len : READ_CHUNK;
        uint8_t cmd[4];
        address_command(cmd, CMD_READ_DATA, addr);
        receive(cmd, sizeof(cmd), dst, n);
        addr += n;
        dst += n;
        len -= n;
    }
    return true;
}

bool k210_flash_program(uint32_t addr, const void *buf, size_t len) {
    if (!k210_flash_init()) {
        return false;
    }
    const uint8_t *src = buf;
    while (len) {
        // A page program wraps within its page: never cross a page boundary
        size_t room = K210_FLASH_PAGE_SIZE - (addr % K210_FLASH_PAGE_SIZE);
        size_t n = len < room ? len : room;
        uint8_t cmd[4];
        address_command(cmd, CMD_PAGE_PROGRAM, addr);
        write_enable();
        send(cmd, sizeof(cmd), src, n);
        if (!wait_ready(PROGRAM_TIMEOUT_MS)) {
            return false;
        }
        addr += n;
        src += n;
        len -= n;
    }
    return true;
}

bool k210_flash_erase_sector(uint32_t addr) {
    if (!k210_flash_init()) {
        return false;
    }
    uint8_t cmd[4];
    address_command(cmd, CMD_SECTOR_ERASE, addr & ~(uint32_t)(K210_FLASH_SECTOR_SIZE - 1));
    write_enable();
    send(cmd, sizeof(cmd), NULL, 0);
    return wait_ready(ERASE_TIMEOUT_MS);
}
