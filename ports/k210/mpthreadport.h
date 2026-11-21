// _thread on the K210's second core: one thread besides the main one, which
// runs on core 0, each on a core of its own and at the same time (no GIL),
// as rp2 has it. Locks are spinlocks on the A extension's atomics: the two
// threads are never on the same core, so a thread waiting for one only waits
// for the other core.
#ifndef MICROPY_INCLUDED_K210_MPTHREADPORT_H
#define MICROPY_INCLUDED_K210_MPTHREADPORT_H

#include <stdint.h>

#include "encoding.h"

typedef struct _mp_thread_mutex_t {
    volatile int locked;
} mp_thread_mutex_t;

typedef struct _mp_thread_recursive_mutex_t {
    mp_thread_mutex_t mutex;
    volatile int owner; // the core holding it, plus 1; 0 if none
    int count;
} mp_thread_recursive_mutex_t;

extern void *k210_core_state[2];

void mp_thread_init(void);
void mp_thread_deinit(void);
void mp_thread_gc_others(void);
uint32_t mp_thread_begin_atomic_section(void);
void mp_thread_end_atomic_section(uint32_t state);

static inline void mp_thread_set_state(struct _mp_state_thread_t *state) {
    k210_core_state[current_coreid()] = state;
}

static inline struct _mp_state_thread_t *mp_thread_get_state(void) {
    return (struct _mp_state_thread_t *)k210_core_state[current_coreid()];
}

static inline void mp_thread_mutex_init(mp_thread_mutex_t *m) {
    __atomic_store_n(&m->locked, 0, __ATOMIC_RELEASE);
}

static inline int mp_thread_mutex_lock(mp_thread_mutex_t *m, int wait) {
    while (__atomic_exchange_n(&m->locked, 1, __ATOMIC_ACQUIRE)) {
        if (!wait) {
            return 0;
        }
    }
    return 1;
}

static inline void mp_thread_mutex_unlock(mp_thread_mutex_t *m) {
    __atomic_store_n(&m->locked, 0, __ATOMIC_RELEASE);
}

static inline void mp_thread_recursive_mutex_init(mp_thread_recursive_mutex_t *m) {
    mp_thread_mutex_init(&m->mutex);
    m->owner = 0;
    m->count = 0;
}

static inline int mp_thread_recursive_mutex_lock(mp_thread_recursive_mutex_t *m, int wait) {
    int me = current_coreid() + 1;
    if (m->owner == me) {
        m->count++;
        return 1;
    }
    if (!mp_thread_mutex_lock(&m->mutex, wait)) {
        return 0;
    }
    m->owner = me;
    m->count = 1;
    return 1;
}

static inline void mp_thread_recursive_mutex_unlock(mp_thread_recursive_mutex_t *m) {
    if (--m->count == 0) {
        m->owner = 0;
        mp_thread_mutex_unlock(&m->mutex);
    }
}

#endif // MICROPY_INCLUDED_K210_MPTHREADPORT_H
