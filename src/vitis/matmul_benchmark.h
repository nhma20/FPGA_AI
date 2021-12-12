#define n_inputs 100
#define n_layer1 32
#define n_layer2 16
#define n_layer3 10

void hwmm_layer1(float input[n_inputs], const float weights[n_inputs][n_layer1], float output[1][n_layer1]);
void hw_act_layer1(float input[1][n_layer1], float output[1][n_layer1]);
void hwmm_layer2(float input[1][n_layer1], const float weights[n_layer1][n_layer2], float output[1][n_layer2]);
void hw_act_layer2(float input[1][n_layer2], float output[1][n_layer2]);
void hwmm_layer3(float input[1][n_layer2], const float weights[n_layer2][n_layer3], float output[1][n_layer3]);
int hw_act_layer3(float input[1][n_layer3], int pred);
int nn_inference(float input_img[n_inputs]);






