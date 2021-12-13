[helloworld.c](/src/vitis/helloworld.c)

- Baremetal C application that initializes BRAM and UART on the PYNQ-Z2 CPU. Receives test images over UART from host PC and stores it in BRAM for FPGA to read.

[helloworld_FPGA_benchmark.c](/src/vitis/helloworld_FPGA_benchmark.c)

- Baremetal C application for benchmarking the FPGA neural network inference.

[helloworld_benchmark.c](/src/vitis/helloworld_benchmark.c)

- Baremetal C application for benchmarking software neural network inference.

[matmul_benchmark.c](/src/vitis/matmul_benchmark.c)

- Definitions of neural network functions and weights for baremetal software benchmark.

[matmul_benchmark.h](/src/vitis/matmul_benchmark.h)

- Header with declarations of neural network functions and weights for baremetal software benchmark.

