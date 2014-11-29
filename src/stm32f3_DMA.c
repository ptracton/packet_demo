
#include "stm32f30x.h"
#include "stm32f3_DMA.h"

static IRQn_Type  channel_to_irqn(uint32_t channel)
{
    IRQn_Type ret_val;
    
    ret_val = (IRQn_Type) 0;        
    
    if (channel == DMA1_Channel1_BASE){
	ret_val = DMA1_Channel1_IRQn;           
    }
    
    if (channel == DMA1_Channel2_BASE){
	ret_val = DMA1_Channel2_IRQn;           
    }
    
    if (channel == DMA1_Channel3_BASE){
	ret_val = DMA1_Channel3_IRQn;           
    }
    
    if (channel == DMA1_Channel4_BASE){
	ret_val = DMA1_Channel4_IRQn;           
    }
    
    if (channel == DMA1_Channel5_BASE){
	ret_val = DMA1_Channel5_IRQn;           
    }
    
    if (channel == DMA1_Channel6_BASE){
	ret_val = DMA1_Channel6_IRQn;           
    }
    
    if (channel == DMA1_Channel7_BASE){
	ret_val = DMA1_Channel7_IRQn;           
    }
    
    return ret_val; 
}


void  DMA1_Channel1_IRQHandler(void)
{
    if (DMA1->ISR & DMA_ISR_TCIF1){
	DMA1->IFCR |= DMA_IFCR_CTCIF1;          
    }
    
    return;
}

void  DMA1_Channel2_IRQHandler(void)
{
    if (DMA1->ISR & DMA_ISR_TCIF2){
	DMA1->IFCR |= DMA_IFCR_CTCIF2;          
    }
    return;
}
void  DMA1_Channel3_IRQHandler(void)
{
    if (DMA1->ISR & DMA_ISR_TCIF3){
	DMA1->IFCR |= DMA_IFCR_CTCIF3;          
    }
    return;
}
void  DMA1_Channel4_IRQHandler(void)
{
    if (DMA1->ISR & DMA_ISR_TCIF4){
	DMA1->IFCR |= DMA_IFCR_CTCIF4;          
    }
    return;
}

void  DMA1_Channel5_IRQHandler(void)
{
    if (DMA1->ISR & DMA_ISR_TCIF5){
	DMA1->IFCR |= DMA_IFCR_CTCIF5;          
    }
    return;
}
void  DMA1_Channel6_IRQHandler(void)
{
    if (DMA1->ISR & DMA_ISR_TCIF6){
	DMA1->IFCR |= DMA_IFCR_CTCIF6;          
    }
    return;
}

void  DMA1_Channel7_IRQHandler(void)
{
    if (DMA1->ISR & DMA_ISR_TCIF7){
	DMA1->IFCR |= DMA_IFCR_CTCIF7;          
    }
    return;
}

void DMA_Start(void)
{
    //
    // Turn on the clock to the DMA1 module
    //
    RCC->AHBENR |= RCC_AHBENR_DMA1EN;
    
    //
    // Turn off all interrupts
    //
    DMA1->IFCR |= 0xFFFFFFFF;   
    
    return;   
}

void DMA_MemCopy(DMA_Channel_TypeDef * dma, uint32_t src, uint32_t dst, uint16_t count)
{
    //
    // Make sure the DMA is off
    //
    dma->CCR &= ~ DMA_CCR_EN;
    
    //
    // This is a memory to memory copy, increment src and dst, 32 bits wide, non-circular.  Only set the bits we want, clear all others!
    //
    dma->CCR = DMA_CCR_MEM2MEM | DMA_CCR_MSIZE_1 | DMA_CCR_PSIZE_1 | DMA_CCR_MINC | DMA_CCR_PINC | DMA_CCR_DIR | DMA_CCR_TEIE | DMA_CCR_TCIE;
    
    //
    // Set count of number of words to move
    //
    dma->CNDTR = count;
    
    //
    // Set memory address
    //
    dma->CMAR = src;
    
    //
    // set destination address
    //
    dma->CPAR = dst;
    
    //
    // Unmask Interrupt
    //
    NVIC_EnableIRQ(channel_to_irqn((uint32_t) dma));
    
    //
    // turn on DMA.  This will start the move and an interrupt will tell us it is done
    //
    dma->CCR |=  DMA_CCR_EN ;
    
    return; 
}

void DMA_MemSet(DMA_Channel_TypeDef *dma, uint32_t dst, uint32_t data, uint16_t count)
{
    //
    // Make sure the DMA is off
    //
    dma->CCR &= ~ DMA_CCR_EN;
    
    //
    // This is a memory to memory copy, increment src and dst, 32 bits wide, non-circular.  Only set the bits we want, clear all others!
    //
    dma->CCR = DMA_CCR_MEM2MEM | DMA_CCR_MSIZE_1 | DMA_CCR_PSIZE_1 | DMA_CCR_PINC | DMA_CCR_DIR | DMA_CCR_TEIE | DMA_CCR_TCIE;
    
    //
    // Set count of number of words to move
    //
    dma->CNDTR = count;
    
    //
    // Set memory address
    //
    dma->CMAR = (uint32_t) &data;
    
    //
    // set destination address
    //
    dma->CPAR = dst;
    
    //
    // turn on DMA.  This will start the move and an interrupt will tell us it is done
    //
    dma->CCR |=  DMA_CCR_EN ;
    
    return;
}

void DMA_FIFOWrite(DMA_Channel_TypeDef *dma, uint32_t src, uint32_t dst, uint16_t count)
{
    //
    // Make sure the DMA is off
    //
    dma->CCR &= ~ DMA_CCR_EN;
    
    //
    // This is a memory to memory copy, increment src and dst, 32 bits wide, non-circular.  Only set the bits we want, clear all others!
    //
    dma->CCR = DMA_CCR_MEM2MEM | DMA_CCR_MSIZE_1 | DMA_CCR_PSIZE_1 | DMA_CCR_MINC | DMA_CCR_DIR | DMA_CCR_TEIE | DMA_CCR_TCIE;
    
    //
    // Set count of number of words to move
    //
    dma->CNDTR = count;
    
    //
    // Set memory address
    //
    dma->CMAR = src;
    
    //
    // set destination address
    //
    dma->CPAR = dst;
        
    //
    // turn on DMA.  This will start the move and an interrupt will tell us it is done
    //
    dma->CCR |=  DMA_CCR_EN ;
    
    return;
}
