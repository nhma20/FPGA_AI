# FPGA_AI
Introduction to AI on FPGAs

### Prerequisites
- Download and unpack the dataset: https://nextcloud.sdu.dk/index.php/s/wZg4FLSxgiigJTL

Tested with:
- `Ubuntu 20.04.2 LTS (host PC)`
- `Vivado / Vitis 2021.1` (with cable drivers and board files installed)
   - Place board_files folder in .../Xilinx/Vivado/2021.1/data/boards/ directory to install pynq-z2 board files.
- `Tensorflow 2.6.0`
- `OpenCV 4.2.0`
- `Python 3.8.10`

## Flow
1. Customize network parameters in `mnist_net.py`. Then run the script to train network and output its weights.
2. Create HLS project with template C++ files from this repository (see steps further down in this readme). Customize parameters to fit network as defined in step 1 above. Then export RTL to obtain IP core.
3. Create Vivado project with files from this repository (see steps further down in this readme). Customize modules to fit network and IP as defined in steps above. Then generate bitstream and export hardware (with bitstream).
4. Create Vitis platform project and application project (see steps further down in this readme). Customize code to fit hardware as defined in the above steps. Build project and deploy on the Pynq-Z2 board.
5. Use `weights_UART.py` to randomly choose a test image and send it to the Pynq-Z2 board via UART (see steps further down in this readme). Observe LED[0:3], which displays the network output in binary, and check against the test image label - hopefully they are the same.


## mnist_net.py
- Loads dataset, defines, trains and tests simple network, extracts weights.
- Edit to customize network for performance and/or accuracy (`dims`, `model`, `epochs` etc)
- Run with: `python3 mnist_net.py`


## Create HLS project
1. Open HLS -> Create Project -> Name and Location -> Next
2. Design files: Add files -> matmul.cpp and matmul.hpp -> Top function -> nn_inference -> Next
3. TestBench files: Add files -> matmul_tb.cpp -> Next
4. Select Configuration: Part -> Boards -> pynq-z2 -> Finish
5. (edit files)
6. Run C Simulation to verify design with testbench file
7. Run C Synthesis (choose appropriate clock Period (ns) to match what you want in design) to synthesize design into VHDL/Verilog
8. (Run Cosimulation)
9. Export RTL to obtain IP that can be imported to Vivado. IP will by default be located in HLS project folder.


## Create Vivado project
1. Open Vivado -> Next -> Name and location, tick create subdirectory -> Next -> RTL Project, untick Do not specify sources -> Next -> Add Directories -> .../FPGA_AI/src/vhdl/ -> Next -> Next -> Under Boards choose pynq-z2 -> Next -> Finish
2. Let Vivado find custom IPs
   - Tools -> IP -> Repository
   - Add folder with new IP (likely HLS project folder)
   - Can now add nn_inference to block design with 'Add IP' (Ctrl+i)
3. Create Block Design and add ZYNQ7 Processing System and then Run Block Automation
4. Double click the Zynq module and edit the green IO peripheral fields to only have a tick on UART 0
5. Add Axi BRAM Controller and then Run Block Automation
6. Double click axi_bram_ctrl_0 module and edit Number of BRAM interfaces to 1
7. Add Nn_inference **without** running block automation
8. From sources, drag in fix_address, not_gate, and nn_ctrl modules. 
   - nn_ctrl: Connect all ap_* ports **except** ap_rst to the corresponding port on nn_inference module. Make all 4 led_ctrl* external. Connect nn_res_in to ap_return on nn_inference. Connect rstb_busy to corresponding port on axi_bram_ctrl_0_bram. Connect i_Clk to FCLK_CLK0 on the Zynq7 module.
   - fix_address: connect addr_in to input_img_address on nn_inference module. If widths do not match, double click on fix_address and edit. Expand BRAM_PORTB on axi_bram_ctrl_0_bram and connect addrb to addr_out on fix_address.
   - not_gate: Connect i_in to ap_rst on nn_ctrl. Connect o_out to ap_rst on nn_inference module.
   - nn_inference: Connect ap_clk to FCLK_CLK0 on Zynq7 module. Connect input_img_q0 to doutb on axi_bram_ctrl_0_bram. Connect input_img_c0 to enb on axi_bram_ctrl_0_bram.
   - Connect clkb on axi_bram_ctrl_0_bram to FCLK_CLK0.
   - Ricght click anywhere in the block diagram and regenerate layout and it should look similar to the below image:
![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/vivado_diagram.png?raw=true)

9. In sources, right click on design_1.bd (in orange) and click create wrapper and let Vivado manage it.
10. Run Synthesis (may take a while) and open Synthesized Design. In the top right corner select I/O Planning. At the bottom, select the I/O Ports window and expand Scalar ports (4).
11. Set the I/O Std of the 4 led_ctrl* ports to LVCMOS33. From led_ctrl1 to led_ctrl4, assign the following package pins: R14, P14, N16, M14. Ctrl+s to save.
12. Go to the block diagram, save, validate design, and then Generate Bitstream (may also take a while).
13. Finally, go to File -> Export Hardware -> Next -> Include bitstream -> Next -> Location -> Next -> Finish


## Create Vitis project
1. Open Vitis -> Create platform project -> name -> Next -> Browse to where you saved the exported hardware -> Finish.
2. File -> New -> Application Project -> Next -> Select your platform project -> name -> Next -> Next -> Select Hello World -> Finish. 
3. Insert the C code from the helloworld.c file in this repository. Make sure NUM_INPUTS matches the parameters of the network and hardware. 
4. Save and right-click application project to build it. 
5. Right-click application project and Run As -> Launch Hardware to deploy on Pynq-Z2 board. Some of the 4 LED[0:3] should light up. 


## Test FPGA neural network with weights_UART.py
1. Find port number of Pynq-Z2 board (e.g. `ls /dev/` and look for ttyUSB*)
2. Run weights_UART.py with port as argument, e.g.: `python3 weights_UART.py -port /dev/ttyUSB1`
3. The script sends a random test image from the dataset to the Pynq board over UART and outputs the corresponding label. Hopefully LED[0:3] lights up in the same binary number as the test image label.


## Speed up HLS implementation
- Unroll loops with: `#pragma HLS UNROLL`. Append factor=X if HLS should not unroll fully but with factor X.
   - Reduces latency ~10x
   - May introduce negative slack which would require longer clock periods (lower clock frequency). Can use clocking wizard to hit desired target.
- Perhaps possible to save cycles by using parallel IO instead of sequential memory reads.
   - Fully parallel IO with: `#pragma HLS ARRAY_PARTITION dim=1 type=complete variable=input_img`
   - Default is simple memory interace if no pragma specified


## HLS ap_ctrl_hs interface
![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/interface.png?raw=true)

## HLS Material
- Excellent HLS walkthrough (with occasional bad audio):
   - https://www.youtube.com/watch?v=i_nQmjEaMVs
- Xilinx HLS User Guide (v2021.1)
   - https://www.xilinx.com/support/documentation/sw_manuals/xilinx2021_1/ug1399-vitis-hls.pdf


## Stuff
1. Let Vivado find custom IPs
   - Tools -> IP -> Repository
   - Add folder with new IP (likely HLS project folder)
   - Can now add nn_inference to block design with 'Add IP' (Ctrl+i)
2. nn_inference works in Vivado simulation and hardware
3. Vitis link to math.h library for `#include "math.h"`
   - Right-click application project -> Properties -> C/C++ Build -> Tool Settings -> ARM v7 gcc linker -> Libraries
![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/RCAP.png?raw=true)
![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/linkmath.png?raw=true)
   - add `m` to Libraries -> Apply and close

## Pynq-Z2 ressources:

![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/xc7z020.png?raw=true)

