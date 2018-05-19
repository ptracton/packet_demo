##
## Per Project Configuration
##
TARGET = packet_demo
CMSIS = 1
HAL = 1


##
## Prefix of the GCC ARM Cross Compiler
##
ARM_GCC_LOCATION = /opt/Atollic/TrueStudio_9.0.0/ARMTools/bin
PREFIX	= $(ARM_GCC_LOCATION)/arm-atollic-eabi


##
## Tools we use for building
##
CC	= $(PREFIX)-gcc
LD	= $(PREFIX)-gcc
ASM     = $(PREFIX)-as
OBJCOPY	= $(PREFIX)-objcopy
OBJDUMP	= $(PREFIX)-objdump
AR     	= $(PREFIX)-ar
GDB	= $(PREFIX)-gdb
FLASH	= $(shell which st-flash)
MKDIR   = mkdir
RM      = rm


##
## Project Directories
##
SRC_DIR  = Src
OBJ_DIR  = objects
INC_DIR  = Inc
EXEC_DIR = Debug
DEP_DIR  = dep
LD_DIR   = .


##
## The files we are creating
##
ELF_FILE  = $(EXEC_DIR)/$(TARGET).elf
LIST_FILE = $(EXEC_DIR)/$(TARGET).lst
HEX_FILE  = $(EXEC_DIR)/$(TARGET).hex
SREC_FILE = $(EXEC_DIR)/$(TARGET).srec
BIN_FILE  = $(EXEC_DIR)/$(TARGET).bin

##
## Start up file
##
ASM_SOURCES      += startup/startup_stm32l475xx.s
ASM_OBJECTS      += $(OBJ_DIR)/startup_stm32l475xx.o
ELF_REQUIREMENTS += $(ASM_OBJECTS)
VPATH            += startup
ASMFLAGS         += -mcpu=cortex-m4 -mthumb -warn --fatal-warnings

##
## Project sources converted to objects
##
SOURCES          += $(wildcard $(SRC_DIR)/*.c)
OBJECTS          += $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SOURCES))
DEPS              = $(addprefix $(DEP_DIR),$(SOURCES:.c=.d))
CINCLUDES        += -I$(INC_DIR)
VPATH            += $(SRC_DIR)
ELF_REQUIREMENTS += $(OBJECTS) 
LDSCRIPT          =$(LD_DIR)/STM32L475VG_FLASH.ld
TAG_FILES        += $(SRC_DIR)/*.c $(INC_DIR)/*.h

##
## The path to the L4 Cube Generate code
##
STM32L4_CUBE_ROOT_DIR = ${CURDIR}/

##
## HAL Drivers
##
ifeq ($(HAL),1)
HAL_ROOT_DIR      = $(STM32L4_CUBE_ROOT_DIR)Drivers/STM32L4xx_HAL_Driver
HAL_SRC_DIR       = $(HAL_ROOT_DIR)/Src
HAL_INC_DIR       = $(HAL_ROOT_DIR)/Inc
HAL_SOURCES      += $(wildcard $(HAL_SRC_DIR)/*.c)
HAL_SOURCES_FIX  := $(filter-out $(HAL_SRC_DIR)/stm32l4xx_hal_msp_template.c,$(HAL_SOURCES))
HAL_OBJECTS      += $(patsubst $(HAL_SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(HAL_SOURCES_FIX))
VPATH            += $(HAL_SRC_DIR)
CINCLUDES        += -I$(HAL_INC_DIR)
ELF_REQUIREMENTS += $(HAL_OBJECTS)
TAG_FILES        += $(HAL_SRC_DIR)/*.c $(HAL_INC_DIR)/*.h
endif

##
## CMSIS Drivers
##
ifeq ($(CMSIS),1)
CMSIS_ROOT_DIR    = $(STM32L4_CUBE_ROOT_DIR)Drivers/CMSIS/Device/ST/STM32L4xx
CMSIS_INC_DIR     = $(CMSIS_ROOT_DIR)/Include
CINCLUDES        += -I$(CMSIS_INC_DIR)
CINCLUDES        += -I$(STM32L4_CUBE_ROOT_DIR)Drivers/CMSIS/Include
TAG_FILES        += $(CMSIS_INC_DIR)/*.h
endif



##
## Options passed to the C compiler
##
CFLAGS  += -DSTM32L475xx
CFLAGS  += -DUSE_HAL_DRIVER
CFLAGS	+= -Os -g  $(CINCLUDES)\
	   -fno-common -mcpu=cortex-m4 -mthumb \
	   -mfloat-abi=hard -mfpu=fpv4-sp-d16 -MD -DSTM32L4

##
## This used to work well before CUBE, but CUBE is a mess
## with violations of this.  You can turn it on all or in
## part but the build is ugly then
##
#CFLAGS  += -Wall -Wextra -Wpedantic -Werror


##
## Flags for linking image together
##
LDFLAGS		+= --static -lc  \
		   -T$(LDSCRIPT) -Wl,--gc-sections \
		   -mthumb -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16

##
## The directories to make for this build.
##
MAKE_DIRS += $(OBJ_DIR) $(EXEC_DIR) $(DEP_DIR)

##
## The list of steps to build the image
##
BUILD_LIST += dirs tags $(ELF_FILE) $(LIST_FILE) $(HEX_FILE) $(SREC_FILE) $(BIN_FILE)

.PHONY: all dirs clean

all: $(BUILD_LIST) 

-include $(DEPS)

##
## Create the directories needed for this build
##
dirs:
	@echo "Making directories $(MAKE_DIRS)"
	@echo "$(BUILD_LIST)"
	@$(MKDIR) -p $(MAKE_DIRS)

##
## Link together the executable
##
$(ELF_FILE): $(ELF_REQUIREMENTS)
	@echo "Linking $(ELF_FILE)"
	@$(LD) -o $(ELF_FILE) $(ELF_REQUIREMENTS) $(LDFLAGS)


$(HEX_FILE) :$(ELF_FILE)
	@echo "Creating $(HEX_FILE)"
	@$(OBJCOPY) -Oihex $(ELF_FILE) $(HEX_FILE)

$(SREC_FILE):$(ELF_FILE)
	@echo "Creating $(SREC_FILE)"
	@$(OBJCOPY) -Osrec $(ELF_FILE)  $(SREC_FILE)

$(BIN_FILE):$(ELF_FILE)
	@echo "Creating $(BIN_FILE)"
	@$(OBJCOPY) -Obinary $(ELF_FILE) $(BIN_FILE)

$(LIST_FILE):$(ELF_FILE)
	@echo "Creating $(LIST_FILE)"
	@$(OBJDUMP) -S $(ELF_FILE) >  $(LIST_FILE)

##
## Turn out C code into objects in our $(OBJ_DIR)
##
$(OBJ_DIR)/%.o:%.c
	@echo "Compiling  $<"
	@$(CC) $(CFLAGS) -o $@ -c $< -MMD -MF dep/$(*F).d

##
## Turn out ASM code into objects in our $(OBJ_DIR)
##
$(OBJ_DIR)/%.o:%.s
	@echo "Assembling $<"
	@$(ASM) $(ASMFLAGS)  -o $@ -c $< 

##
## Create TAGS file for our editor to find symbols in code
##
tags:
	etags $(TAG_FILES)


##
## Program target via stlink took
##
program: dirs $(BIN_FILE)
	$(FLASH) write $(BIN_FILE) 0x8000000

##
## Clean up files and directories
##
clean:
	find . -name "*~" | xargs $(RM) -f
	$(RM) -f TAGS	
	$(RM) -rf $(OBJ_DIR)
	$(RM) -rf $(EXEC_DIR)
	$(RM) -rf $(DEP_DIR)

