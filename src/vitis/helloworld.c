#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_io.h"
#include "xuartps.h"
#include "xbram.h"
#include "xparameters.h"
#include <unistd.h>

#define BRAM(A)     ((volatile u32*)px_config->MemBaseAddress)[A]
#define NUM_INPUTS		100 // number of pixel in input image
#define BYTES_PR_INPUT	4 	// 32 bit float = 4 bytes
#define BASE_ADDR		XPAR_AXI_BRAM_CTRL_0_S_AXI_BASEADDR	 // from xparameters.h

XBram             	x_bram;
XBram_Config    	*px_config;
XUartPs_Config 		*Config_1;
XUartPs 			Uart_PS_1; // UART 1 for Ultra96-V2

uint8_t 		ucAXIInit();
int				xuartps_init();
void 			printBits(unsigned int num);
float 			IntBitsToFloat(long long int bits);

int main()
{
    init_platform();

    xil_printf("\n\rInitializing..\n\r");

	ucAXIInit();

	xuartps_init();

	uint8_t BufferPtr_rx[NUM_INPUTS*BYTES_PR_INPUT] = {0x00};

	int Status = 0;
	uint32_t tempInt;
	float tempFloat = 0.0;

	xil_printf("\n\rReady for data transfer\n\r");

    while(1)
    {
		Status = 0;

		while (Status < NUM_INPUTS*BYTES_PR_INPUT) {

//			if(Status == 1){
//				xil_printf("Started receiving data");
//			}

			BufferPtr_rx[Status] = XUartPs_RecvByte(XPAR_XUARTPS_1_BASEADDR); // read UART
			Status ++;
//			xil_printf("Status: %d\n\r", Status);
//			xil_printf("Newest Data: %d\n\r", BufferPtr_rx[Status-1]);
		}

//		xil_printf("Finished receiving data");

		for(int i = 0; i < NUM_INPUTS; i++){

			// concatenate 8-but input messages into 32-bit values
			tempInt = ((BufferPtr_rx[i*4+3]<<24) | (BufferPtr_rx[i*4+2]<<16) | (BufferPtr_rx[i*4+1]<<8) | BufferPtr_rx[i*4]);
			// prints current values in BRAM
			tempFloat = *((float *)&tempInt); 	// int bits to float
			char buffer2[10];
			sprintf(buffer2, "%f", tempFloat);//tempInt);
//			xil_printf("BRAM[%d]:", i);
//			xil_printf(buffer2);

			BRAM(i) = tempInt; // write to BRAM
		}

		sleep(0.1);
		xil_printf("Network output: %u\n\r", BRAM(128));

    }

    print("Shutting down");
    cleanup_platform();
    return 0;
}

uint8_t 	ucAXIInit(){
	/*************************
	*  BRAM initialization   *
	*************************/
	xil_printf("\n\rBRAM init...\n");
	px_config = XBram_LookupConfig(XPAR_BRAM_0_DEVICE_ID);
	if (px_config == (XBram_Config *) NULL) {
		xil_printf("\n\rBRAM init failed\n");
		return XST_FAILURE;
	}
	int x_status 	= 	XBram_CfgInitialize(&x_bram, px_config,
			px_config->CtrlBaseAddress);
	if (x_status != XST_SUCCESS) {
		xil_printf("\n\rBRAM init failed\n");
		return XST_FAILURE;
	}
	xil_printf("\n\rBRAM init success\n");
	return XST_SUCCESS;
}


int xuartps_init(){
	/*************************
	 * UART 0 initialization *
	 *************************/
	xil_printf("\n\rUART 1 init...\n");
	Config_1 = XUartPs_LookupConfig(XPAR_XUARTPS_1_DEVICE_ID);
	if (NULL == Config_1) {
		xil_printf("\n\rUART 1 init failed\n");
		return XST_FAILURE;
	}
	int uart_x_status = XUartPs_CfgInitialize(&Uart_PS_1, Config_1, Config_1->BaseAddress);
	if (uart_x_status != XST_SUCCESS) {
		xil_printf("\n\rUART 1 init failed\n");
		return XST_FAILURE;
	}
	xil_printf("\n\rUART 1 init success\n");
	return XST_SUCCESS;
}
