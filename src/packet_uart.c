
#include "stm32f30x.h"
#include "stm32f30x_conf.h"
#include "stm32f3_discovery.h"
#include "packet_demo.h"

//
// USART 2 IRQ Handler
//
void USART2_IRQHandler(void){
  uint16_t data;

  data = USART_ReceiveData(USART2);
  USART_ClearITPendingBit(USART2, USART_IT_RXNE);
  STM_EVAL_LEDToggle(LED4);
  USART_SendData(USART2, data);
  return;
}

/***
    Initialize the UART for use in packet communication.  We are using 
    USART 1, since USART 2 is in use for the CLI
 ***/
void PacketUARTInit(void){

  GPIO_InitTypeDef Pin_A2;
  GPIO_InitTypeDef Pin_A3;
  USART_InitTypeDef uart2;

  //
  // Turn on Clocks to USART 2 and GPIO A
  //
  RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);
  RCC_AHBPeriphClockCmd(RCC_AHBENR_GPIOAEN, ENABLE);

  //
  // GPIO Pin A2 --> USART 2 TX
  //
  Pin_A2.GPIO_Pin = GPIO_Pin_2;
  Pin_A2.GPIO_Mode = GPIO_Mode_AF;
  Pin_A2.GPIO_Speed = GPIO_Speed_50MHz;
  Pin_A2.GPIO_OType = GPIO_OType_PP;
  Pin_A2.GPIO_PuPd = GPIO_PuPd_UP;
  GPIO_Init(GPIOA, &Pin_A2);
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource2, GPIO_AF_7);

  //
  // GPIO Pin A3 --> USART 1 RX
  //
  Pin_A3.GPIO_Pin = GPIO_Pin_3;
  Pin_A3.GPIO_Mode = GPIO_Mode_AF;
  Pin_A3.GPIO_Speed = GPIO_Speed_50MHz;
  Pin_A3.GPIO_OType = GPIO_OType_PP;
  Pin_A3.GPIO_PuPd = GPIO_PuPd_UP;
  GPIO_Init(GPIOA, &Pin_A3);
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource3, GPIO_AF_7);

  //
  // USART 1 -- Set up as:
  //            8 bit data
  //            No Parity
  //            1 Stop Bit
  //            No Flow Control
  //            115200 BaudRate
  //
  USART_StructInit(&uart2);
  uart2.USART_BaudRate = 115200;
  USART_Init(USART2, &uart2);

  // Get the RXNE (receive not empty) IRQ so we know when a packet is 
  // starting to arrive
  USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);
  NVIC_EnableIRQ(USART2_IRQn);

  //
  // Turn on the UART, we are now live!
  //
  USART_Cmd(USART2, ENABLE);

  return;
}
