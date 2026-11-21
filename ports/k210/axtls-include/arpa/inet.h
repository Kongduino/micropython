// The byte-order functions axTLS takes from <arpa/inet.h>, which a bare-metal
// toolchain doesn't have. The K210 is little-endian.
#ifndef MICROPY_INCLUDED_K210_ARPA_INET_H
#define MICROPY_INCLUDED_K210_ARPA_INET_H

#include <stdint.h>

static inline uint32_t htonl(uint32_t x) {
    return __builtin_bswap32(x);
}

static inline uint32_t ntohl(uint32_t x) {
    return __builtin_bswap32(x);
}

static inline uint16_t htons(uint16_t x) {
    return __builtin_bswap16(x);
}

static inline uint16_t ntohs(uint16_t x) {
    return __builtin_bswap16(x);
}

#endif // MICROPY_INCLUDED_K210_ARPA_INET_H
