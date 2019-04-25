import cv2 as cv2
import numpy as np


vid = cv2.VideoCapture("video.mp4")
suc, img = vid.read()
count = 0
while suc:
    cv2.imwrite("video_frames/frame%d.jpg" % count, img)
    suc, img = vid.read()
    print("Read a new frame", suc)
    count += 1
