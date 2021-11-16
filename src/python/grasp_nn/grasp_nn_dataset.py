import os
import cv2
 
 
openness = 5
 
# Opens the inbuilt camera of laptop to capture video.
cap = cv2.VideoCapture(0)
i = 0
 
while(cap.isOpened()):
	ret, frame = cap.read()
	 
	# This condition prevents from infinite looping
	# incase video ends.
	if ret == False:
		break
		
	# Image directory
	directory = r'/home/nm/FPGA_AI/src/python/grasp_nn/dataset/' + str(openness)
	# Change the current directory to specified directory 
	os.chdir(directory)
	# Save Frame by Frame into disk using imwrite method
	cv2.imwrite(str(i)+'.jpg', frame)
	i += 1

cap.release()
cv2.destroyAllWindows()
