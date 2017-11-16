#! /usr/bin/env python

########################################################################
# This code takes a video file (VF) from a  folder as the first argument
# and a name (NAME) as the second argument.
# It code checks whether the folder with the NAME exists.
# If yes, the VF is copied to the folder NAME
# If no, a new folder NAME is created and the VF is copied there
# The VF is renamed in the format of randomnumbers_NAME.mp4
########################################################################

import sys
import os
#import cv2
import time
from shutil import copyfile

# Get the video file (VF) path from the first argument
vf_path = sys.argv[1]
# Get the label from the second argument
label = str(sys.argv[2])

if ' ' in label:
    label = label.replace(" ", "_")

vf_filename = os.path.basename(vf_path)
# where this file lives
dir_path = os.path.dirname(os.path.realpath(__file__))
# the label directory
label_dir_path_vid = os.path.join(dir_path, (str(label) + '_vid'))
label_dir_path_img = os.path.join(dir_path, (str(label) + '_img'))
# where we want to move the file
dest_vid = os.path.join(label_dir_path_vid, vf_filename)
dest_img = os.path.join(label_dir_path_img, vf_filename)

if os.path.isdir(label_dir_path_vid):
    os.rename(vf_path, dest_vid)
    print ("Success: ")
else:
    os.mkdir(label_dir_path_vid)
    print ("Folder Created")
    os.rename(vf_path, dest_vid)
    print ("File moved")

#Checking the current working directory and creating a list with all the folders inside
#Assumes there are only .py files and folders inside the CWD
print ("CWD: " + os.getcwd())
filelist = []
for _item in os.listdir(os.getcwd()):
    if os.path.isdir(_item):
        filelist += [_item]
print ("List of all folders: " + str(filelist))

#function for extracting images from videos at fixed fps
#This function expects a video file (in .mp4 format) as an input
def apply_v2i(file):
    vidcap = cv2.VideoCapture(file)
    count = 0
    j_count = 0
    success = True
    while success and count < 5000:
        # vidcap.read() reads frames one by one from the file
        # for a 10 second video at 30 fps there are 300 total frames
        success, image = vidcap.read()
        # for 30 fps, the approach below gives 5 images for every second.
        if count == j_count * 6:
            j_count += 1
            print 'Read a new frame: ', success
            cv2.imwrite(str(file).replace(".mp4", "_") + "frame%d.jpg" % j_count, image)  # save frame as JPEG file
            print j_count
        count += 1
    return

# For all new video files in the current working directory, this function applies apply_v2i,
# and renames the video files to append _old.mp4 to the end of the name
def v2i_and_rename():
    for file in os.listdir(os.getcwd()):
        if file.endswith(".mp4") and not file.endswith("_old.mp4"):
            #print(file)
            apply_v2i(file)
            newname = str(file).replace(".mp4", "_old.mp4")
            #print(newname)
            os.rename(file, newname)
    return

# For all directories in the CWD apply v2i_and_rename()
# for _dir in filelist:
#     os.chdir(_dir)
#     v2i_and_rename()
#     os.chdir('/home/e29298/PycharmProjects/ImagePrep/Video2Images/')

#Removes empty files in current directory
def remove_empty():
    for file in os.listdir(os.getcwd()):
        #print str(file) + str(" = ") + str(round(os.path.getsize(file) / 1000000.0,1)) + " MB"
        if round(os.path.getsize(file) / 1000000.0,1) < 0.01:
            print "The file: " + str(file) + " was smaller than 10kB and was be removed"
            os.remove(file)
    return

#Removes files that are not jpg or jpeg
def remove_non_image():
    for file in os.listdir(os.getcwd()):
        #print str(file) + str(" = ") + str(round(os.path.getsize(file) / 1000000.0,1)) + " MB"
        if not (file.endswith(".jpeg") or file.endswith(".jpg")):
            print "The file: " + str(file) + " was not a jpg or jpeg file and was removed"
            os.remove(file)
    return

#Remove empty files from all directories and print files that were removed
# for _dir in filelist:
#     os.chdir(_dir)
#     remove_empty()
#     remove_non_image()
#     os.chdir('/home/e29298/PycharmProjects/ImagePrep/Video2Images/')

def db_stats():
    for _dir in filelist:
        os.chdir(_dir)
        num_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
        print str(_dir) + " " + str(num_files)
        os.chdir('/home/e29298/PycharmProjects/ImagePrep/Video2Images/')
    return

#db_stats()
