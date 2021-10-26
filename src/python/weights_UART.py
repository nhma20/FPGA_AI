import serial
import os
import random
import cv2
import numpy as np
import struct
import time

dims = (10,10) # dimensions of images to train/test with

randomint = random.randrange(10)
read_dir = os.path.expanduser("~") + '/Downloads/MNIST_Dataset_JPG/MNIST_JPG_testing/' + str(randomint) + '/'
read_file = random.choice(os.listdir(read_dir)) # choose random test image
img = cv2.imread(os.path.join(read_dir,read_file),0) # read img as grayscale
img = cv2.resize(img, dims, interpolation = cv2.INTER_AREA)	# resize img to fit dims
img = np.asarray((img / 255)).astype('float32')
print("Label: ", str(randomint), " Filename: ", read_file) # print test image label
# define serial connection
ser = serial.Serial('/dev/ttyUSB1', 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

for i in range(dims[1]):
	for j in range(dims[0]):
		values = bytearray(struct.pack("f", img[i][j])) # turn pixel values into bytearray
		#print([ "0x%02x" % b for b in values ])
		ser.write(values) # send bytearray over UART
		#time.sleep(0.001)

quit()

