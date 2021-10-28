import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import time
import tensorflow as tf
import struct
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
from sklearn.utils import shuffle
import sys

def main():
	args = sys.argv[1:]
	if len(args) == 2 and args[0] == '-dataset_dir':
		dataset_dir = str(args[1])	

	## Use CPU only
	os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

	## Load MNIST dataset
	print("Loading dataset")
	train_images = []
	train_labels = []
	test_images = []
	test_labels = []

	dims = (10,10) # dimensions of images to train/test with

	for j in range(2): # train and test	
		for i in range(10): # 0 to 9
			if j == 0:
				read_folder = dataset_dir + '/MNIST_JPG_training/' + str(i) + '/'
			if j == 1:
				read_folder = dataset_dir + '/MNIST_JPG_testing/' + str(i) + '/'
			for filename in os.listdir(read_folder):
				img = cv2.imread(os.path.join(read_folder,filename),0) # read img as grayscale
				img = cv2.resize(img, dims, interpolation = cv2.INTER_AREA)	# resize img to fit dims
				if img is not None:
					if j == 0:
						train_images.append(img / 255) # normalize pixel vals to be between 0 - 1
						train_labels.append(i)
					if j == 1:
						test_images.append(img / 255)
						test_labels.append(i)

	## Convert to numpy arrays, flatten images - change dimensions from Nx10x10 to Nx100
	train_images = np.asarray(train_images).astype('float16')
	test_images = np.asarray(test_images).astype('float16')
	train_labels = np.asarray(train_labels).astype('uint8')
	test_labels = np.asarray(test_labels).astype('uint8')

	## Shuffle dataset
	train_images, train_labels = shuffle(train_images, train_labels)
	test_images, test_labels = shuffle(test_images, test_labels)

	## Define network structure
	model = Sequential([
		Flatten(input_shape=dims),		# reshape 10x10 to 100, layer 0
		Dense(32, activation='relu', use_bias=False),	# dense layer 1
		Dense(16, activation='relu', use_bias=False),	# dense layer 2
		Dense(10, activation='softmax', use_bias=False),	# dense layer 3
	])

	model.compile(optimizer='adam',
				  loss='sparse_categorical_crossentropy',
				  metrics=['accuracy'])


	## Train network  
	model.fit(train_images, train_labels, epochs=100, batch_size=2000, validation_split = 0.1)

	model.summary()

	start_t = time.time()
	results = model.evaluate(test_images, test_labels, verbose=0)
	totalt_t = time.time() - start_t
	print("Inference time for ", len(test_images), " test image: " , totalt_t, " seconds")


	print("test loss, test acc: ", results)

	#print(model.layers[1].weights[0].numpy().shape)
	#print(model.layers[2].weights[0].numpy().shape)
	#print(model.layers[3].weights[0].numpy().shape)

	## Retrieve network weights after training. Skip layer 0 (input layer)
	for w in range(1, len(model.layers)):
		weight_filename = "layer_" + str(w) + "_weights.txt" 
		open(weight_filename, 'w').close() # clear file
		file = open(weight_filename,"a") 
		file.write('{')
		for i in range(model.layers[w].weights[0].numpy().shape[0]):
			file.write('{')
			for j in range(model.layers[w].weights[0].numpy().shape[1]):
				file.write(str(model.layers[w].weights[0].numpy()[i][j]))
				if j != model.layers[w].weights[0].numpy().shape[1]-1:
					file.write(', ')
			file.write('}')
			if i != model.layers[w].weights[0].numpy().shape[0]-1:
				file.write(', \n')
		file.write('}')
		file.close()

	network_weights = model.layers[1].weights
	#print(network_weights)
	layer_1_W = network_weights[0].numpy()
	#print(layer_1_W)




	
	img_filename = "img_pixel_vals.txt" 
	open(img_filename, 'w').close() # clear file
	file = open(img_filename,"a") 
	file.write('{')
	for i in range(dims[1]):
		for j in range(dims[0]):
			file.write(str(test_images[0][i][j]))
			if j != dims[1]-1:
				file.write(', ')
		if i != dims[0]-1:
			file.write(', \n')
	file.write('}')
	file.close()



	print("test_image[0] label: ", test_labels[0])

	x = test_images[0]
	x = np.expand_dims(x, axis=0)
	print("NN Prediction: ", np.argmax(model.predict(x)))



	""" ------ Quantization ------ """

	import tensorflow_model_optimization as tfmot

	quantize_model = tfmot.quantization.keras.quantize_model

	# q_aware stands for for quantization aware.
	q_aware_model = quantize_model(model)

	# `quantize_model` requires a recompile.
	q_aware_model.compile(optimizer='adam',
		          loss='sparse_categorical_crossentropy',
		          metrics=['accuracy'])

	q_aware_model.summary()

	train_images_subset = train_images[0:1000] # out of 60000
	train_labels_subset = train_labels[0:1000]

	q_aware_model.fit(train_images, train_labels,
		              batch_size=50, epochs=1, validation_split=0.1)

	_, baseline_model_accuracy = model.evaluate(
		test_images, test_labels, verbose=0)

	_, q_aware_model_accuracy = q_aware_model.evaluate(
	   test_images, test_labels, verbose=0)

	print('Baseline test accuracy:', baseline_model_accuracy)
	print('Quant test accuracy:', q_aware_model_accuracy)

	converter = tf.lite.TFLiteConverter.from_keras_model(q_aware_model)
	converter.optimizations = [tf.lite.Optimize.DEFAULT]
	converter.target_spec.supported_types = [tf.float16]


	quantized_tflite_model = converter.convert()

	def evaluate_model(interpreter):
		input_index = interpreter.get_input_details()[0]["index"]
		output_index = interpreter.get_output_details()[0]["index"]

		# Run predictions on every image in the "test" dataset.
		prediction_digits = []
		for i, test_image in enumerate(test_images):
			if i % 1000 == 0:
		  		print('Evaluated on {n} results so far.'.format(n=i))
			# Pre-processing: add batch dimension and convert to float32 to match with
			# the model's input data format.
			test_image = np.expand_dims(test_image, axis=0).astype(np.float32)
			interpreter.set_tensor(input_index, test_image)

			# Run inference.
			interpreter.invoke()

			# Post-processing: remove batch dimension and find the digit with highest
			# probability.
			output = interpreter.tensor(output_index)
			digit = np.argmax(output()[0])
			prediction_digits.append(digit)

		print('\n')
		# Compare prediction results with ground truth labels to calculate accuracy.
		prediction_digits = np.array(prediction_digits)
		accuracy = (prediction_digits == test_labels).mean()
		return accuracy
	  
	interpreter = tf.lite.Interpreter(model_content=quantized_tflite_model)
	interpreter.allocate_tensors()

	test_accuracy = evaluate_model(interpreter)

	print('Quant TFLite test_accuracy:', test_accuracy)
	print('Quant TF test accuracy:', q_aware_model_accuracy)
	
	

	# from https://stackoverflow.com/a/1602964
	# retrieve quatized weights
	tensor_details = interpreter.get_tensor_details()
	layer = 1
	for dict in tensor_details:
		#print(dict)
		i = dict['index']
		if 'name' in dict:
			tensor_name = dict['name']
			if 'LastValueQuant/FakeQuantWithMinMaxVars' in tensor_name:
				tensor = interpreter.tensor(i)()
				print(tensor_name, tensor.shape, tensor)
				rows, cols = tensor.shape
				weight_filename = "layer_" + str(layer) + "_quantized_weights.txt" 
				open(weight_filename, 'w').close() # clear file
				file = open(weight_filename,"a") 
				file.write('{')
				for i in range(cols):
					file.write('{')
					for j in range(rows):
						file.write(str(tensor[j][i]))
						if j != rows-1:
							file.write(', ')
					file.write('}')
					if i != cols-1:
						file.write(', \n')
				file.write('}')
				file.close()
				layer = layer + 1
	
	
	  
	"""## Retrieve network weights after quantization. Skip layer 0 (input layer)
	for w in range(1, len(q_aware_model.layers)):
		weight_filename = "layer_" + str(w) + "quantized_weights.txt" 
		open(weight_filename, 'w').close() # clear file
		file = open(weight_filename,"a") 
		file.write('{')
		for i in range(q_aware_model.layers[w].weights[0].numpy().shape[0]):
			file.write('{')
			for j in range(q_aware_model.layers[w].weights[0].numpy().shape[1]):
				file.write(str(q_aware_model.layers[w].weights[0].numpy()[i][j]))
				if j != q_aware_model.layers[w].weights[0].numpy().shape[1]-1:
					file.write(', ')
			file.write('}')
			if i != q_aware_model.layers[w].weights[0].numpy().shape[0]-1:
				file.write(', \n')
		file.write('}')
		file.close()"""



	print("Finished")
	
	
	
if __name__=="__main__":
    main()
