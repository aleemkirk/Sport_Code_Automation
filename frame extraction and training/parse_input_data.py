#parsing the data from the .csv file to train network
import csv
import ast

annotation_path = "video_frames/video_annotations.csv" #path to frame annotations
path_prefix = "video_frames/"
writable_String = ''

with open(annotation_path) as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        try:
            this_dict = ast.literal_eval(row[5])
            label_dict = ast.literal_eval(row[6])
            if "name" in this_dict: #filter the annotated frames
                frame_name = row[0]
                frame_path = path_prefix + frame_name
                x1 = int(this_dict['x'])
                y1 = int(this_dict['y'])
                x2 = x1 + int(this_dict['width'])
                y2 = y1 + int(this_dict['height'])
                class_name = label_dict['name']
                writable_String = writable_String + frame_path + ',' + str(x1) + ',' + str(y1) + ',' + str(x2) + ',' + str(y2) + ',' + class_name + '\n'
                               
        except:
            print('didn\'t work')
            continue
        
with open("my_data.txt", "w") as text_file:
    text_file.write(writable_String)