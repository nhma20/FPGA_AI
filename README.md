# Ultra96-V2 Simple Neural Network FPGA Inference
Introduction to AI on FPGAs

- Clone `ultra96-v2` branch of repository: `git clone --branch ultra96-v2 https://github.com/nhma20/FPGA_AI.git`
- Download and unpack the dataset: https://nextcloud.sdu.dk/index.php/s/wZg4FLSxgiigJTL

### Prerequisites
Ultra96-V2 board, power supply and JTAG programmer, PC, USB-A to micro USB cable.

Tested with:
- `Ubuntu 20.04.2 LTS (host PC)`
- `Vivado / Vitis / Vitis HLS 2021.1` (with cable drivers and board files installed)
- `Tensorflow 2.6.0`
- `OpenCV 4.2.0`
- `Python 3.8.10`

Connect the JTAG programmer to the Ultra96-V2 and make sure the `SW3` switches on the Ultra96-V2 are set up as follows:

<img src="https://user-images.githubusercontent.com/76950970/202680502-c8d98da5-8719-422e-996f-d752148d4b55.jpg" width="400">



## Flow

<img src="https://user-images.githubusercontent.com/76950970/202475201-8fd8bcf3-b685-45e6-b446-df71c0078535.jpg" width="650">

1. Customize network parameters in `mnist_net.py`. Then run the script to train network and output its weights.
2. Create HLS project with template C++ files from this repository (see steps further down in this readme). Customize parameters to fit network as defined in step 1 above. Then export RTL to obtain IP core.
3. Create Vivado project with files from this repository (see steps further down in this readme). Customize modules to fit network and IP as defined in steps above. Then generate bitstream and export hardware (with bitstream).
4. Create Vitis platform project and application project (see steps further down in this readme). Customize code to fit hardware as defined in the above steps. Build project and deploy on the Ultra96-V2 board.
5. Use `uart_test_nn.py` to randomly choose a test image and send it to the Ultra96-V2 board via UART (see steps further down in this readme). Observe the console which displays the network output, and check against the test image label - hopefully they are the same.


## 1) Train network and extract weights with mnist_net.py
- Loads dataset, defines, trains and tests simple network, extracts weights.
- Edit to customize network for performance and/or accuracy (`dims`, `model`, `epochs` etc)
- Run with : `python3 mnist_net.py -dataset_dir <PATH_TO_DATASET>` e.g. `python3 mnist_net.py -dataset_dir /home/nm/Downloads/MNIST_Dataset_JPG/`
- Prints information regarding the network such as training progress, an overview of the network structure, test accuracy, and a random test inference result at the end.
- Should generate several .txt files containing the weights of the network.

The (default) implemented network is the following:

<img src="https://user-images.githubusercontent.com/76950970/202475687-0a7e29b9-3159-4fe3-ac73-26d944a0a0d9.jpg" width="650">


## 2) Create HLS project
1. Open HLS -> Create Project -> Name and Location -> Next
2. Design files: Add files -> matmul.cpp and matmul.hpp -> Top function -> nn_inference -> Next
3. TestBench files: Add files -> matmul_tb.cpp -> Next
4. Select Configuration: Part -> xczu3eg-sbva484-1-i and period 10 ns-> Finish
5. (edit files to fit any network customization)
6. Run C Simulation to verify design with testbench file
7. Run C Synthesis (choose appropriate clock Period (ns) to match what you want in design) to synthesize design into VHDL/Verilog
   - This step outputs the estimated ressource usage, timings, and other relevant information.
8. Export RTL to obtain IP that can be imported to Vivado. IP will by default be located in HLS project folder.

Below image shows the expected resource utilization and timings as estimated by HLS:

<img src="https://user-images.githubusercontent.com/76950970/194881378-706d83f3-c932-4a47-ad25-ee805f2aaac2.png" width="750">


## 3) Create Vivado project
1. Open Vivado -> Next -> Name and location, tick create subdirectory -> Next -> RTL Project, untick Do not specify sources -> Next -> Add Directories -> .../FPGA_AI/src/vhdl/ -> Next -> Next -> Under Boards choose Ultra96-V2 -> Next -> Finish
2. Let Vivado find custom IPs
   - Tools -> IP -> Repository
   - Add folder with new IP (likely HLS project folder)
   - Can now add nn_inference to block design with 'Add IP' (Ctrl+i)
3. Create Block Design and add Zynq Ultrascale+ MPSoC Processing System and then Run Block Automation
4. Double click the Zynq module and edit the green IO peripheral fields to have a tick on UART 0 and UART 1
5. Add Axi BRAM Controller and then Run Block Automation
6. Double click axi_bram_ctrl_0 module and edit Number of BRAM interfaces to 1
7. Add Nn_inference **without** running block automation
8. From sources, drag in fix_address, not_gate, and nn_ctrl modules. 
   - nn_ctrl: Connect all ap_* ports **except** ap_rst to the corresponding port on nn_inference module. Make all 4 led_ctrl* external. Connect nn_res_in to ap_return on nn_inference. Connect rstb_busy to corresponding port on axi_bram_ctrl_0_bram. Connect i_Clk to ps_clk0 on the Zynq module. Connect i_BRAM_ce to input_img_ce0 on nn_inference module. Connect i_BRAM_addr to addr_out on fix_address module. Connect o_BRAM_addr to addrb and o_BRAM_ce to enb and o_BRAM_wr to web and o_BRAM_din to dinb on axi_bram_ctrl_0_bram.
   - fix_address: connect addr_in to input_img_address on nn_inference module. If widths do not match, double click on fix_address and edit. 
   - not_gate: Connect i_in to ap_rst on nn_ctrl. Connect o_out to ap_rst on nn_inference module.
   - nn_inference: Connect ap_clk to ps_clk0 on Zynq module. Connect input_img_q0 to doutb on axi_bram_ctrl_0_bram.
   - Connect clkb on axi_bram_ctrl_0_bram to ps_clk0.
   - Right-click anywhere in the block diagram and regenerate layout and it should look similar to the below image:
![vivado_diagram_u96](https://user-images.githubusercontent.com/76950970/194881568-65717829-969a-46c6-8ed2-e80114f63712.png)

9. In sources, right click on design_1.bd (in orange) and click create wrapper and let Vivado manage it.
10. Run Synthesis (may take a while) and open Synthesized Design. In the top right corner select I/O Planning. At the bottom, select the I/O Ports window and expand Scalar ports (4).
11. Set the I/O Std of the 4 led_ctrl* ports to LVCMOS33. From led_ctrl1 to led_ctrl4, assign the following package pins: D7, F8, F7, G7. Ctrl+s to save.
12. Go to the block diagram, save, validate design, and then Generate Bitstream (may also take a while).
13. Finally, go to File -> Export Hardware -> Next -> Include bitstream -> Next -> Location -> Next -> Finish

Below is the actual resource utilization as reported by Vivado:

<img src="https://user-images.githubusercontent.com/76950970/194882543-40cff797-90fa-42c1-98b8-a6b86c0c6c54.png" width="550">


## 4) Create Vitis project
1. Open Vitis -> Create platform project -> name -> Next -> Browse to where you saved the exported hardware -> Finish.
2. File -> New -> Application Project -> Next -> Select your platform project -> name -> Next -> Next -> Select Hello World -> Finish. 
3. Insert the C code from the helloworld.c file in this repository. Make sure NUM_INPUTS matches the parameters of the network and hardware. 
4. Edit BSP settings to use UART1 instead of UART0: Under the platform project, open platform.spr, click on "psu_cortexa53_0">"zynqmp_fsbl">"Bord Support Package" and click "Modify BSP Settings" -> Under "standalone" change "psu_uart0" to "psu_uart1". Repeat for "psu_cortexa53_0">"standalone on psu_cortexa53_0">"Bord Support Package" and "psu_pmu_0">"zynqmp_pmufw">"Bord Support Package".
5. Save and right-click application project to build it. 
6. Right-click application project and Run As -> Launch Hardware to deploy on Ultra92-V2 board. While flashing, a blue LED should light up. To check if everything flashes successfully, find port of board and ```screen /dev/ttyUSB1 115200``` and then flash again. Some text should appear during flashing.

You have now set up the following system:

<img src="https://user-images.githubusercontent.com/76950970/202704099-b04854ce-e5fa-4e44-bb0b-d3f98b779884.jpg" width="550">

- From the host PC, you can now send an image to the CPU of the Ultra96-V2 via a serial connection.
- The CPU will then load the data into BRAM.
- On the FPGA, the neural network inference IPs will grab the data from BRAM, perform inference, and load the result back into BRAM.
- The Ultra96-V2 CPU will read the result from BRAM and send it back to the host PC over the serial connection.

Time to test if it actually works.


## 5) Test FPGA neural network with uart_test_nn.py
1. Find port number of Ultra96-V2 board (e.g. `ls /dev/` and look for ttyUSB*)
2. Run uart_test_nn.py with port as argument, e.g.: `python3 uart_test_nn.py -port /dev/ttyUSB1`
3. The script sends a random test image from the dataset to the Ultra96-V2 board over UART and outputs the corresponding label. Hopefully it outputs the same number as the test image label.

Expected output:
![nn_uart_test_u96](https://user-images.githubusercontent.com/76950970/194883215-4ec03353-0f0c-4b42-9b97-501bac5497d6.png)



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



## Proposed exercises
- Change network input image resolution. At least the following needs attention: network training script (`dims`), HLS (`n_inputs`), Vivado (`fix_address`), Vitis (`NUM_INPUTS`), network testing script (`dims`) - possibly more.
- Add or change existing layers in the network to increase resource utilization and accuracy.
- Solve different computer vision problem. Get dataset, re-train network, FPGA rebuild application.
- Evaluate the network inference time in hardware and send it to host PC via UART. Have a look at the HLS ap_ctrl_hs interface image above for inspiration on which signals from the nn_inference module might be interesting.
- Implement convolutional layers for increased efficiency and accuracy.
- Quantize network to reduce inference time - change input data type to 16 or 8-bit datatype instead of 32-bit float. The following links may be helpful:
   - [Tensorflow guide on quantization after training](https://www.tensorflow.org/model_optimization/guide/quantization/post_training)
   - [Tensorflow guide on quantization before training](https://www.tensorflow.org/model_optimization/guide/quantization/training)
- Customize network parameters to improve accuracy and/or inference time. Some interesting parameters: input image resolution, number of layers, number of neurons in each layer, number of training epochs etc.
- Optimize HLS implementation to decrease latency using directives/#pragmas to e.g. unroll loops. 
   - [Xilinx tips on HLS optimization](https://www.xilinx.com/html_docs/xilinx2021_1/vitis_doc/vitis_hls_optimization_techniques.html)


