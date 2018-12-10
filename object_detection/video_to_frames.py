# starter code from tutorial: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# import the necessary packages
from imutils.video import VideoStream
import argparse
import csv
import cv2 as cv
import imutils
import numpy as np
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

frameCount = 0 # variable used to keep track of which frame we are on
FRAMES_DIR = 'frames/' + str(args["video"].split('/')[-1].split('.')[0]) + "/" # folder where frames will be saved
 
# TODO: will not need since we will not read from webcam, maybe security cams in future
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
 
# otherwise, we are reading from a video file
else:
	vs = cv.VideoCapture(args["video"])

# initaliaze the current status of the animal
status = "Not active"

with open('../sandiegozoo/static/animal_activity_data.csv', mode='w') as data_file:
	data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	data_writer.writerow(['file_name', 'millis'])

	# loop over the frames of the video
	while True:
		# grab the current frame and initialize the occupied/unoccupied text
		frame = vs.read()
		frame = frame if args.get("video", None) is None else frame[1]
	 
		# if the frame could not be grabbed, then we have reached the end of the video
		if frame is None:
			break 
		# if there is a frame then we update the frame count
		else:
			frameCount += 1 

		# save current time in milliseconds
		millisNum = int(round(time.time() * 1000))

		# save frame in frames folder and write info to csv file
		filename = FRAMES_DIR + str(frameCount) + ".png"
		# print(filename)
		cv.imwrite(filename, frame) # save frame to 
		data_writer.writerow([filename, millisNum])

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv.destroyAllWindows()
