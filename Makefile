
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
ROOT_DIR := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
TARGET = $(notdir $(shell pwd))
TARGET_PATH = $(shell pwd)
TARGET_DIR = executable
LIBRARY = 0


##
## Prefix of the GCC ARM Cross Compiler
##
PREFIX	?= arm-none-eabi

##
## Tools we use for building
##
CC	= $(PREFIX)-gcc
LD	= $(PREFIX)-gcc
ASM     = $(PREFIX)-as
OBJCOPY	= $(PREFIX)-objcopy
OBJDUMP	= $(PREFIX)-objdump
AR	= $(PREFIX)-ar
GDB	= $(PREFIX)-gdb
FLASH	= $(shell which st-flash)
MKDIR   = mkdir
RM      = rm

##
## OpenOCD setup
##
OOCD		?= openocd
OOCD_INTERFACE	?= stlink-v2
OOCD_BOARD	?= stm32f3discovery

##
## Root Paths
##
CMSIS_ROOT_DIR = STM32F3-Discovery_FW_V1.1.0/Libraries/CMSIS
PERIPHERAL_DRIVERS_ROOT_DIR = STM32F3-Discovery_FW_V1.1.0/Libraries/STM32F30x_StdPeriph_Driver


##
## Project Directories
##
SRC_DIR = src
OBJ_DIR = GNU/objects
INC_DIR = includes
EXEC_DIR = GNU/executable
LD_DIR = GNU

##
## The files we are creating
##
ELF_FILE  = $(EXEC_DIR)/$(TARGET).elf
LIST_FILE = $(EXEC_DIR)/$(TARGET).lst
HEX_FILE  = $(EXEC_DIR)/$(TARGET).hex
SREC_FILE = $(EXEC_DIR)/$(TARGET).srec
BIN_FILE  = $(EXEC_DIR)/$(TARGET).bin

##
## Project sources converted to objects
##
SOURCES     += $(wildcard $(SRC_DIR)/*.c)
SOURCES	    += $(CMSIS_ROOT_DIR)/Device/ST/STM32F30x/Source/Templates/system_stm32f30x.c
SOURCES     += $(wildcard $(PERIPHERAL_DRIVERS_ROOT_DIR)/src/*.c)
SOURCES     += $(wildcard  STM32F3-Discovery_FW_V1.1.0/Utilities/STM32F3_Discovery/*.c)
OBJECTS := $(patsubst %.c, $(OBJ_DIR)/%.o, $(notdir $(SOURCES)))

ASM_SOURCES += GNU/startup_stm32f30x.s
ASM_OBJECTS += $(patsubst %.s, $(OBJ_DIR)/%.o, $(notdir $(ASM_SOURCES)))

SOURCES += $(ASM_SOURCES)
OBJECTS += $(ASM_OBJECTS)

ASMFLAGS += -mcpu=cortex-m4 -mthumb -warn --fatal-warnings

VPATH := $(sort  $(dir $(SOURCES)))
##
## Directories to make
##
MAKE_DIRS = $(OBJ_DIR) $(EXEC_DIR)


##
## Include paths
##
PERIPHERAL_DRIVERS_INC_DIR = $(PERIPHERAL_DRIVERS_ROOT_DIR)/inc
PERIPHERAL_UTILITY_INC_DIR = STM32F3-Discovery_FW_V1.1.0/Utilities/STM32F3_Discovery/
CMSIS_ARM_INC_DIR = $(CMSIS_ROOT_DIR)/Include
CMSIS_DEVICE_INC_DIR = $(CMSIS_ROOT_DIR)/Device/ST/STM32F30x/Include

CINCLUDES += -I$(INC_DIR) -I$(PERIPHERAL_DRIVERS_INC_DIR) -I$(CMSIS_ARM_INC_DIR) -I $(CMSIS_DEVICE_INC_DIR) -I$(PERIPHERAL_UTILITY_INC_DIR)

##
## Options passed to the C compiler
##
CFLAGS += -DUSE_STDPERIPH_DRIVER
CFLAGS	+= -Os -g -Wall -Wextra  $(CINCLUDES)\
	   -fno-common -mcpu=cortex-m4 -mthumb \
	   -mfloat-abi=hard -mfpu=fpv4-sp-d16 -MD -DSTM32F3

LDSCRIPT = $(LD_DIR)/stm32f3.ld
LDFLAGS		+= --static -lc -T$(LDSCRIPT) -nostartfiles -Wl,--gc-sections \
		   -mthumb -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16

TAG_FILES += $(SOURCES)
TAG_FILES += $(INC_DIR)/*.h
TAG_FILES += $(PERIPHERAL_DRIVERS_INC_DIR)/*.h
TAG_FILES += $(CMSIS_ARM_INC_DIR)/*.h
TAG_FILES += $(CMSIS_DEVICE_INC_DIR)/*.h
TAG_FILES += $(PERIPHERAL_UTILITY_INC_DIR)/*.h

##
## The list of steps to build the image
##
BUILD_LIST += dirs TAGS $(ELF_FILE) 



all: $(BUILD_LIST)  $(BIN_FILE)

dirs:
	@echo "Making Dirs $(MAKE_DIRS)"
	@$(MKDIR) -p $(MAKE_DIRS)

TAGS:
	@echo "Making TAG File"
	@etags $(TAG_FILES)

$(ELF_FILE):$(OBJECTS)	
	@echo "Linking $(ELF_FILE)"
	@$(LD) -o $(ELF_FILE) $(OBJECTS) $(LDFLAGS)

$(BIN_FILE):$(ELF_FILE)
	@echo "Creating $(BIN_FILE)"
	@$(OBJCOPY) -Obinary $(ELF_FILE) $(BIN_FILE)

program: dirs $(BIN_FILE)
	$(FLASH) --reset write $(BIN_FILE) 0x8000000

debug: $(ELF_FILE)
	$(GDB) --tui -x ../GNU/gdb_cmds $(ELF_FILE)


##
## Turn out C code into objects in our $(OBJ_DIR)
##
$(OBJ_DIR)/%.o:%.c
	@echo "Compiling  $<"
	@$(CC) $(CFLAGS) -o $@ -c $< 

##
## Turn our S code into objects in our $(OBJ_DIR)
##
$(OBJ_DIR)/%.o:%.s
	@echo "Assembling $<"
	@$(CC) $(CFLAGS) -o $@ -c $< 

clean:
	rm -rf $(OBJ_DIR) $(EXEC_DIR) TAGS
	find . -name "*~" | xargs rm -f
