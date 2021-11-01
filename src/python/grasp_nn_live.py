import numpy as np
import cv2
import tensorflow as tf
import struct
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Activation
from keras.models import load_model
import matplotlib.pyplot as plt
import time


def main():

	dims = (15,15) 

	# Loads the weights
	checkpoint_path = '/home/nm/FPGA_AI/src/python/grasp_nn/grasp_nn_model.h5'
	model = load_model(checkpoint_path)
	
	# Opens the inbuilt camera to capture video.
	cap = cv2.VideoCapture(0)

	plt.ion()
	zeros = np.zeros(dims)
	ones = zeros + 1
	fig1, ax1 = plt.subplots()
	axim1 = ax1.imshow(zeros, cmap='gray', vmin=0, vmax=255)


	while(cap.isOpened()):
		ret, frame = cap.read()
		 
		# This condition prevents from infinite looping incase video ends.
		if ret == False:
			break
			
		# Run inference on grabbed frame
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		img = cv2.resize(gray, dims, interpolation = cv2.INTER_AREA)	# resize img to fit dims
		zeros = img
		
		x = np.array([img / 255]).astype('float32')
		x = np.expand_dims(x, axis=0)
		result = np.argmax(model.predict(x))
		openness = ['open','closed', 'nothing']
		print("NN Prediction: ", openness[result])

		axim1.set_data(img)
		fig1.canvas.flush_events()


	cap.release()
	cv2.destroyAllWindows()

	
if __name__=="__main__":
    main()
