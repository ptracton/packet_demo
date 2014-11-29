#ifndef __stm32f3_EXEC_H__
#define __stm32f3_EXEC_H__
#include "stm32f30x.h"

#define MAX_TASK_COUNT 32

typedef void (*ExecFunctionPointer)(void);

void Exec_Init(void);
void Exec_Start(void);
void Exec_SetTask(uint32_t task);
void Exec_ClearTask(uint32_t task);



//
// These defines should be "1-hot"
//

#define EXEC_TASK_PACKET_TASK             0x00000001
#define EXEC_TASK_PACKET_ADD_BYTE_TASK    0x00000002

#endif

