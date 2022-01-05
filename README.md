Educational Platform for FPGA Accelerated AI in Robotics
============================================================================

Introduction to AI on FPGAs
----------------------------------------------------------------------------

This branch (ap_fixed) follows the same implementation flow as the [main](https://github.com/nhma20/FPGA_AI/tree/main) branch. The main difference is the use of ```ap_fixed<32,24>``` fixed point datatypes in the HLS implementation instead of single precision ```float```. This is done in an effort to increase throughput and reduce unnessecary resource utilization. 

By simply switching out all ```float``` occurences with ```ap_fixed<32,24>``` in [matmul.cpp](/src/hls/matmul.cpp), [matmul.hpp](/src/hls/matmul.hpp), and [matmul_tb.cpp](/src/hls/matmul_tb.cpp), the estimated latency drops ~8x, BRAM usage drops 2x, DSP usage drops ~4x, FF usage drops ~1.35x, and LUT usage drops 3x.

Below is the HLS Synthesis Summary when using ```float```:
![hls_float_nn](https://user-images.githubusercontent.com/76950970/148224660-2dd4cddc-b9dc-445d-ba16-48690c73f3da.png)

And here is the HLS Synthesis Summary when using ```ap_fixed<32,24>```:
![hls_ap_fixed_nn png](https://user-images.githubusercontent.com/76950970/148224677-eafeb439-b870-4086-9d06-3dcfeeeea0ac.png)
