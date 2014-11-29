
#ifndef __stm32f3_DMA_H__
#define __stm32f3_DMA_H__

void DMA_Start(void);
void DMA_Interrupt(DMA_Channel_TypeDef *dma, uint8_t interrupt, uint8_t state);
void DMA_MemCopy(DMA_Channel_TypeDef * dma, uint32_t src, uint32_t dst, uint16_t count);
void DMA_MemSet(DMA_Channel_TypeDef *dma, uint32_t dst, uint32_t data, uint16_t count);
void DMA_FIFOWrite(DMA_Channel_TypeDef *dma, uint32_t src, uint32_t dst, uint16_t count);

#endif


