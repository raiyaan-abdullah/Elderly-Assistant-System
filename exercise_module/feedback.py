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

def detect_arm_bend(image,hand,elbow,shoulder):
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
    
    #print(hand)
    #print(elbow)
    #print(shoulder)
    
    for i in range (0,len(hand)):
        x1, y1 = elbow[i][0] - hand[i][0], elbow[i][1] - hand[i][1]
        x2, y2 = shoulder[i][0] - hand[i][0], shoulder[i][1] - hand[i][1]
        
        area= abs(x1 * y2 - x2 * y1)
        #print(area)
        
        if area > 5000:
            print("Arm bended in frame ",i)
        

                
def detect_arm_horizontal(image,hand,elbow,shoulder):

    for i in range (0,len(hand)):
        diff_1 = abs(hand[i][1] - elbow[i][1])
        diff_2 = abs(elbow[i][1] - shoulder[i][1])
        total_diff = diff_1 + diff_2
        
        if total_diff <100:
            print("Arm was horizontal in frame ",i)

                
def detect_arm_vertical_deviation(image,hand,elbow,shoulder):

    for i in range (0,len(hand)):
        diff_1 = abs(hand[i][0] - elbow[i][0])
        diff_2 = abs(elbow[i][0] - shoulder[i][0])
        total_diff = diff_1 + diff_2
        
        #print (total_diff)
        
        if total_diff >100:
            print("Arm deviated horizontally in frame ",i)        
            




video_frames = []

def analyze_video(json_files_location):
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
        
        points = []
        
        for i in range (0,len(video_frames_header),2):
            
            print (video_frames_header[i]," ",video_frames_header[i+1])
            
            
            
            points.append(video_frames[[video_frames_header[i],video_frames_header[i+1]]].values.tolist())
            
            
            #print (points)
            
            #img = colouring_halt_points(img,points)
            
        #print("Left bend")
        #detect_arm_bend(img,points[3],points[4],points[5])
        print("Right bend")
        detect_arm_bend(img,points[6],points[7],points[8]) 

        #print("Left horiz")
        #detect_arm_horizontal(img,points[3],points[4],points[5])
        #print("Right horiz")
        #detect_arm_horizontal(img,points[6],points[7],points[8]) 

        #print("Left vert")
        #detect_arm_vertical_deviation(img,points[3],points[4],points[5])
        print("Right vert")
        detect_arm_vertical_deviation(img,points[6],points[7],points[8])         
        
           
        #print(video_frames[["head_X","head_Y"]].values.tolist())
        
        print(video_frames_folder)
        print("")
        #np.save(output_location+video_frames_folder+".npy",img)  

        

        video_no=video_no+1
        

                     

analyze_video('Openpose variations/openpose-1.7.0-binaries-win64-gpu/openpose/python/movenet/live_json/')
 