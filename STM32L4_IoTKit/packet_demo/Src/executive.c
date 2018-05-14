/*
 * executive.c
 *
 *  Created on: May 12, 2018
 *      Author: ptracton
 */

#include "stdint.h"
#include "executive.h"

#define NULL (0x00000000)

static uint32_t executiveTaskFlag;
static executiveFunctionPointer executiveTaskList[EXECUTIVE_MAX_TASK_COUNT];

void executive_Init(void){
  uint8_t i;
  executiveTaskFlag = 0;
  for (i=0; i<EXECUTIVE_MAX_TASK_COUNT; i++){
    executiveTaskList[i] = NULL;
  }
}

/*
 * This function NEVER returns!  This is the executive in operation
 */
void executive_Start(void){
  volatile static uint8_t i;
	
  while(1){
    //
    // This if statement is killing the debugger
    
    //    if (0 != executiveTaskFlag){
      for (i = 0; i < EXECUTIVE_MAX_TASK_COUNT; i++){
	if (executiveTaskFlag & (1<<i)){
	  executive_ClearTask(1<<i);
	  if (NULL != executiveTaskList[i]){
	    executiveTaskList[i]();
	  }
	}
	//      }
    }
  }  
}

void executive_SetTask(uint32_t task){
  executiveTaskFlag |= task;
}

void executive_ClearTask(uint32_t task){
  executiveTaskFlag &= ~task;
}

void executive_InstallTask(executiveFunctionPointer task, uint32_t taskID){
  if (taskID < EXECUTIVE_MAX_TASK_COUNT){
    executiveTaskList[taskID-1] = task;
  }
}

void executive_RemoveTask(uint32_t taskID){
  if (taskID < EXECUTIVE_MAX_TASK_COUNT){
    executiveTaskList[taskID-1] = NULL;
  }
}
