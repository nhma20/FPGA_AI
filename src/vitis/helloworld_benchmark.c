#include <stdio.h>
#include <stdlib.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_io.h"
#include "xuartps.h"
#include "xbram.h"
#include "xparameters.h"
#include <unistd.h>
#include "xtime_l.h"
#include "matmul_benchmark.h"

#define BRAM(A)     ((volatile u32*)px_config->MemBaseAddress)[A]
#define NUM_INPUTS		100 // number of pixel in input image
#define BYTES_PR_INPUT	4 	// 32 bit float = 4 bytes
#define BASE_ADDR		XPAR_AXI_BRAM_CTRL_0_S_AXI_BASEADDR	 // from xparameters.h

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

    //print("\n\rInitializing..\n\r");

    //sleep(1);

	//ucAXIInit();

	xuartps_init();

	/*uint8_t BufferPtr_rx[NUM_INPUTS*BYTES_PR_INPUT] = {0x00};

	int Status = 0;
	//int oldStatus = -1;
	uint32_t tempInt;
	float tempFloat = 0.0;*/

	//print("\n\rReady for weights transfer\n\r");

	float input_img[n_inputs] = {0.0, 0.0, 0.0, 0.0, 0.003921569, 0.003921569, 0.015686275, 0.019607844, 0.003921569, 0.0,
			0.0, 0.0, 0.0, 0.003921569, 0.0, 0.02745098, 0.13725491, 0.015686275, 0.007843138, 0.0,
			0.0, 0.0, 0.0, 0.003921569, 0.003921569, 0.34117648, 0.6, 0.015686275, 0.015686275, 0.0,
			0.0, 0.0, 0.0, 0.011764706, 0.007843138, 0.60784316, 0.54509807, 0.015686275, 0.007843138, 0.0,
			0.0, 0.0, 0.0, 0.007843138, 0.13725491, 0.9490196, 0.19607843, 0.019607844, 0.003921569, 0.0,
			0.0, 0.0, 0.0, 0.007843138, 0.4627451, 0.627451, 0.019607844, 0.007843138, 0.007843138, 0.0,
			0.0, 0.0, 0.0, 0.011764706, 0.68235296, 0.2901961, 0.0, 0.0, 0.0, 0.0,
			0.0, 0.0, 0.0, 0.02745098, 0.7529412, 0.0627451, 0.0, 0.0, 0.0, 0.0,
			0.0, 0.0, 0.0, 0.02745098, 0.6901961, 0.11372549, 0.0, 0.0, 0.0, 0.0,
			0.0, 0.0, 0.0, 0.007843138, 0.015686275, 0.007843138, 0.0, 0.0, 0.0, 0.0}; // 1

    while(1)
    {

    	for(int i = 0; i < 100; i++){
    		input_img[i] = (float)rand()/(float)(RAND_MAX/1);
    	}

	/* from https://0xstubs.org/measuring-time-in-a-bare-metal-zynq-application/ */
    	XTime tEnd, tCur;
    	u32 tUsed;
    	XTime_GetTime (& tCur);
    	int pred = nn_inference(input_img);
	//usleep (1345);
	XTime_GetTime (& tEnd);
	tUsed = ((tEnd-tCur) * 1000000)/(COUNTS_PER_SECOND);
	xil_printf ("Inference time is %d us\r\n", tUsed);

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
