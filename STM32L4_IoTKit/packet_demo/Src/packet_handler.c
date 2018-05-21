/*
 * packet_handler.c
 *
 *  Created on: May 12, 2018
 *      Author: ptracton
 */

/* Includes ------------------------------------------------------------------*/
#include "string.h"
#include "stdbool.h"
#include "main.h"
#include "stm32l4xx_hal.h"
#include "executive.h"
#include "packet_handler.h"

/* Private variables ---------------------------------------------------------*/
static UART_HandleTypeDef * packetHandlerUART = NULL;  // The UART to use for all communications
static PacketHandler_TypeDef rxPacket;                 // The packet we are receiving
static uint8_t rxPacketPayloadCount;                   // Keep track of payload bytes received
static PacketHandler_TypeDef txPacket;                 // The packet we are sending
static bool receivingPacket;                           // Are we receiving a packet?
static bool transmittingPacket;                        // Are we transmitting a packet?
PacketHandlerRXStateMachine_TypeDef rxStateMachine;    // State machine for receiving a packet
static uint8_t packet_char;                            // The last character received

static packetHandler packetHandlerList[PACKET_MAX_COMMAND]; // This is our list of handlers for received packets

/*
 * @brief UART IRQ handler for receiving packets
 * @retval None
 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){

  HAL_UART_Receive_IT(huart, &packet_char, 1);
  executive_SetTask(TASK_PACKET_HANDLER_RECEIVE_BYTE);

  return;
}

void packetHandler_ReceiveByte(void){
  switch (rxStateMachine){
    
  case RX_PACKET_IDLE:
    if (PACKET_PREAMBLE == packet_char){
      rxStateMachine = RX_PACKET_COMMAND;
      receivingPacket = true;
    }else{
      rxStateMachine = RX_PACKET_IDLE;
      receivingPacket = false;
    }
    break;
    
  case RX_PACKET_COMMAND:
    rxPacket.command = packet_char;
    rxStateMachine = RX_PACKET_BYTE_COUNT;
    break;

  case RX_PACKET_BYTE_COUNT:
    rxPacket.byteCount = packet_char;
    rxPacketPayloadCount = 0;
    rxStateMachine = RX_PACKET_PAYLOAD;
    break;

  case RX_PACKET_PAYLOAD:
    rxPacket.payLoad[rxPacketPayloadCount] = packet_char;
    rxPacketPayloadCount ++;

    if (rxPacketPayloadCount >=rxPacket.byteCount){
      rxStateMachine = RX_PACKET_CRC_HIGH;
    }else{
      rxStateMachine = RX_PACKET_PAYLOAD;
    }
    break;

  case RX_PACKET_CRC_HIGH:
    rxPacket.crc = (packet_char << 8);
    rxStateMachine = RX_PACKET_CRC_LOW;
    break;    

  case RX_PACKET_CRC_LOW:
    rxPacket.crc |= packet_char;
    rxStateMachine = RX_PACKET_IDLE;
    receivingPacket = false;
    executive_SetTask(TASK_PACKET_HANDLER_PROCESS_PACKET);
    break;    

    
  default:
    receivingPacket = false;
    rxStateMachine = RX_PACKET_IDLE;
    memset(&rxPacket, 0, sizeof(PacketHandler_TypeDef));
  }
  
  return;
}

void packetHandler_ProcessPacket(void){

  //TODO: Check packet CRC signature!
  
  if (NULL != packetHandlerList[rxPacket.command]){
    packetHandlerList[rxPacket.command](&rxPacket);
  }
  
  return;
}

/*
 * @brief set the UART for the packet handler code
 * @retval None
 */
void packetHandler_SetUART(UART_HandleTypeDef * ptr){
  if (NULL != ptr){
    packetHandlerUART = ptr;
  }
}


void packetHandler_Ping(PacketHandler_TypeDef * pkt){
  
  
  return;
}

void packetHandler_InstallHandler(uint8_t index, packetHandler phandle){

  if (index >= PACKET_MAX_COMMAND){
    return;
  }
  packetHandlerList[index] = phandle;
  return;
}

/*
 * @brief init thte packet handling system
 * @retval None
 */
void packetHandler_Init(void){
  memset(&rxPacket, 0, sizeof(PacketHandler_TypeDef));
  memset(&txPacket, 0, sizeof(PacketHandler_TypeDef));
  memset(&packetHandlerList, 0, PACKET_MAX_COMMAND*sizeof(packetHandler));
  receivingPacket = false;
  transmittingPacket = false;
  rxStateMachine = RX_PACKET_IDLE;
  packet_char = 0;
  rxPacketPayloadCount = 0;
  executive_InstallTask(packetHandler_ReceiveByte,
			 TASK_PACKET_HANDLER_RECEIVE_BYTE);

  executive_InstallTask(packetHandler_ProcessPacket,
			 TASK_PACKET_HANDLER_PROCESS_PACKET);
  packetHandler_InstallHandler(PACKET_PING, packetHandler_Ping);
}
