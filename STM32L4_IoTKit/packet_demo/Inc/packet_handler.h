/*
 * packet_handler.h
 *
 *  Created on: May 12, 2018
 *      Author: ptracton
 */

#ifndef PACKET_HANDLER_H_
#define PACKET_HANDLER_H_

/* defines ------------------------------------------------------------*/
#define PACKET_PREAMBLE (0xC7)
#define PACKET_PAYLOAD_SIZE 256

/* data structures ------------------------------------------------------------*/
typedef enum{
  RX_PACKET_IDLE = 0x00,
  RX_PACKET_COMMAND,
  RX_PACKET_BYTE_COUNT,
  RX_PACKET_PAYLOAD,
  RX_PACKET_CRC_HIGH,
  RX_PACKET_CRC_LOW,
  RX_PACKET_ERROR
} PacketHandlerRXStateMachine_TypeDef;

typedef enum{
  PACKET_PING = 0x00,
  PACKET_ID,
  PACKET_MAX_COMMAND
} PacketHandlerCommands_TypeDef;

typedef struct{
  PacketHandlerCommands_TypeDef command;
  uint8_t byteCount;
  uint8_t payLoad[PACKET_PAYLOAD_SIZE];
  uint16_t crc;
} PacketHandler_TypeDef;

typedef void (*packetHandler)(PacketHandler_TypeDef *);

/* function prototypes ------------------------------------------------------------*/
void packetHandler_SetUART(UART_HandleTypeDef * ptr);
void packetHandler_Init(void);

#endif /* PACKET_HANDLER_H_ */
