#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_io.h"
#include "xuartps.h"
#include "xbram.h"
#include "xparameters.h"
#include <unistd.h>

#define BRAM(A)     ((volatile u32*)px_config->MemBaseAddress)[A]
#define NUM_INPUTS		100 					// number of pixel in input image
#define BYTES_PR_INPUT		4 					// 32 bit float = 4 bytes
#define BASE_ADDR		XPAR_AXI_BRAM_CTRL_0_S_AXI_BASEADDR	// from xparameters.h

XBram             	x_bram;
XBram_Config    	*px_config;
XUartPs_Config 		*Config_0;
XUartPs 			Uart_PS_0;

uint8_t 		ucAXIInit();
int				xuartps_init();
void 			printBits(unsigned int num);
float 			IntBitsToFloat(long long int bits);

int main()
{
    init_platform();

    print("\n\rInitializing..\n\r");

    sleep(1);

	ucAXIInit();

	xuartps_init();

	uint8_t BufferPtr_rx[NUM_INPUTS*BYTES_PR_INPUT] = {0x00};

	int Status = 0;
	uint32_t tempInt;
	float tempFloat = 0.0;

	print("\n\rReady for weights transfer\n\r");

    while(1)
    {
		Status = 0;

		while (Status < NUM_INPUTS*BYTES_PR_INPUT) {
			BufferPtr_rx[Status] = XUartPs_RecvByte(XPAR_XUARTPS_0_BASEADDR); // read UART
			Status ++;
		}


		for(int i = 0; i < NUM_INPUTS; i++){
			// concatenate 8-bit input messages into 32-bit values
			tempInt = ((BufferPtr_rx[i*4+3]<<24) | (BufferPtr_rx[i*4+2]<<16) | (BufferPtr_rx[i*4+1]<<8) | BufferPtr_rx[i*4]);
			// prints current values in BRAM
			tempFloat = *((float *)&tempInt); 	// int bits to float
			char buffer2[10];
			sprintf(buffer2, "%f", tempFloat);
			xil_printf("BRAM[%d]:", i);
			xil_printf(buffer2);
			print("\n\r");

			BRAM(i) = tempInt; // write to BRAM
		}
    }

    print("Shutting down");
    cleanup_platform();
    return 0;
}

uint8_t 	ucAXIInit(){
	/*************************
	*  BRAM initialization   *
	*************************/
	px_config = XBram_LookupConfig(XPAR_BRAM_0_DEVICE_ID);
	if (px_config == (XBram_Config *) NULL) {
		return XST_FAILURE;
	}
	int x_status 	= 	XBram_CfgInitialize(&x_bram, px_config,
			px_config->CtrlBaseAddress);
	if (x_status != XST_SUCCESS) {
		return XST_FAILURE;
	}
	return XST_SUCCESS;
}


int xuartps_init(){
	/*************************
	 * UART 0 initialization *
	 *************************/
	Config_0 = XUartPs_LookupConfig(XPAR_XUARTPS_0_DEVICE_ID);
	if (NULL == Config_0) {
		return XST_FAILURE;
	}
	int uart_x_status = XUartPs_CfgInitialize(&Uart_PS_0, Config_0, Config_0->BaseAddress);
	if (uart_x_status != XST_SUCCESS) {
		return XST_FAILURE;
	}
	return XST_SUCCESS;
}
