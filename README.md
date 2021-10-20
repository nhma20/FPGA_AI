# FPGA_AI
Introduction to AI on FPGAs

### Prerequisites
Tested with:
- Ubuntu 20.04.2 LTS (host PC)
- Vivado / Vitis 2021.1 (with cable drivers and board files installed)
Board files installed by creating new project, and pressing refresh (lower left corner) when looking for boards. Ultra96V2 should appear now. Can close Vivado before finishing creation of new project. 
- Download and unpack the dataset: https://nextcloud.sdu.dk/index.php/s/wZg4FLSxgiigJTL


## HLS ap_ctrl_hs interface
![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/interface.png?raw=true)

## HLS Material
- Excellent HLS walkthrough (with occasional bad audio):
   - https://www.youtube.com/watch?v=i_nQmjEaMVs
- Xilinx HLS User Guide (v2021.1)
   - https://www.xilinx.com/support/documentation/sw_manuals/xilinx2021_1/ug1399-vitis-hls.pdf

## Stuff
Stuff
1. Let Vivado find custom IPs
   - Tools -> IP -> Repository
   - Add folder with new IP (likely HLS project folder)
2. nn_inference works in Vivado simulation and hardware
   - Might have to simulate first
   - Then generate bitstream and deploy on FPGA


## TODO
0. :green_circle: Make sure image pixel values are loaded into NN IP
1. :green_circle: Make sure reset is correct
2. :yellow_circle: Set up PS side or UART for easier debugging
3. :green_circle: Make work with block memory instead of array input
