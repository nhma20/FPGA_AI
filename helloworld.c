#include <stdio.h>
#include "platform.h"
#include "xil_printf.h"
#include "xil_io.h"
#include "xuartps.h"
#include "xbram.h"
#include "xparameters.h"
#include <unistd.h>

//#define BRAM(A)     ((volatile u32*)px_config->MemBaseAddress)[A]
#define BRAM_FP(A)  ((volatile float*)px_config->MemBaseAddress)[A]
#define NUM_INPUTS		100
#define BYTES_PR_INPUT	4
#define BASE_ADDR		XPAR_AXI_BRAM_CTRL_0_S_AXI_BASEADDR	 // from xparameters.h, probably 0x40000000U

XBram             	x_bram;
XBram_Config    	*px_config;
XUartPs_Config 		*Config_0;
XUartPs 			Uart_PS_0;

uint8_t 		ucAXIInit();
int				xuartps_init();

int main()
{
    init_platform();

    print("\n\rStart..\n\r");

    sleep(1);

	ucAXIInit();

	xuartps_init();

	u8 BufferPtr_rx[NUM_INPUTS];

	int Status = 0;
	float bram0;

    while(1)
    {
    	/**********************************************************************************************************/

		Status = 0;
		while (Status < NUM_INPUTS*BYTES_PR_INPUT) {
			print("Status: ");
			xil_printf("%u", Status);
			print("\n\r");
			Status +=	XUartPs_Recv(&Uart_PS_0, BufferPtr_rx, (NUM_INPUTS*BYTES_PR_INPUT - Status)); // read UART
		}

		bram0 = Xil_In32(BASE_ADDR);
		print("BRAM(0): ");
		xil_printf("f", bram0);
		print("\n\r");

		for(int i = 0; i < NUM_INPUTS; i++){
			BRAM_FP(i) = BufferPtr_rx[i]; // write to BRAM
		}

		bram0 = Xil_In32(BASE_ADDR);
		print("BRAM(0): ");
		xil_printf("f", bram0);
		print("\n\r");

    }

    print("Hello World\n\r");
    print("Successfully ran Hello World application");
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
