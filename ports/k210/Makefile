# MicroPython port for the Kendryte K210 (Sipeed Maix Amigo), on the bare
# Kendryte standalone SDK.

include ../../py/mkenv.mk

# The Kendryte standalone SDK (https://github.com/kendryte/kendryte-standalone-sdk)
K210_SDK ?= $(abspath $(TOP)/../kendryte-standalone-sdk)

CROSS_COMPILE ?= riscv-none-elf-

# Serial port and baud rate for `make deploy` (kflash)
PORT ?= /dev/cu.usbserial-2101
BAUD ?= 2000000
KFLASH ?= $(HOME)/.platformio/packages/tool-kflash-kendryte210/kflash.py

QSTR_DEFS = qstrdefsport.h

MICROPY_ROM_TEXT_COMPRESSION ?= 1
MICROPY_VFS_LFS2 ?= 1
MICROPY_VFS_FAT ?= 1

FROZEN_MANIFEST ?= $(abspath manifest.py)

include $(TOP)/py/py.mk
include $(TOP)/extmod/extmod.mk

# The SDK's flags (cmake/compile-flags.cmake), with the extensions GCC 12 and
# later want named
ARCH_FLAGS = -march=rv64imafc_zicsr_zifencei -mabi=lp64f -mcmodel=medany
AFLAGS = -march=rv64imafc_zicsr_zifencei -mabi=lp64f

# The SDK's definitions (cmake/common.cmake), logging only errors
SDK_DEFS = -DCONFIG_LOG_LEVEL=LOG_ERROR -DCONFIG_LOG_ENABLE -DLOG_KERNEL -D__riscv64

SDK_INC = \
	-I$(K210_SDK)/lib/bsp/include \
	-I$(K210_SDK)/lib/drivers/include \
	-I$(K210_SDK)/lib/utils/include \

INC += -I.
INC += -I$(TOP)
INC += -I$(BUILD)
INC += $(SDK_INC)

CFLAGS += $(SDK_DEFS)

# cryptolib's AES is axTLS's aes.c, built on its own (extmod.mk builds axTLS
# only for the ssl module, which this port leaves out)
CFLAGS += -DMICROPY_SSL_AXTLS=1 -Iaxtls-include -I$(TOP)/lib/axtls/ssl -I$(TOP)/lib/axtls/crypto -I$(TOP)/extmod/axtls-include
GIT_SUBMODULES += lib/axtls
$(BUILD)/lib/axtls/%.o: CFLAGS += -Wno-all -Wno-unused-parameter -Wno-sign-compare

# qr's decoder, quirc, in single precision (the FPU's), with its own code
# style's warnings
QUIRC_CFLAGS = -DQUIRC_FLOAT_TYPE=float -DQUIRC_USE_TGMATH
CFLAGS += $(QUIRC_CFLAGS)
$(BUILD)/quirc/%.o: CFLAGS += -Wno-all -Wno-sign-compare -Wno-double-promotion

CFLAGS += $(INC) $(ARCH_FLAGS) -Wall -Werror -std=gnu11 -nostdlib $(COPT)
CFLAGS += -fno-common -ffunction-sections -fdata-sections -fstrict-volatile-bitfields
CFLAGS += -fsingle-precision-constant -Wdouble-promotion
CFLAGS += -g

CSUPEROPT = -O2

ifeq ($(DEBUG), 1)
COPT = -O0
else
COPT = -Os -DNDEBUG
endif

# The SDK is built with its own, looser warnings, as its CMake build does;
# GCC 14 made some of what it does errors.
SDK_CFLAGS = $(SDK_INC) $(SDK_DEFS) $(ARCH_FLAGS) -std=gnu11 -Os -g \
	-fno-common -ffunction-sections -fdata-sections -fstrict-volatile-bitfields \
	-fno-zero-initialized-in-bss -ffast-math -fno-math-errno -fsingle-precision-constant \
	-w -Wno-error=incompatible-pointer-types -Wno-error=implicit-function-declaration \
	-Wno-error=int-conversion

LDFLAGS += -nostartfiles -static -Wl,--gc-sections -Wl,--no-relax -Wl,-EL -Wl,--no-warn-rwx-segments
LDFLAGS += -T $(K210_SDK)/lds/kendryte.ld -Wl,-Map=$(BUILD)/firmware.map
LIBS = -Wl,--start-group -lc -lm -lgcc -Wl,--end-group

SRC_C = \
	k210_aes.c \
	k210_camera.c \
	k210_flash.c \
	k210_lcd.c \
	k210_sdcard.c \
	k210_sha256.c \
	drivers/bus/softspi.c \
	machine_i2c.c \
	machine_pin.c \
	machine_rtc.c \
	machine_spi.c \
	machine_timer.c \
	main.c \
	modk210.c \
	modqr.c \
	mphalport.c \
	mpthreadport.c \
	quirc/decode.c \
	quirc/identify.c \
	quirc/quirc.c \
	quirc/version_db.c \
	shared/timeutils/timeutils.c \
	lib/axtls/crypto/aes.c \
	shared/readline/readline.c \
	shared/runtime/gchelper_native.c \
	shared/runtime/interrupt_char.c \
	shared/runtime/pyexec.c \
	shared/runtime/stdout_helpers.c \
	shared/runtime/sys_stdio_mphal.c \

SRC_S = \
	shared/runtime/gchelper_rv64i.s \

SRC_QSTR += \
	k210_camera.c \
	machine_timer.c \
	k210_sha256.c \
	k210_aes.c \
	k210_lcd.c \
	k210_sdcard.c \
	machine_i2c.c \
	machine_pin.c \
	machine_rtc.c \
	machine_spi.c \
	main.c \
	modk210.c \
	modqr.c \
	shared/readline/readline.c \
	shared/runtime/pyexec.c \
	shared/runtime/sys_stdio_mphal.c \

SDK_SRC_C = $(addprefix lib/bsp/, \
	entry.c \
	entry_user.c \
	interrupt.c \
	locks.c \
	printf.c \
	sleep.c \
	syscalls.c \
	) $(addprefix lib/drivers/, \
	aes.c \
	clint.c \
	dmac.c \
	dvp.c \
	fpioa.c \
	gpiohs.c \
	i2s.c \
	i2c.c \
	iomem.c \
	plic.c \
	pwm.c \
	sha256.c \
	spi.c \
	sysctl.c \
	timer.c \
	uart.c \
	uarths.c \
	utils.c \
	)

SDK_SRC_S = lib/bsp/crt.S

# iomem.c (the DMA driver's allocator) wants the lock type of older newlibs,
# which the SDK's locks.c defines for itself
$(BUILD)/sdk/lib/drivers/iomem.o: SDK_CFLAGS += -D_lock_t=long

# The SDK's hash driver and MicroPython's software SHA-256 (in the port's
# hashlib, k210_sha256.c) both define sha256_init/update/final: the SDK's are
# renamed
SHA256_RENAME = -Dsha256_init=k210_sha256_init -Dsha256_update=k210_sha256_update -Dsha256_final=k210_sha256_final
$(BUILD)/sdk/lib/drivers/sha256.o: SDK_CFLAGS += $(SHA256_RENAME)

OBJ += $(PY_O)
OBJ += $(addprefix $(BUILD)/, $(SRC_C:.c=.o))
OBJ += $(addprefix $(BUILD)/, $(SRC_S:.s=.o))
SDK_OBJ = $(addprefix $(BUILD)/sdk/, $(SDK_SRC_C:.c=.o) $(SDK_SRC_S:.S=.o))
OBJ += $(SDK_OBJ)

all: $(BUILD)/firmware.bin

$(BUILD)/sdk/%.o: $(K210_SDK)/%.c
	$(ECHO) "CC $<"
	$(Q)$(MKDIR) -p $(dir $@)
	$(Q)$(CC) $(SDK_CFLAGS) -c -o $@ $<

$(BUILD)/sdk/%.o: $(K210_SDK)/%.S
	$(ECHO) "AS $<"
	$(Q)$(MKDIR) -p $(dir $@)
	$(Q)$(CC) $(SDK_CFLAGS) -c -o $@ $<

$(BUILD)/firmware.elf: $(OBJ)
	$(ECHO) "LINK $@"
	$(Q)$(CC) $(ARCH_FLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)
	$(Q)$(SIZE) $@

$(BUILD)/firmware.bin: $(BUILD)/firmware.elf
	$(Q)$(OBJCOPY) -O binary $< $@

deploy: $(BUILD)/firmware.bin
	$(ECHO) "Writing $< to the board"
	$(Q)$(PYTHON) $(KFLASH) -p $(PORT) -b $(BAUD) -B goE $<

include $(TOP)/py/mkrules.mk
