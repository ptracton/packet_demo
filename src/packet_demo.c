
#include "stm32f30x_conf.h"
#include "stm32f3_discovery.h"
#include "packet_demo.h"


int main(){
  STM_EVAL_LEDInit(LED3);
  STM_EVAL_LEDInit(LED4);
  STM_EVAL_LEDInit(LED5);
  STM_EVAL_LEDInit(LED6);
 
  PacketUARTInit();
  __enable_irq();
  
  while(1){
    //USART_SendData(USART2, 'A');
  }

  return 0;
}
