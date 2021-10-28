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
	train_images = np.asarray(train_images).astype('float32')
	test_images = np.asarray(test_images).astype('float32')
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
	model.fit(train_images, train_labels, epochs=50, batch_size=2000, validation_split = 0.1)

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




	
	"""img_filename = "img_pixel_vals.txt" 
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
	file.close()"""


	"""img_filename = "img_pixel_vals_vhdl_array.txt" 
	open(img_filename, 'w').close() # clear file
	file = open(img_filename,"a") 
	file.write('(')
	for i in range(dims[1]):
		for j in range(dims[0]):
			file.write('"')
			wstr = ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', test_images[0][i][j]))
			file.write(wstr)
			file.write('"')
			if j != dims[1]-1:
				file.write(', ')
		if i != dims[0]-1:
			file.write(', \n')
	file.write(')')
	file.close()"""


	"""img_filename = "img_pixel_vals.coe" 
	open(img_filename, 'w').close() # clear file
	file = open(img_filename,"a") 
	file.write('memory_initialization_radix=2;\n') # radix 2 = binary, radix 10 = decimal
	file.write('memory_initialization_vector=\n')
	for i in range(dims[1]):
		for j in range(dims[0]):
			wstr = ''.join('{:0>8b}'.format(c) for c in struct.pack('!f', test_images[0][i][j]))
			file.write(wstr)
			if i == dims[0]-1 and j == dims[1]-1:
				file.write(';')
			else:
				file.write(',\n')
	file.close()"""

	print("test_image[0] label: ", test_labels[0])

	x = test_images[0]
	x = np.expand_dims(x, axis=0)
	print("NN Prediction: ", np.argmax(model.predict(x)))


	print("Finished")
	
	
	
if __name__=="__main__":
    main()
