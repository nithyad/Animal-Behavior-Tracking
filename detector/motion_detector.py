# starter code from tutorial: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

# import the necessary packages
from imutils.video import VideoStream
import argparse
import csv
import cv2 as cv
import datetime
import imutils
import numpy as np
import pandas as pd
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

animal = "Zebra" # TODO(amysorto): take animal as input instead of hard coding
frameCount = 0 # variable used to refresh the reference frame
REFENCE_FRAME_THRESHOLD = 60 # number represents how many frames to wait before setting a nre reference frame
# vars for deep learning object detection
prototxt = "detector/MobileNetSSD_deploy.prototxt.txt"
model = "detector/MobileNetSSD_deploy.caffemodel"
confidenceDefault = 0.2
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
net = cv.dnn.readNetFromCaffe(prototxt, model)

 
# TODO: will not need since we will not read from webcam, maybe security cams in future
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
 
# otherwise, we are reading from a video file
else:
	vs = cv.VideoCapture(args["video"])
 
# initialize the reference frame in the video stream
referenceFrame = None


# initialize varibles to store the time of active and non active behavior
activeTime = datetime.timedelta()
notActiveTime = datetime.timedelta()
lastUpdate = datetime.datetime.now()

# initaliaze the current status of the animal
status = "Not active"

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
 
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	gray = cv.GaussianBlur(gray, (21, 21), 0)
 
	# if the reference frame is None, initialize it
	if referenceFrame is None or frameCount == REFENCE_FRAME_THRESHOLD:
		referenceFrame = gray
		frameCount = 0
		continue

	# compute the absolute difference between the current frame and first frame
	frameDelta = cv.absdiff(referenceFrame, gray)
	thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv.dilate(thresh, None, iterations=2)
	cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
		cv.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
 
	# if contours exist, then we set the status to active
	if (cnts):
		activeTime += datetime.datetime.now() - lastUpdate
		lastUpdate = datetime.datetime.now()
		status = "Active"
	else:
		notActiveTime += datetime.datetime.now() - lastUpdate
		lastUpdate = datetime.datetime.now()
		status = "Not Active"

	# draw deep learning object detection boxes on the frame
	(h, w) = frame.shape[:2]
	blob = cv.dnn.blobFromImage(cv.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
	net.setInput(blob)
	detections = net.forward()
	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > confidenceDefault:
			# extract the index of the class label from the `detections`,
			# then compute the (x, y)-coordinates of the bounding box for
			# the object
			idx = int(detections[0, 0, i, 1])
			if CLASSES[idx] != "chair":
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				# print(startX, endX, startY, endY)

				# display the prediction
				label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
				print("[INFO] {}".format(label))
				cv.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)

				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv.putText(frame, label, (startX, y),
					cv.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	# draw the text and timestamp on the frame
	cv.putText(frame, "Behavior Status: {}".format(status), (10, 20),
		cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv.putText(frame, "     Active Time: " + str(activeTime),
		(10, frame.shape[0] - 20), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	cv.putText(frame, "Non Active Time: " + str(notActiveTime),
		(10, frame.shape[0] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
 
	# show the frame and record if the user presses a key
	cv.imshow(animal + " Feed", frame)
	cv.imshow("Thresh", thresh)
	cv.imshow("Frame Delta", frameDelta)
	key = cv.waitKey(1) & 0xFF
 
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv.destroyAllWindows()

# create csv to write data
with open('sandiegozoo/static/animal_activity_data.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    data_writer.writerow(['Animal', 'Active Time', 'Non Active Time'])
    # TODO(amysorto): have animal type come from 
    data_writer.writerow([animal, (activeTime.microseconds / 1000), (notActiveTime.microseconds / 1000)])

