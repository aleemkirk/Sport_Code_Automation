#testing the lucas kanade function on a video
import numpy as np 
import cv2
import matplotlib
import argparse
from LK import lucas_kanade, compute_flow_map, compute_heat_map, compute_phase_map


#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", '--video', help='path to video')
args = vars(ap.parse_args()) #get the args

#if vid arg is none, the read from the webcam
if args.get("video", None) is None:
    cap = cv2.VideoCapture(0)
#else get the video at the specified path
else:
    cap = cv2.VideoCapture(args["video"])

firstFrame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("flow map", cv2.WINDOW_NORMAL)
cv2.namedWindow("heat map", cv2.WINDOW_NORMAL)
cv2.namedWindow("phase map", cv2.WINDOW_NORMAL)
current_frame = firstFrame
previous_frame = current_frame
np.set_printoptions(threshold=np.inf)

while True:

    ret, frame = cap.read()

    if ret == True:
        
        cv2.imshow('frame',frame)

        #finding the optical flow between two consecutive frames 
        u, v = lucas_kanade(current_frame, previous_frame, 9)
        flow_map = compute_flow_map(u, v)
        #heat_map = compute_heat_map(u, v, 3)
        phase_map = compute_phase_map(u, v)

        cv2.imshow('flow map', flow_map.astype(firstFrame.dtype))
        #cv2.imshow('heat map', heat_map.astype(firstFrame.dtype))
        cv2.imshow('phase map', phase_map)

        #update the previous and current frames 
        previous_frame = current_frame  
        current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
