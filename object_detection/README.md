# Python script to create active v. non active behavior pie chart for a video sample
This script takes in a video and catergorizes what the animal behavior is active or not active.

To run this script go to the object detection folder: 
1. Add the video you want to detect motion in to the folder test_videos in object_detection
2. Add a folder to the frames folder in object_detection with the same name as the video you added
    1. ex: if you had a video called mark_room.mp4, create a folder called mark_room
3. run the command on your terminal  python video_to_frames.py --video test_videos/the video you want to change
    1. You will need to cd into the folder where this file is held, to cd animal-detection > cd object_detection
4. Navigate to the file object_detection_script.py in the object_detection folder
    1. Change the PATH_TO_TEST_IMAGES_DIR to = frames/ the folder you created in step 2
    2. run python object_detection_script.py
