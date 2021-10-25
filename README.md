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

## mnist_net.py
- Loads dataset, defines, trains and tests simple network, extracts weights.
- Edit to customize network for performance and/or accuracy (dims, model, epochs etc)
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
   - Might have to simulate first
   - Then generate bitstream and deploy on FPGA
3. Vitis link to math.h library for ´#include "math.h"´
   - Right-click application project -> Properties -> C/C++ Build -> Tool Settings -> ARM v7 gcc linker -> Libraries
![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/RCAP.png?raw=true)
![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/linkmath.png?raw=true)
   - add ´m´ to Libraries -> Apply and close

## Pynq-Z2 ressources:

![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/xc7z020.png?raw=true)

## Vivado example block design:

![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/nn_vivado.png?raw=true)



## TODO
:yellow_circle: Set up UART to send images to PL for inference
