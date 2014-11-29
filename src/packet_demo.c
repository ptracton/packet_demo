
#include "stm32f30x_conf.h"
#include "stm32f3_discovery.h"
#include "packet_demo.h"


int main(){
  STM_EVAL_LEDInit(LED3);
  STM_EVAL_LEDInit(LED4);
  STM_EVAL_LEDInit(LED5);
  STM_EVAL_LEDInit(LED6);
  PacketUARTInit();
  DMA_Start();
  Exec_Init();

  __enable_irq();
  STM_EVAL_LEDToggle(LED3);
  Exec_Start();

  //  while(1){
    //USART_SendData(USART2, 'A');
  //  }

  return 0;
}
