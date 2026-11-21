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
	k210_flash.c \
	k210_lcd.c \
	drivers/bus/softspi.c \
	machine_i2c.c \
	machine_pin.c \
	machine_rtc.c \
	machine_spi.c \
	main.c \
	modk210.c \
	mphalport.c \
	shared/timeutils/timeutils.c \
	shared/readline/readline.c \
	shared/runtime/gchelper_native.c \
	shared/runtime/interrupt_char.c \
	shared/runtime/pyexec.c \
	shared/runtime/stdout_helpers.c \
	shared/runtime/sys_stdio_mphal.c \

SRC_S = \
	shared/runtime/gchelper_rv64i.s \

SRC_QSTR += \
	k210_lcd.c \
	machine_i2c.c \
	machine_pin.c \
	machine_rtc.c \
	machine_spi.c \
	main.c \
	modk210.c \
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
	clint.c \
	dmac.c \
	fpioa.c \
	gpiohs.c \
	i2c.c \
	iomem.c \
	plic.c \
	spi.c \
	sysctl.c \
	uart.c \
	uarths.c \
	utils.c \
	)

SDK_SRC_S = lib/bsp/crt.S

# iomem.c (the DMA driver's allocator) wants the lock type of older newlibs,
# which the SDK's locks.c defines for itself
$(BUILD)/sdk/lib/drivers/iomem.o: SDK_CFLAGS += -D_lock_t=long

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
