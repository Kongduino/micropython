// The port's part of the time module, included by extmod/modtime.c

#include "py/mphal.h"
#include "shared/timeutils/timeutils.h"

static void mp_time_localtime_get(timeutils_struct_time_t *tm) {
    timeutils_seconds_since_epoch_to_struct_time(mp_hal_time_ns() / 1000000000, tm);
}

static mp_obj_t mp_time_time_get(void) {
    return mp_obj_new_int_from_ull(mp_hal_time_ns() / 1000000000);
}
