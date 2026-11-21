#include "py/mphal.h"
#include "py/runtime.h"
#include "py/stream.h"
#include "shared/timeutils/timeutils.h"
#include "lib/oofatfs/ff.h"

#include "clint.h"
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

// Light sleep: the CPU (and the buses, which run from its clock) on the
// 26 MHz oscillator, PLL0 powered down, waiting for an interrupt. PLL1 (the
// KPU's, which also clocks the top 2 MB of RAM) and PLL2 run on. The
// high-speed UART's divider is set for each clock, so the REPL (Ctrl-C) works
// asleep too. The cycle counter, which keeps the time, is moved on by the
// time asleep, counted by the CLINT's timer (the CPU clock / 50).
//
// ms is the longest sleep (K210_SLEEP_FOREVER: no limit); an external
// interrupt (a pin, a Timer, the UART...) ends it early if wake_on_irq,
// else only the time does. Returns whether it ended early.
//
// The UART's bit time measures about 10 clock cycles longer than its
// divider gives (found at the oscillator: it receives without error from 209
// to 221, where freq / 115200 - 1 is 224), nothing at 400 MHz but 4% at
// 26 MHz, so the divider is set with that taken off.
static void uarths_set_div(void) {
    uarths->div.div = sysctl_clock_get_freq(SYSCTL_CLOCK_CPU) / 115200 - 11;
}

bool k210_lightsleep(uint64_t ms, bool wake_on_irq) {
    // Let the UART send what it has at the old rate (its FIFO holds 8 bytes)
    mp_hal_delay_us(1000);
    uint64_t cycles = read_csr(mcycle);
    clear_csr(mstatus, MSTATUS_MIE);
    uintptr_t mie = read_csr(mie);

    sysctl_clock_set_clock_select(SYSCTL_CLOCK_SELECT_ACLK, SYSCTL_SOURCE_IN0);
    sysctl->pll0.pll_out_en0 = 0;
    sysctl->pll0.pll_pwrd0 = 0;
    uarths_set_div();

    uint64_t rate = sysctl_clock_get_freq(SYSCTL_CLOCK_CPU) / CLINT_CLOCK_DIV;
    uint64_t start = clint->mtime;
    uint64_t end = ms == K210_SLEEP_FOREVER ? UINT64_MAX : start + ms * rate / 1000;
    clint->mtimecmp[0] = end;
    write_csr(mie, (wake_on_irq ? (mie & MIP_MEIP) : 0) | MIP_MTIP);
    bool early = false;
    while (clint->mtime < end) {
        if (read_csr(mip) & MIP_MEIP & read_csr(mie)) {
            early = true;
            break;
        }
        asm volatile ("wfi");
    }
    clint->mtimecmp[0] = UINT64_MAX;

    write_csr(mie, mie);

    // PLL0 back on, as sysctl_pll_set_freq() starts it, at the frequency it
    // was set to
    sysctl->pll0.pll_pwrd0 = 1;
    mp_hal_delay_us(1);
    sysctl->pll0.pll_reset0 = 0;
    sysctl->pll0.pll_reset0 = 1;
    mp_hal_delay_us(1);
    sysctl->pll0.pll_reset0 = 0;
    while (sysctl->pll_lock.pll_lock0 != 3) {
        sysctl->pll_lock.pll_slip_clear0 = 1;
    }
    sysctl->pll0.pll_out_en0 = 1;
    uint64_t asleep = clint->mtime - start;
    sysctl_clock_set_clock_select(SYSCTL_CLOCK_SELECT_ACLK, SYSCTL_SOURCE_PLL0);
    uarths_set_div();
    write_csr(mcycle, cycles + asleep * 1000000 / rate * cycles_per_us);
    set_csr(mstatus, MSTATUS_MIE);
    return early;
}

// FAT's timestamps, packed as FatFs wants them
DWORD get_fattime(void) {
    timeutils_struct_time_t tm;
    timeutils_seconds_since_epoch_to_struct_time(mp_hal_time_ns() / 1000000000, &tm);
    return ((tm.tm_year - 1980) << 25) | (tm.tm_mon << 21) | (tm.tm_mday << 16)
           | (tm.tm_hour << 11) | (tm.tm_min << 5) | (tm.tm_sec / 2);
}
