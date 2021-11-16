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
import random

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

	dims = (15,15) # dimensions of images to train/test with

	for i in range(3): # 0 to 9
		read_folder = dataset_dir + str(i) + '/'
		for filename in os.listdir(read_folder):
			j = random.randint(0, 9)
			img = cv2.imread(os.path.join(read_folder,filename),0) # read img as grayscale
			img = cv2.resize(img, dims, interpolation = cv2.INTER_AREA)	# resize img to fit dims
			if img is not None:
				if j == 0:
					test_images.append(img / 255) # normalize pixel vals to be between 0 - 1
					test_labels.append(i)
				else:
					train_images.append(img / 255)
					train_labels.append(i)

	## Convert to numpy arrays, flatten images - change dimensions from Nx15x15 to Nx225
	train_images = np.asarray(train_images).astype('float32')
	test_images = np.asarray(test_images).astype('float32')
	train_labels = np.asarray(train_labels).astype('uint8')
	test_labels = np.asarray(test_labels).astype('uint8')

	## Shuffle dataset
	train_images, train_labels = shuffle(train_images, train_labels)
	test_images, test_labels = shuffle(test_images, test_labels)

	## Define network structure
	model = Sequential([
		Flatten(input_shape=dims),		# reshape 15x15 to 225, layer 0
		Dense(32, activation='relu', use_bias=False),	# dense layer 1
		Dense(24, activation='relu', use_bias=False),	# dense layer 2
		Dense(16, activation='relu', use_bias=False),	# dense layer 3
		Dense(3, activation='softmax', use_bias=False),	# dense layer 4
	])

	model.compile(optimizer='adam',
				  loss='sparse_categorical_crossentropy',
				  metrics=['accuracy'])

	#checkpoint_path = '/home/nm/FPGA_AI/src/python/grasp_nn/model/'
	#cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)


	## Train network  
	model.fit(train_images, train_labels, epochs=250, batch_size=2000, validation_split = 0.1)

	#tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)
	model.save("grasp_nn_model.h5")

	model.summary()

	start_t = time.time()
	results = model.evaluate(test_images, test_labels, verbose=0)
	totalt_t = time.time() - start_t
	print("Inference time for ", len(test_images), " test image: " , totalt_t, " seconds")


	print("test loss, test acc: ", results)


	
if __name__=="__main__":
    main()
