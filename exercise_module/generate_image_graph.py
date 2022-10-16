# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import json
import pandas as pd
import imageio
import glob


video_x=1280
video_y=720

#colors bgr
blue = (255, 0, 0)  
green = (0, 255, 0)
red = (0, 0, 255)
orange = (0, 165, 255)
yellow = (0,255,255) 

# Iterating through the json and saving x,y and probability values in dict
def get_keypoints(json_file):
    f = open(json_file,)
    data = json.load(f)
    joint_names=['head','chest','r_shoulder','r_elbow','r_hand','l_shoulder','l_elbow','l_hand','abdomen','r_hip','r_knee','r_ankle','l_hip','l_knee','l_ankle','r_eye','l_eye','r_ear','l_ear','l_feet','l_toe','l_heel','r_feet','r_toe','r_heel']
    #print(data)
    keypoints=data['people'][0]['pose_keypoints_2d']
    
    keypoints_dict={}
    
    for i in range(0,25):
        
        #print(joint_names[i],"- X:",keypoints[i*3],"- Y:",keypoints[i*3+1],"- P:",keypoints[i*3+2])
        keypoints_dict[joint_names[i]]={"X":keypoints[i*3],"Y":keypoints[i*3+1]}
        #keypoints_dict[joint_names[i]]={"X":keypoints[i*3],"Y":keypoints[i*3+1],"P":keypoints[i*3+2]}
    return keypoints_dict 


#store x,y position and angle value of important body keypoints for exercise 1 (which mostly involves hand)

def drawline_from_point_list(image,points,joint_name):
    '''
    if joint_name == "l_elbow_X" or joint_name == "r_elbow_X" or joint_name == "l_wrist_X" or joint_name == "r_wrist_X":
        # Red color in RGB
        color = red
    else:
        # Green color in RGB
        color = green
    '''

    count=0
    # Line thickness of 1 px
    thickness = 4
    
    for point in points:
        if point[0] > 320 and point[0] < 960: #checking for outlier points
            if count==0:
                start_point=point
                count=count+1
            else:
                end_point=point

                #if both increase
                if end_point[0] > start_point[0] and end_point[1] > start_point[1]:
                    color = red
                #if x increases
                elif end_point[0] > start_point[0] and end_point[1] <= start_point[1]:
                    color = green
                #if y increases
                elif end_point[0] <= start_point[0] and end_point[1] > start_point[1]:
                    color = orange
                #if both decrease
                else:
                    color = yellow


                image = cv2.line(image, (int(start_point[0]),int(start_point[1])), (int(end_point[0]),int(end_point[1])), color, thickness)            
                
                #current end point is next start point
                start_point=end_point
    return image

def calc_vel_acc(points):
    vel = []
    acc = []
    time = 5
    prev_vel_X = 0
    prev_vel_Y = 0
    for count, point in enumerate(points):
        if count > 0 and count % 5 == 0:
            vel_X = (points[count][0] - points[count - 5][0])/time
            vel_Y = (points[count][1] - points[count - 5][1])/time
            vel_lobdhi = math.sqrt(pow(vel_X,2)+pow(vel_Y,2))
            vel.append(vel_lobdhi)
            
            
            acc_X = (vel_X - prev_vel_X)/time
            acc_Y = (vel_Y - prev_vel_Y)/time
            prev_vel_X = vel_X
            prev_vel_Y = vel_Y
            acc.append((round(acc_X, 3), round(acc_Y, 3)))
            
    print("Velocity:",max(vel))
    #print(round(acc))
            
def detect_dir(points):
    directions = []
    prev_X = 0
    prev_Y = 0
    for point in points:
        if point[0] > prev_X:
            dir_X = 1
        else:
            dir_X = -1
        if point[1] > prev_Y:
            dir_Y = 1
        else:
            dir_Y = -1
        prev_X = point[0]
        prev_Y = point[1]
        
        directions.append((dir_X, dir_Y))
            
    print(directions)
                
            
            


def colouring_halt_points(image,points):
    # Blue color in RGB
    color = blue
    count=0
    thresh=5
    radius=4
    x_difference=0
    y_difference=0
    total_difference=0
    #thickness of -1 px for filled circle
    thickness = -1
    for point in points:
        if count==0:
            start_point=point
            count=count+1
        else:
            if count<=3:
                end_point=point
                x_difference=x_difference+abs(end_point[0]-start_point[0])
                y_difference=y_difference+abs(end_point[1]-start_point[1])
                total_difference= x_difference+ y_difference
                if total_difference<=thresh:
                    image = cv2.circle(image, (int(start_point[0]),int(start_point[1])), radius, color, thickness)
                    image = cv2.circle(image, (int(end_point[0]),int(end_point[1])), radius, color, thickness)
                start_point=end_point
                count=count+1
            else:
                count=0
                x_difference=0
                y_difference=0
    
    return image

video_frames = []

def generate_frame_plot(json_files_location, output_location):
    global video_frames
    video_no=0
    per_frame=1
    
    for video_frames_folder in os.listdir(json_files_location):

    
        important_parts = ["head", "abdomen", "chest", "l_hand", "l_elbow", "l_shoulder", "r_hand", "r_elbow", "r_shoulder"]      
        
        single_video_frames_path = os.path.join(json_files_location,video_frames_folder)
        frame_no=0
        
        video_frames_header = []
        for header in important_parts:
            video_frames_header.append(header+'_X')
            video_frames_header.append(header+'_Y')
            
        video_frames= pd.DataFrame(columns = video_frames_header)

        #img = np.zeros((video_y,video_x, 3),dtype=np.uint8)
        img= 0* np.ones((video_y,video_x, 3),np.uint8)
        for frame_file in os.listdir(single_video_frames_path):

            if frame_no % per_frame == 0:
            #getting keypoints
                try:
                    all_keypoints= get_keypoints(os.path.join(single_video_frames_path,frame_file))

                    chosen_keypoints = {key: value for key, value in all_keypoints.items() if key in important_parts}
                    
                    
                    #make nested dict into single level dict by converting head:{'X':,'Y':} to head_X and head_Y for further simplicity
                    keypoints={}
                    for keypoint in chosen_keypoints:
                        keypoints[keypoint+'_X'] = chosen_keypoints[keypoint]['X']
                        keypoints[keypoint+'_Y'] = chosen_keypoints[keypoint]['Y']
                    #print(keypoints)
                    video_frames = video_frames.append(keypoints, ignore_index=True)
                except:
                    "Rejected keypoint"    
                #print("Processed frame: ",frame_no)
                frame_no = frame_no + 1
        #iterate through different bodyparts
        for i in range (0,len(video_frames_header),2):
            #print (video_frames_header[i]," ",video_frames_header[i+1])
            points = video_frames[[video_frames_header[i],video_frames_header[i+1]]].values.tolist()
            #print (points)
            img = drawline_from_point_list(img,points,video_frames_header[i])
            img = colouring_halt_points(img,points)
            #calc_vel_acc(points)
            #detect_dir(points)
            
        #print(video_frames[["head_X","head_Y"]].values.tolist())
        
        print(video_frames_folder)
        print("")
        #np.save(output_location+video_frames_folder+".npy",img)  
        cv2.imwrite(output_location+video_frames_folder+".jpg",img)
        

        video_no=video_no+1
        

files = glob.glob('good/*')
for f in files:
    os.remove(f)

files = glob.glob('bad/*')
for f in files:
    os.remove(f)                        
files = glob.glob('live_record/*')
for f in files:
    os.remove(f)  
'''                      
generate_frame_plot('Openpose variations/openpose-1.7.0-binaries-win64-gpu/openpose/python/output_json_folder/arm_movement_good/','good/')
generate_frame_plot('Openpose variations/openpose-1.7.0-binaries-win64-gpu/openpose/python/output_json_folder/arm_movement_bad/','bad/')

'''
generate_frame_plot('Openpose variations/openpose-1.7.0-binaries-win64-gpu/openpose/python/movenet/live_json/',
'live_record/')
 