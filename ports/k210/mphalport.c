#include "py/mphal.h"
#include "py/runtime.h"
#include "py/stream.h"
#include "shared/timeutils/timeutils.h"
#include "lib/oofatfs/ff.h"

#include "encoding.h"
#include "fpioa.h"
#include "plic.h"
#include "syscalls.h"
#include "sysctl.h"
#include "uarths.h"

// The USB serial port (the FT2232's second channel) is wired to IO4 (RX) and
// IO5 (TX), routed to the K210's high-speed UART. Its receive FIFO holds only
// 8 bytes, so an interrupt moves each byte into a ring buffer: a pasted script
// or mpremote's raw REPL arrives faster than the REPL reads it.
#define STDIN_PIN_RX 4
#define STDIN_PIN_TX 5
#define STDIN_BUF_SIZE 4096 // a power of two

static uint8_t stdin_buf[STDIN_BUF_SIZE];
static volatile uint32_t stdin_head; // written by the interrupt
static volatile uint32_t stdin_tail; // written by mp_hal_stdin_rx_chr

static uint64_t cycles_per_us;

static int stdin_irq(void *ctx) {
    (void)ctx;
    int c;
    while ((c = uarths_getchar()) != EOF) {
        if (c == mp_interrupt_char) {
            mp_sched_keyboard_interrupt();
            continue;
        }
        uint32_t next = (stdin_head + 1) & (STDIN_BUF_SIZE - 1);
        if (next != stdin_tail) {
            stdin_buf[stdin_head] = c;
            stdin_head = next;
        }
    }
    return 0;
}

static int stdout_putchar(char c) {
    return uarths_putchar(c);
}

void mp_hal_init(void) {
    cycles_per_us = sysctl_clock_get_freq(SYSCTL_CLOCK_CPU) / 1000000;

    // The SDK's start-up code put the SDK's console on UART3 on these pins
    fpioa_set_function(STDIN_PIN_RX, FUNC_UARTHS_RX);
    fpioa_set_function(STDIN_PIN_TX, FUNC_UARTHS_TX);
    uarths_init();
    uarths_set_irq(UARTHS_RECEIVE, stdin_irq, NULL, 1);
    // The SDK's own messages (trap dumps, its logging) go to the same port
    sys_register_putchar(stdout_putchar);
}

uintptr_t mp_hal_stdio_poll(uintptr_t poll_flags) {
    uintptr_t ret = 0;
    if ((poll_flags & MP_STREAM_POLL_RD) && stdin_tail != stdin_head) {
        ret |= MP_STREAM_POLL_RD;
    }
    if (poll_flags & MP_STREAM_POLL_WR) {
        ret |= MP_STREAM_POLL_WR;
    }
    return ret;
}

int mp_hal_stdin_rx_chr(void) {
    for (;;) {
        // Sleep until a byte arrives. Interrupts are masked between the check
        // and the wfi, so one arriving in between still wakes the core.
        clear_csr(mstatus, MSTATUS_MIE);
        if (stdin_tail != stdin_head) {
            set_csr(mstatus, MSTATUS_MIE);
            break;
        }
        asm volatile ("wfi");
        set_csr(mstatus, MSTATUS_MIE);
        mp_handle_pending(true);
    }
    int c = stdin_buf[stdin_tail];
    stdin_tail = (stdin_tail + 1) & (STDIN_BUF_SIZE - 1);
    return c;
}

mp_uint_t mp_hal_stdout_tx_strn(const char *str, size_t len) {
    for (size_t i = 0; i < len; i++) {
        uarths_putchar(str[i]);
    }
    return len;
}

mp_uint_t mp_hal_ticks_cpu(void) {
    return read_csr(mcycle);
}

mp_uint_t mp_hal_ticks_us(void) {
    return read_csr(mcycle) / cycles_per_us;
}

mp_uint_t mp_hal_ticks_ms(void) {
    return read_csr(mcycle) / (cycles_per_us * 1000);
}

// The K210's RTC loses its time at every reset, like a clock kept from the
// cycle counter: the time of day is the counter plus an offset that
// machine.RTC().datetime() sets (Thonny sets it on connecting). Until then it
// counts from the epoch.
static int64_t time_offset_us;

uint64_t mp_hal_time_ns(void) {
    return ((int64_t)mp_hal_ticks_us() + time_offset_us) * 1000;
}

void mp_hal_time_set(uint64_t seconds) {
    time_offset_us = (int64_t)seconds * 1000000 - (int64_t)mp_hal_ticks_us();
}

void mp_hal_delay_us(mp_uint_t us) {
    uint64_t start = read_csr(mcycle);
    uint64_t wait = (uint64_t)us * cycles_per_us;
    while (read_csr(mcycle) - start < wait) {
    }
}

void mp_hal_delay_ms(mp_uint_t ms) {
    mp_uint_t start = mp_hal_ticks_ms();
    while (mp_hal_ticks_ms() - start < ms) {
        mp_handle_pending(true);
    }
}

// FAT's timestamps, packed as FatFs wants them
DWORD get_fattime(void) {
    timeutils_struct_time_t tm;
    timeutils_seconds_since_epoch_to_struct_time(mp_hal_time_ns() / 1000000000, &tm);
    return ((tm.tm_year - 1980) << 25) | (tm.tm_mon << 21) | (tm.tm_mday << 16)
           | (tm.tm_hour << 11) | (tm.tm_min << 5) | (tm.tm_sec / 2);
}
