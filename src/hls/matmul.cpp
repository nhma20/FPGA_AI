#include "matmul.hpp"


void float_to_fixed(float input[n_inputs], ap_fixed<32,24> output[n_inputs]) {
	for(int i = 0; i < n_inputs; i++){
		output[i] = input[i];
	}
}


//void fixed_to_float(ap_fixed<32,24> input[n_inputs], float output[n_inputs]) {
//	for(int i = 0; i < n_inputs; i++){
//		output[i] = input[i];
//	}
//}


/* Layer 1 matrix multiplication */
void hwmm_layer1(ap_fixed<32,24> input[n_inputs], const ap_fixed<32,24> weights[n_inputs][n_layer1], ap_fixed<32,24> output[1][n_layer1]) {

    col: for (int j = 0; j < n_layer1; ++j) {
//#pragma HLS UNROLL factor = 4
      ap_fixed<32,24> sum = 0;

      prod: for (int k = 0; k < n_inputs; ++k){
#pragma HLS UNROLL factor=2
        sum += input[k] * weights[k][j];
      }
      output[0][j] = sum;
    }

  return;
}



/* Layer 2 matrix multiplication */
void hwmm_layer2(ap_fixed<32,24> input[1][n_layer1], const ap_fixed<32,24> weights[n_layer1][n_layer2], ap_fixed<32,24> output[1][n_layer2]) {

    col: for (int j = 0; j < n_layer2; ++j) {
//#pragma HLS UNROLL
      ap_fixed<32,24> sum = 0;

      prod: for (int k = 0; k < n_layer1; ++k){
//#pragma HLS UNROLL
        sum += input[0][k] * weights[k][j];
      }
      output[0][j] = sum;
    }

  return;
}



/* Layer 3 matrix multiplication */
void hwmm_layer3(ap_fixed<32,24> input[1][n_layer2], const ap_fixed<32,24> weights[n_layer2][n_layer3], ap_fixed<32,24> output[1][n_layer3]) {

    col: for (int j = 0; j < n_layer3; ++j) {
//#pragma HLS UNROLL
      ap_fixed<32,24> sum = 0;

      prod: for (int k = 0; k < n_layer2; ++k){
//#pragma HLS UNROLL
        sum += input[0][k] * weights[k][j];
      }
      output[0][j] = sum;
    }

  return;
}



/* ReLU layer 1 activation function */
void hw_act_layer1(ap_fixed<32,24> input[1][n_layer1], ap_fixed<32,24> output[1][n_layer1]){
	loop1: for (int i = 0; i < n_layer1; i++){
//#pragma HLS UNROLL
		if (input[0][i] < 0.0)
			output[0][i] = 0.0;
		else
			output[0][i] = input[0][i];
	}

	return;
}



/* ReLU layer 2 activation function */
void hw_act_layer2(ap_fixed<32,24> input[1][n_layer2], ap_fixed<32,24> output[1][n_layer2]){
	loop1: for (int i = 0; i < n_layer2; i++){
//#pragma HLS UNROLL
		if (input[0][i] < 0.0)
			output[0][i] = 0.0;
		else
			output[0][i] = input[0][i];
	}

	return;
}



/* Softmax layer 3 activation function */
void hw_act_layer3(ap_fixed<32,24> input[1][n_layer3], ap_fixed<32,24> &pred){
	ap_fixed<32,24> max_idx = -1;
	ap_fixed<32,24> max_val = -126;
	loop1: for (int i = 0; i < n_layer3; i++){
//#pragma HLS UNROLL
		if (input[0][i] > max_val){
			max_idx = (ap_fixed<32,24>)i;
			max_val = input[0][i];
		}
	}
	pred = max_idx;
	return;
}



/* Connect NN Layers */
//ap_fixed<32,24> nn_inference(float input_img[n_inputs]){
int nn_inference(float input_img[n_inputs]){
//#pragma HLS INTERFACE mode=s_axilite port=return
//#pragma HLS INTERFACE mode=m_axi port=input_img

//#pragma HLS ARRAY_PARTITION dim=1 type=complete variable=input_img

	ap_fixed<32,24> fp_input_img[n_inputs] = {1.0};
	float_to_fixed(input_img, fp_input_img);

	ap_fixed<32,24> temp_output[1][n_layer1] = {1};
	ap_fixed<32,24> temp_output2[1][n_layer2] = {1};
	ap_fixed<32,24> temp_output3[1][n_layer3] = {1};
	ap_fixed<32,24> prediction = -1;
	int prediction_int = -1;

	hwmm_layer1(fp_input_img, weights::layer1_weights, temp_output);
	hw_act_layer1(temp_output, temp_output);
	hwmm_layer2(temp_output, weights::layer2_weights, temp_output2);
	hw_act_layer2(temp_output2, temp_output2);
	hwmm_layer3(temp_output2, weights::layer3_weights, temp_output3);
	hw_act_layer3(temp_output3, prediction);

	prediction_int = prediction;

	return prediction_int;

}


