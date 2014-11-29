#include "stdio.h"
#include "stm32f30x_conf.h"
#include "stm32f3_discovery.h"
#include "packet_demo.h"


static uint32_t ExecTaskFlag;
static ExecFunctionPointer ExecTaskList[MAX_TASK_COUNT];

void Exec_Init(void){
    uint32_t i;

    //
    // No tasks need to run yet
    //
    ExecTaskFlag = 0;
    
    //
    // Set all tasks to NULL, no task handler present
    //
    for (i=0; i<MAX_TASK_COUNT; i++){
        ExecTaskList[i] = NULL;
    }
    
    //
    // Add the actual tasks you want to run
    //
    ExecTaskList[0] = Packet_Task;
    ExecTaskList[1] = Packet_AddByte_Task;
    
    return;
}
void Exec_Start(void){
    uint32_t i;
    
    while(1){  
                
        if (ExecTaskFlag){
        
            for(i=0; i< MAX_TASK_COUNT; i++){
                if (ExecTaskFlag & (0x1 << i)){
                    Exec_ClearTask(0x1 << i);
                    if (ExecTaskList[i]){
		      STM_EVAL_LEDToggle(LED5);
                        (ExecTaskList[i])();   
                    }
                }
            }                
        }
    }
}
void Exec_SetTask(uint32_t task){
    
    //
    // Set a bit indicating a specific task is needed to run
    //
    ExecTaskFlag |= task;
    return;
}
void Exec_ClearTask(uint32_t task){
    
    //
    // Clear a bit indicating a specific task has executed
    //
    ExecTaskFlag &= ~task;
    return;
}

