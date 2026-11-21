#include "py/mpconfig.h"
#include "py/obj.h"
#include "shared/runtime/interrupt_char.h"

void mp_hal_init(void);

mp_uint_t mp_hal_ticks_ms(void);
mp_uint_t mp_hal_ticks_us(void);
mp_uint_t mp_hal_ticks_cpu(void);
void mp_hal_delay_ms(mp_uint_t ms);
void mp_hal_delay_us(mp_uint_t us);

// The time of day, in seconds since the epoch (1970)
void mp_hal_time_set(uint64_t seconds);

// Pins: the K210's IO0 to IO47, by number. Pin routes one to a high-speed
// GPIO channel through the FPIOA; the I2C, SPI and UART classes route their
// pins to the peripheral's functions.
#define MICROPY_HW_PIN_COUNT (48)
#define mp_hal_pin_obj_t uint32_t
#define mp_hal_pin_name(p) (p)
#define MP_HAL_PIN_FMT "%u"
#define mp_hal_delay_us_fast(us) mp_hal_delay_us(us)
mp_hal_pin_obj_t mp_hal_get_pin_obj(mp_obj_t pin_in);
void mp_hal_pin_input(mp_hal_pin_obj_t pin);
void mp_hal_pin_output(mp_hal_pin_obj_t pin);
void mp_hal_pin_open_drain(mp_hal_pin_obj_t pin);
void mp_hal_pin_od_low(mp_hal_pin_obj_t pin);
void mp_hal_pin_od_high(mp_hal_pin_obj_t pin);
int mp_hal_pin_read(mp_hal_pin_obj_t pin);
void mp_hal_pin_write(mp_hal_pin_obj_t pin, int value);

// The high-speed GPIO channel a pin is routed to, routing it to a free one
// if it has none (for drivers that drive pins as GPIOs themselves)
int machine_pin_gpio_channel(mp_hal_pin_obj_t pin);
// Routes a pin to a peripheral's function, freeing any GPIO channel it held
void machine_pin_set_function(mp_hal_pin_obj_t pin, int function);
// Turns off the pins' interrupts at a soft reset
void machine_pin_deinit(void);
// Turns off the UARTs' interrupts at a soft reset
void machine_uart_deinit_all(void);
// Who set up SPI0 and SPI1 last: machine.SPI, the SD card and the screen
// share them, each setting the controller and its pins up again when another
// has used it since
extern const void *k210_spi_owner[2];

// Full-duplex transfer on SPI0 or SPI1 as set up (src NULL: sends 0xFF;
// dest NULL: drops what comes back)
void k210_spi_transfer(int id, size_t len, const uint8_t *src, uint8_t *dest);
// Stop the timers and free the PWM channels at a soft reset
void machine_timer_deinit_all(void);
void machine_pwm_deinit_all(void);
void machine_i2s_deinit_all(void);
// Turns the camera off at a soft reset
void k210_camera_deinit(void);

// A register of a chip on the internal I2C bus (the power chip's)
int k210_i2c0_read_reg(uint8_t addr, uint8_t reg);
bool k210_i2c0_write_reg(uint8_t addr, uint8_t reg, uint8_t value);
// The screen off, held in reset (its backlight off too)
void k210_lcd_power_off(void);
// Reads why the chip started, at start-up (machine.reset_cause)
void k210_reset_cause_init(void);
// Sleeps with the CPU on the oscillator and PLL0 off (machine.lightsleep)
#define K210_SLEEP_FOREVER (UINT64_MAX)
bool k210_lightsleep(uint64_t ms, bool wake_on_irq);
