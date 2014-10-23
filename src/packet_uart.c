
#include "stm32f30x.h"
#include "stm32f30x_conf.h"
#include "packet_demo.h"

//
// USART 1 IRQ Handler
//
void USART1_IRQHandler(void){
  uint16_t data;

  data = USART_ReceiveData(USART1);
  USART_ClearITPendingBit(USART1, USART_IT_RXNE);
  USART_SendData(USART1, data);
  return;
}

/***
    Initialize the UART for use in packet communication.  We are using 
    USART 1, since USART 2 is in use for the CLI
 ***/
void PacketUARTInit(void){

  GPIO_InitTypeDef Pin_A9;
  GPIO_InitTypeDef Pin_A10;
  USART_InitTypeDef uart1;

  //
  // Turn on Clocks to USART 2 and GPIO A
  //
  RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);
  RCC_AHBPeriphClockCmd(RCC_AHBENR_GPIOAEN, ENABLE);

  //
  // GPIO Pin A9 --> USART 1 TX
  //
  Pin_A9.GPIO_Pin = GPIO_Pin_9;
  Pin_A9.GPIO_Mode = GPIO_Mode_AF;
  Pin_A9.GPIO_Speed = GPIO_Speed_50MHz;
  Pin_A9.GPIO_OType = GPIO_OType_PP;
  Pin_A9.GPIO_PuPd = GPIO_PuPd_UP;
  GPIO_Init(GPIOA, &Pin_A9);
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource9, GPIO_AF_7);

  //
  // GPIO Pin A10 --> USART 1 RX
  //
  Pin_A10.GPIO_Pin = GPIO_Pin_10;
  Pin_A10.GPIO_Mode = GPIO_Mode_AF;
  Pin_A10.GPIO_Speed = GPIO_Speed_50MHz;
  Pin_A10.GPIO_OType = GPIO_OType_PP;
  Pin_A10.GPIO_PuPd = GPIO_PuPd_UP;
  GPIO_Init(GPIOA, &Pin_A10);
  GPIO_PinAFConfig(GPIOA, GPIO_PinSource10, GPIO_AF_7);

  //
  // USART 1 -- Set up as:
  //            8 bit data
  //            No Parity
  //            1 Stop Bit
  //            No Flow Control
  //            115200 BaudRate
  //
  USART_StructInit(&uart1);
  uart1.USART_BaudRate = 115200;
  USART_Init(USART1, &uart1);

  // Get the RXNE (receive not empty) IRQ so we know when a packet is 
  // starting to arrive
  USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);
  NVIC_EnableIRQ(USART1_IRQn);

  //
  // Turn on the UART, we are now live!
  //
  USART_Cmd(USART1, ENABLE);

  return;
}
