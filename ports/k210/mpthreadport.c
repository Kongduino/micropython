// _thread's port side: the second thread runs on core 1 (see mpthreadport.h).
//
// The SDK's start-up code parks core 1 until register_core1(), which can be
// called once, and exits if the function it starts returns. So core 1 is
// started once, at the first thread, into a loop of its own: wait for a
// thread (woken by a software interrupt), run it, wait again. It runs on the
// stack the start-up code gave it (the 32 KB below _sp1).
//
// At a soft reset, a thread still running is dropped: a software interrupt
// with the stop flag set sends core 1 from its interrupt handler back to its
// loop, on a fresh stack, before the heap the thread used is set up anew.

#include "py/runtime.h"
#include "py/gc.h"
#include "py/mphal.h"
#include "py/mpthread.h"

#include "clint.h"
#include "entry.h"

#if MICROPY_PY_THREAD

#define CORE1_STACK_SIZE (32 * 1024)
#define STOP_TIMEOUT_MS (100)

// The start-up code's stacks: core 0's from _tp0 to _sp0, core 1's from _tp1
// to _sp1
extern char _tp0[], _sp0[], _tp1[], _sp1[];

void *k210_core_state[2];

// The thread core 1 runs, and its argument: core1_entry is non-NULL while one
// runs (or is about to)
static void *(*volatile core1_entry)(void *);
static void *volatile core1_arg;
static bool core1_started;
static volatile bool core1_stop;

// The atomic sections' lock between the cores, taken (with interrupts off)
// only while core 1 runs a thread; it nests on a core
static mp_thread_recursive_mutex_t atomic_mutex;

uint32_t mp_thread_begin_atomic_section(void) {
    uint32_t state = read_csr(mstatus) & MSTATUS_MIE;
    clear_csr(mstatus, MSTATUS_MIE);
    if (core1_entry != NULL || atomic_mutex.owner) {
        mp_thread_recursive_mutex_lock(&atomic_mutex, 1);
    }
    return state;
}

void mp_thread_end_atomic_section(uint32_t state) {
    if (atomic_mutex.owner == (int)current_coreid() + 1) {
        mp_thread_recursive_mutex_unlock(&atomic_mutex);
    }
    set_csr(mstatus, state);
}

void mp_thread_init(void) {
    mp_thread_recursive_mutex_init(&atomic_mutex);
    mp_thread_set_state(&mp_state_ctx.thread);
}

// The other core's stack, all of it (its registers aren't seen: as on rp2)
void mp_thread_gc_others(void) {
    if (current_coreid() == 0) {
        if (core1_entry != NULL) {
            gc_collect_root((void **)_tp1, (_sp1 - _tp1) / sizeof(void *));
            gc_collect_root((void **)&core1_arg, 1);
        }
    } else {
        gc_collect_root((void **)_tp0, (_sp0 - _tp0) / sizeof(void *));
    }
}

static void core1_stopped(void);

// The software interrupt, on core 1: a stop drops the thread, going back to
// the loop on a fresh stack (never returning to the interrupted code)
static int core1_ipi(void *ctx) {
    if (core1_stop) {
        clear_csr(mstatus, MSTATUS_MIE);
        asm volatile (
            "mv sp, %0\n"
            "jr %1\n"
            : : "r" (_sp1), "r" (core1_stopped));
    }
    return 0;
}

static void core1_wait(void) {
    // A software interrupt wakes it from wfi; nothing else is enabled on
    // core 1 (the PLIC's interrupts go to core 0). The check and the wfi are
    // made with interrupts off, so that one coming in between still wakes it
    // (wfi ends on a pending interrupt even so), then taken.
    write_csr(mie, MIP_MSIP);
    for (;;) {
        clear_csr(mstatus, MSTATUS_MIE);
        if (core1_entry == NULL) {
            asm volatile ("wfi");
        }
        set_csr(mstatus, MSTATUS_MIE);
        void *(*entry)(void *) = __atomic_load_n(&core1_entry, __ATOMIC_ACQUIRE);
        if (entry != NULL) {
            entry(core1_arg);
            core1_entry = NULL;
        }
    }
}

// Back from a dropped thread
static void core1_stopped(void) {
    core1_stop = false;
    __atomic_store_n(&core1_entry, NULL, __ATOMIC_RELEASE);
    core1_wait();
}

static int core1_main(void *ctx) {
    clint_ipi_register(core1_ipi, NULL);
    core1_wait();
    return 0;
}

mp_uint_t mp_thread_get_id(void) {
    return current_coreid() + 1;
}

mp_uint_t mp_thread_create(void *(*entry)(void *), void *arg, size_t *stack_size) {
    if (core1_entry != NULL) {
        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("core1 in use"));
    }
    // Its stack is the start-up code's, whatever size is asked for; room is
    // left to recover from hitting the limit
    *stack_size = CORE1_STACK_SIZE - 1024;
    core1_arg = arg;
    __atomic_store_n(&core1_entry, entry, __ATOMIC_RELEASE);
    if (!core1_started) {
        core1_started = true;
        register_core1(core1_main, NULL);
    } else {
        clint_ipi_send(1);
    }
    return 2;
}

void mp_thread_start(void) {
}

void mp_thread_finish(void) {
}

// At a soft reset: a thread still running is dropped. The GC's lock is
// taken first, so that the thread isn't dropped holding it (the sweep that
// follows would wait for it for ever).
void mp_thread_deinit(void) {
    if (core1_entry == NULL) {
        return;
    }
    mp_thread_recursive_mutex_lock(&MP_STATE_MEM(gc_mutex), 1);
    core1_stop = true;
    __atomic_thread_fence(__ATOMIC_SEQ_CST);
    clint_ipi_send(1);
    mp_uint_t start = mp_hal_ticks_ms();
    while (core1_entry != NULL && mp_hal_ticks_ms() - start < STOP_TIMEOUT_MS) {
    }
    mp_thread_recursive_mutex_unlock(&MP_STATE_MEM(gc_mutex));
}

#endif // MICROPY_PY_THREAD
