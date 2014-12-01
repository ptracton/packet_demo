#include "stdint.h"

#ifndef __PACKET_HANDLER_H__
#define __PACKET_HANDLER_H___

#define MAX_PACKET_COUNT 32

#define PACKET_RX_STATE_IDLE  0
#define PACKET_RX_STATE_TYPE  1
#define PACKET_RX_STATE_SIZE  2
#define PACKET_RX_STATE_DATA  3
#define PACKET_RX_STATE_CRC   4

#define PACKET_PREAMBLE_BYTE (0xC7)

/*******************************************************************************

Data Structures

 ******************************************************************************/
typedef struct{
  uint8_t type;
  uint8_t size;
  uint8_t data[256];
  uint16_t crc;
} Packet_TypeDef;

typedef void (*PacketHandler)(Packet_TypeDef *);

/*******************************************************************************

PUBLIC API

 ******************************************************************************/
void Packet_Init(void);
void Packet_Clear(Packet_TypeDef *);
void Packet_AddByte_Task(void);
void Packet_Task(void);

#endif
