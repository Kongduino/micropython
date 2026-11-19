#include <stdint.h>

// Options to control how MicroPython is built for the K210

#define MICROPY_CONFIG_ROM_LEVEL          (MICROPY_CONFIG_ROM_LEVEL_BASIC_FEATURES)

#define MICROPY_ENABLE_COMPILER           (1)
#define MICROPY_ENABLE_GC                 (1)
#define MICROPY_ENABLE_FINALISER          (1)
#define MICROPY_GCREGS_SETJMP             (0)
#define MICROPY_HELPER_REPL               (1)
#define MICROPY_REPL_AUTO_INDENT          (1)
#define MICROPY_KBD_EXCEPTION             (1)
#define MICROPY_LONGINT_IMPL              (MICROPY_LONGINT_IMPL_MPZ)
#define MICROPY_FLOAT_IMPL                (MICROPY_FLOAT_IMPL_FLOAT)
#define MICROPY_ALLOC_PATH_MAX            (256)
#define MICROPY_STACK_CHECK               (1)

#define MICROPY_PY_SYS_STDFILES           (1)
#define MICROPY_PY_SYS_PLATFORM           "k210"
#define MICROPY_PY_TIME                   (1)
#define MICROPY_PY_TIME_GMTIME_LOCALTIME_MKTIME (0)
#define MICROPY_PY_TIME_TIME_TIME_NS      (0)

// The file system: littlefs on the SPI flash, mounted by the frozen _boot.py
#define MICROPY_VFS                       (1)
#define MICROPY_READER_VFS                (1)
#define MICROPY_PY_OS                     (1)
#define MICROPY_PY_OS_UNAME               (1)
#define MICROPY_PY_OS_SYNC                (1)

// Type definitions for the specific machine

typedef long mp_off_t;

// We need to provide a declaration/definition of alloca()
#include <alloca.h>

#define MICROPY_HW_BOARD_NAME             "Sipeed Maix Amigo"
#define MICROPY_HW_MCU_NAME               "K210"

// The SDK gives each core a 32 KB stack (STKSHIFT in crt.S)
#define MICROPY_HW_STACK_SIZE             (32 * 1024)
#define MICROPY_HEAP_SIZE                 (2 * 1024 * 1024)

#define MP_STATE_PORT MP_STATE_VM
