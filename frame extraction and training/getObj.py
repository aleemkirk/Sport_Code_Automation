#get objects from the extracted frames using the .csv annotation files.
import cv2
import numpy as np
import csv
import ast

img = cv2.imread("video_frames/frame0.jpg")
shape = img.shape #storing image shape
dim_x = 28 #value of new image dimention
dim_y = 28 #value of new image dimention
dim = (dim_x, dim_y)
cnt = 0 # counter used to image storing/nameing purposes
annotation_path = "video_frames/video_annotations.csv" #path to frame annotations
frames_path = "video_frames/" #path to frames

with open(annotation_path) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        try:
            this_dict = ast.literal_eval(row[5]) #convert string to dict
            label_dict = ast.literal_eval(row[6])                
            if "name" in this_dict: #if the frame is annotated extract the objects
                image_name = row[0] #get image name with annotations
                label = label_dict["name"] #get object label
                img = cv2.imread(frames_path + image_name)
                x = int(this_dict['x'])
                y = int(this_dict['y'])
                width = int(this_dict['width'])
                height = int(this_dict['height'])
                obj = img[y:y+height, x:x+width]
                resized_img = cv2.resize(obj, dim)
                path = label + '/' +'img_'+str(cnt)+'.jpg'
                cv2.imwrite(path, resized_img)   #writing new image to specified path
                print(path)
                cnt += 1
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
        except:
            continue