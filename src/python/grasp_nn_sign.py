import numpy as np
import cv2
import os
import time
import tensorflow as tf
import struct
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Activation
from sklearn.utils import shuffle
import sys
import random
import csv


def main():
	args = sys.argv[1:]
	if len(args) == 2 and args[0] == '-dataset_dir':
		dataset_dir = str(args[1])	

	## Use CPU only
	os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

	dims = (15,15) # dimensions of images to train/test with

	## Load MNIST dataset
	print("Loading dataset")
	train_images = []
	train_labels = []
	test_images = []
	test_labels = []
	
	
	read_paths = [dataset_dir + 'sign_mnist_train.csv', dataset_dir + 'sign_mnist_test.csv']

	for i in range(2):
		with open(read_paths[i]) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if line_count == 0:
				    line_count += 1
				else:
					#print(row[0])
					#if row[0] == "2" or row[0] == "14":					
					img = np.zeros((28,28))
					for j in range(28):
						for k in range(28):
							img[j][k] = row[j*28+k]
					img = cv2.resize(img, dims, interpolation = cv2.INTER_AREA)	# resize img to fit dims
					if i == 0:
						train_images.append(img / 255)
						if row[0] == "2":
							train_labels.append(0)
						elif row[0] == "14":
							train_labels.append(1)
						else:
							train_labels.append(2)
					else:
						#if random.randrange(10) == 1:
						test_images.append(img / 255)
						if row[0] == "2":
							test_labels.append(0)
						elif row[0] == "14":
							test_labels.append(1)		
						else:
							test_labels.append(2)
							
					"""print(train_labels[-1])
					plt.imshow(train_images[-1])
					plt.colorbar()
					plt.show()	"""				
							

	"""# Data augmentation
	print("augmenting data..")
	shift_size = (dims[0]/4)
	for i in range(len(train_images)):
		width1 = train_images[i].shape[1]
		height1 = train_images[i].shape[0]
		# translate horizontally
		transvar = np.random.randint(-shift_size,shift_size,size=1) # randomly decide how much to translate horizontally
		T = np.float32([[1, 0, transvar], [0, 1, 0]])
		img_translation = cv2.warpAffine(train_images[i], T, (width1, height1))
		train_labels.append(train_labels[i]) # no change in label
		train_images.append(img_translation)

		# translate vertically
		transvar = np.random.randint(-shift_size,shift_size,size=1) # randomly decide how much to translate vertically
		T = np.float32([[1, 0, 0], [0, 1, transvar]])
		img_translation = cv2.warpAffine(train_images[i], T, (width1, height1))
		train_labels.append(train_labels[i]) # no change in label
		train_images.append(img_translation)
		
		# translate vertically and horizontally
		transvarhor = np.random.randint(-shift_size,shift_size,size=1) # randomly decide how much to translate horizontally
		transvarver = np.random.randint(-shift_size,shift_size,size=1) # randomly decide how much to translate vertically
		train_labels.append(train_labels[i])
		T = np.float32([[1, 0, transvarhor], [0, 1, transvarver]])
		img_translation = cv2.warpAffine(train_images[i], T, (width1, height1))
		train_images.append(img_translation)

		# flip image 
		flipimg = cv2.flip(train_images[i], 1)
		train_images.append(flipimg)
		train_labels.append(train_labels[i])"""


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

	## Train network  
	model.fit(train_images, train_labels, epochs=100, batch_size=2000, validation_split = 0.1)

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
