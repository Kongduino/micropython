#include "py/mphal.h"
#include "py/runtime.h"
#include "py/stream.h"

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
