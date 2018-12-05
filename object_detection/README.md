# Python script to create active v. non active behavior pie chart for a video sample
This script takes in a video and catergorizes what the animal behavior is active or not active. It records the time for each behavior catergory and at the end of the video generates a pie chart that shows the breakdown of the animal's behavior for that video clip. The pie chart is then saved into the django app's static folder.

To following is a sample command to run the script on a video clip in the zebra folder
`python detector/motion_detector.py --video detector/zebra/mark_bedroom.avi`