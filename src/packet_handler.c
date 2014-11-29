
#include "stm32f30x.h"
#include "stm32f30x_conf.h"
#include "stm32f3_discovery.h"
#include "packet_demo.h"

/*******************************************************************************

FILE VARIABLES

 ******************************************************************************/
//
// Table of Packet Handlers
//

static PacketHandler packet_handler_table[MAX_PACKET_COUNT];

//
// The packet we are actively receiving
//
static Packet_TypeDef packet_rx;

//
// A copy of the packet we just received.  This is the double buffer so we 
// can process this copy of the packet while receiving another one
//
static Packet_TypeDef packet_copy;

//
// State machine variable for receiving the packet
//
static uint32_t packet_rx_state;

/*******************************************************************************

PRIVATE API

 ******************************************************************************/
static void packet_ping_handler(Packet_TypeDef * pkt){
  pkt->type ++;
  return;
}

static void packet_add_handler(uint8_t index, PacketHandler handler){
  packet_handler_table[index] = handler;
  return;
}

/*******************************************************************************

PUBLIC API

 ******************************************************************************/

void Packet_Init(void){
  uint8_t ii;

  packet_rx_state = PACKET_RX_STATE_TYPE;
  for (ii =0; ii <MAX_PACKET_COUNT; ii++){
    packet_handler_table[ii] = 0;
  }
  Packet_Clear(&packet_rx);
  Packet_Clear(&packet_copy);
  
  packet_add_handler(0, &packet_ping_handler);
}

//
// Clear out a Packet_TypeDef data structure
//
void Packet_Clear(Packet_TypeDef *ptr){
  uint16_t ii;
  ptr->type = 0;
  ptr->size = 0;
  for (ii =0; ii<256; ii++){
    ptr->data[ii] = 0;
  }
  ptr->crc = 0;
  return;
}

void Packet_Task(void){
  DMA_MemCopy(DMA1_Channel1, (uint32_t) &packet_rx,  (uint32_t) &packet_copy, sizeof(packet_rx));
  __WFI();
  STM_EVAL_LEDToggle(LED6);
  return;
}


void Packet_AddByte_Task(void){
  static uint16_t ii;
  
  switch(packet_rx_state){
  case PACKET_RX_STATE_TYPE:
    packet_rx.type = USART_ReceiveData(USART2);
    packet_rx_state = PACKET_RX_STATE_SIZE;
    break;
  case PACKET_RX_STATE_SIZE:
    packet_rx.size = USART_ReceiveData(USART2);
    packet_rx_state = PACKET_RX_STATE_DATA;
    ii =0;
    break;
  case PACKET_RX_STATE_DATA:
    packet_rx.data[ii] = USART_ReceiveData(USART2);
    ii++;
    if (ii == packet_rx.size){
      packet_rx_state = PACKET_RX_STATE_CRC;
      ii =0;
    }else{
      packet_rx_state = PACKET_RX_STATE_DATA;
    }
    break;
  case PACKET_RX_STATE_CRC:
    if (ii == 0){
      packet_rx.crc = (USART_ReceiveData(USART2) << 8);
      packet_rx_state = PACKET_RX_STATE_CRC;
      ii++;
    }else if (ii == 1) {
      packet_rx.crc |= USART_ReceiveData(USART2) ;
      packet_rx_state = PACKET_RX_STATE_TYPE;
      Exec_SetTask(EXEC_TASK_PACKET_TASK);
    }
    break;

  }
    
  
  return;
}
