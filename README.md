Educational Platform for FPGA Accelerated AI in Robotics
============================================================================

Benchmarking
----------------------------------------------------------------------------

## Flow
1) Follow ``main`` branch to build network with Tensorflow and Vivado IP with HLS.
2) Use ``benchmark`` branch VHDL files and set up Vivado block diagram as shown below in this readme. Export hardware+bitstream
3) Use new exported hardware to create platform in Vitis.
4) Benchmarking
  - FPGA inference
    - Create application project with new platform and [helloworld_FPGA_benchmark.c](/src/vitis/helloworld_FPGA_benchmark.c).
    - Use [FPGA_benchmark.py](/src/python/FPGA_benchmark.py) to send random image to FPGA and read the inference time response.
    - LEDs should behave as in ``main`` branch and show inference prediction.
    - Timing based on number of clock cycles between each ``ap_done`` signal of the nn_inference IP module.
  - Software inference
    - Create application project with new platform and [helloworld_benchmark.c](/src/vitis/helloworld_benchmark.c), [matmul_benchmark.c](/src/vitis/matmul_benchmark.c), and [matmul_benchmark.h](/src/vitis/matmul_benchmark.h). 
    - Use [software_benchmark.py](/src/python/software_benchmark.py) to read the inference time response.
    - LEDs should be static in this benchmark.
    - Timing based on difference between two ``XTime_GetTime`` (``xtime_l.h`` livrary) calls.



Vitis HLS reports the following ressource utilizations:

![hls_utilization_2](https://user-images.githubusercontent.com/76950970/145794324-f351360a-af86-4f62-8009-d8afefd517a2.png)

The Vivado implementation takes up the following ressources, including everything not neural network related:

![vivado_utilization_2](https://user-images.githubusercontent.com/76950970/145794315-3904b3e8-f0e7-4051-aca4-304c89b0c87b.png)

Software inference looks like the following with TCF profiler in Vitis:

![TCF_profile_PYNQ_Z2](https://user-images.githubusercontent.com/76950970/145794344-d2e5e52f-bef3-4af2-b563-1ba7eea99c9a.png)

Below is the implemented block diagram of the FPGA benchmark in Vivado:

![vivado_FPGA_benchmark_diagram](https://user-images.githubusercontent.com/76950970/145794352-a33a2c6c-56ed-49dc-9263-b2d29f3016c9.png)
