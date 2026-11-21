#include <stdint.h>

// Options to control how MicroPython is built for the K210

#define MICROPY_CONFIG_ROM_LEVEL          (MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES)

#define MICROPY_ENABLE_COMPILER           (1)
#define MICROPY_ENABLE_GC                 (1)
#define MICROPY_ENABLE_FINALISER          (1)
#define MICROPY_GCREGS_SETJMP             (0)
#define MICROPY_HELPER_REPL               (1)
#define MICROPY_REPL_AUTO_INDENT          (1)
#define MICROPY_KBD_EXCEPTION             (1)
#define MICROPY_ENABLE_SCHEDULER          (1)
#define MICROPY_LONGINT_IMPL              (MICROPY_LONGINT_IMPL_MPZ)
#define MICROPY_FLOAT_IMPL                (MICROPY_FLOAT_IMPL_FLOAT)
#define MICROPY_ALLOC_PATH_MAX            (256)
#define MICROPY_STACK_CHECK               (1)

#define MICROPY_PY_BUILTINS_HELP          (1)
#define MICROPY_PY_BUILTINS_HELP_MODULES  (1)
#define MICROPY_PY_SYS_STDFILES           (1)
#define MICROPY_STREAMS_NON_BLOCK         (1)
#define MICROPY_PY_SYS_PLATFORM           "k210"
#define MICROPY_EPOCH_IS_1970             (1)
#define MICROPY_PY_TIME                   (1)
#define MICROPY_PY_TIME_GMTIME_LOCALTIME_MKTIME (1)
#define MICROPY_PY_TIME_TIME_TIME_NS      (1)
#define MICROPY_PY_TIME_INCLUDEFILE       "ports/k210/modtime.c"

#define MICROPY_PY_MACHINE                (1)
#define MICROPY_PY_MACHINE_INCLUDEFILE    "ports/k210/modmachine.c"
#define MICROPY_PY_MACHINE_RESET          (1)
#define MICROPY_PY_MACHINE_MEMX           (1)
#define MICROPY_PY_MACHINE_BARE_METAL_FUNCS (1)
#define MICROPY_PY_MACHINE_PIN_MAKE_NEW   mp_pin_make_new
#define MICROPY_PY_MACHINE_I2C            (1)
#define MICROPY_PY_MACHINE_I2C_TRANSFER_WRITE1 (1)
#define MICROPY_PY_MACHINE_SOFTI2C        (1)
#define MICROPY_PY_MACHINE_SPI            (1)
#define MICROPY_PY_MACHINE_SOFTSPI        (1)
#define MICROPY_PY_MACHINE_UART           (1)
#define MICROPY_PY_MACHINE_UART_INCLUDEFILE "ports/k210/machine_uart.c"
#define MICROPY_PY_MACHINE_UART_SENDBREAK (1)
#define MICROPY_PY_MACHINE_EXTRA_GLOBALS \
    { MP_ROM_QSTR(MP_QSTR_Pin), MP_ROM_PTR(&machine_pin_type) }, \
    { MP_ROM_QSTR(MP_QSTR_RTC), MP_ROM_PTR(&machine_rtc_type) },

// The file system: littlefs on the SPI flash, mounted by the frozen _boot.py;
// FAT for SD cards
#define MICROPY_VFS                       (1)
#define MICROPY_FATFS_ENABLE_LFN          (1)
#define MICROPY_FATFS_RPATH               (2)
#define MICROPY_FATFS_MAX_SS              (4096)
#define MICROPY_FATFS_LFN_CODE_PAGE       437
#define MICROPY_READER_VFS                (1)
#define MICROPY_PY_OS                     (1)
#define MICROPY_PY_OS_UNAME               (1)
#define MICROPY_PY_OS_SYNC                (1)

// Type definitions for the specific machine

typedef long mp_off_t;
#define MP_SSIZE_MAX (0x7fffffffffffffffL)

// We need to provide a declaration/definition of alloca()
#include <alloca.h>

#define MICROPY_HW_BOARD_NAME             "Sipeed Maix Amigo"
#define MICROPY_HW_MCU_NAME               "K210"

// The SDK gives each core a 32 KB stack (STKSHIFT in crt.S)
#define MICROPY_HW_STACK_SIZE             (32 * 1024)
#define MICROPY_HEAP_SIZE                 (3 * 1024 * 1024)

#define MP_STATE_PORT MP_STATE_VM
