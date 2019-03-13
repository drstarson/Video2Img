# This is the latest code for Video to Image conversion.
# It saves frames into folders named after videos and deletes videos after parsing.
# Frame extraction rate can be adjusted in the code.

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
# Path setting is required for the package to see cv2 module

import cv2
import numpy as np
import os

# Function for extracting images from videos at fixed fps
# This function expexts a video file (in .mov format) as an input


def apply_v2i(file):
    vidcap = cv2.VideoCapture(file)
    count = 0
    j_count = 0
    success = True
    while success and count < 5000:
        # vidcap.read() reads frames one by one from the file
        # for a 10 second video at 30 fps there are 300 total frames
        success, image = vidcap.read()
        # for 30 fps, the approach below gives 1 image for every second.
        if count == j_count * 30:
            j_count += 1
            img_file_name = str(file).replace(
                ".MOV", "_") + "%d.jpg" % j_count
            cv2.imwrite(img_file_name, image)  # save frame as JPEG file
            if os.path.getsize(img_file_name) > 0:
                print ('Saved frame')
            else:
                os.remove(img_file_name)
            print j_count
        count += 1
    return

# For all new video files in the current working directory, this function applies apply_v2i,
# and renames the video files to append _old.mov to the end of the name


def v2i_and_rename(target_dir):
    for file in os.listdir(target_dir):
        if file.endswith(".MOV") and not file.endswith("_old.MOV"):
            print(file)
            #new_dir_name = (target_dir + '/' + file).replace('.mov','')
            #os.system('mkdir ' + new_dir_name)
            file_path = target_dir + '/' + file
            os.system('mv ' + file_path + ' ' + 'Photos')
            new_file_path = 'Photos/' + file
            apply_v2i(new_file_path)
            #newname = str(new_file_path).replace(".mov", "_old.mov")
            # print(newname)
            os.remove(new_file_path)
    return


v2i_and_rename('Videos')
