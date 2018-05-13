/*
 * executive.h
 *
 *  Created on: May 12, 2018
 *      Author: ptracton
 */

#ifndef EXECUTIVE_H_
#define EXECUTIVE_H_

// These defines should be 1 hot encoded!
#define TASK_PACKET_HANDLER_RECEIVE_BYTE   (0x00000001)
#define TASK_PACKET_HANDLER_PROCESS_PACKET (0x00000002)

#define EXECUTIVE_MAX_TASK_COUNT 32
typedef void (*executiveFunctionPointer)(void);

void executive_Init(void);
void executive_Start(void);
void executive_SetTask(uint32_t task);
void executive_ClearTask(uint32_t task);
void executive_InstallTask(executiveFunctionPointer task, uint32_t taskID);
void executive_RemoveTask(uint32_t taskID);

#endif /* EXECUTIVE_H_ */
