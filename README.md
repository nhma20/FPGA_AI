Educational Platform for FPGA Accelerated AI in Robotics
============================================================================

Benchmarking
----------------------------------------------------------------------------

Vitis HLS reports the following ressource utilizations:

![hls_utilization_2](https://user-images.githubusercontent.com/76950970/145794324-f351360a-af86-4f62-8009-d8afefd517a2.png)

The Vivado implementation takes up the following ressources, including everything not neural network related:

![vivado_utilization_2](https://user-images.githubusercontent.com/76950970/145794315-3904b3e8-f0e7-4051-aca4-304c89b0c87b.png)

Software inference looks like the following with TCF profiler in Vitis:

![TCF_profile_PYNQ_Z2](https://user-images.githubusercontent.com/76950970/145794344-d2e5e52f-bef3-4af2-b563-1ba7eea99c9a.png)

Below is the implemented block diagram of the FPGA benchmark in Vivado:

![vivado_FPGA_benchmark_diagram](https://user-images.githubusercontent.com/76950970/145794352-a33a2c6c-56ed-49dc-9263-b2d29f3016c9.png)
