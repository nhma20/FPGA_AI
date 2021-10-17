# FPGA_AI
Introduction to AI on FPGAs

### Prerequisites
Tested with:
- Ubuntu 20.04.2 LTS (host PC)
- Vivado / Vitis 2021.1 (with cable drivers and board files installed)
Board files installed by creating new project, and pressing refresh (lower left corner) when looking for boards. Ultra96V2 should appear now. Can close Vivado before finishing creation of new project. 
- Download and unpack the dataset: https://nextcloud.sdu.dk/index.php/s/wZg4FLSxgiigJTL


![Alt text](https://github.com/nhma20/FPGA_AI/blob/main/pictures/interface.png?raw=true)


## Stuff
Stuff
1. Stuff


- Let Vivado find custom IPs
   - Tools -> IP -> Repository
   - Add folder with new IP (likely HLS project folder)


## TODO
0. :yellow_circle: Make sure image pixel values are loaded into NN IP
1. :yellow_circle: Make sure reset is correct
2. :yellow_circle: Set up PS side or UART for easier debugging
