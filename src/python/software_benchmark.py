import serial
import os
import random
import cv2
import numpy as np
import struct
import time
import sys
def main():
	args = sys.argv[1:]
	if len(args) == 2 and args[0] == '-port':
		port = str(args[1])	

	# define serial connection
	ser = serial.Serial(port, 115200, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)

	while 1:
		nn_res = ""
		while "time" not in nn_res: # check if nn output received
			nn_res = ser.readline().decode('UTF-8') # decode received bytes
			
		print(nn_res)
	
	
if __name__=="__main__":
    main()
