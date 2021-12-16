# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 03:23:27 2020

@author: Raiyaan Abdullah
"""

import Augmentor
import cv2 
import os 
import numpy as np 
from random import shuffle 
from tqdm import tqdm 

MAIN_LOCATION = 'D:\Github Projects\Elderly-Assistance-System\exercise_module'

# Creating an empty list where we should store the training data 
# after a little preprocessing of the data 
data = [] 

# tqdm is only used for interactive loading 
# loading the training data 

def augment_images(extra_number_of_images, folder_location):

    p = Augmentor.Pipeline(source_directory=folder_location, output_directory='')
    p.rotate(probability=0.8, max_left_rotation=10, max_right_rotation=10)
    p.zoom(probability=0.2, min_factor=1.1, max_factor=1.5)
    #p.skew_tilt(probability=0.2,magnitude=0.2)
    #p.random_brightness(probability=0.9,min_factor=0.8,max_factor=1.3)
    #p.random_contrast(probability=0.9,min_factor=0.5,max_factor=1.5)
    
    p.sample(extra_number_of_images)

def count_files(folder):
    list = os.listdir(folder) # dir is your directory path
    number_files = len(list)
    return number_files

train_good_no = count_files(MAIN_LOCATION+'\\train\good')
train_bad_no = count_files(MAIN_LOCATION+'\\train\\bad')

total = train_good_no + train_bad_no


augment_images(train_bad_no+total*3 ,MAIN_LOCATION+'\\train\good')
augment_images(train_good_no+total*3 ,MAIN_LOCATION+'\\train\\bad')

augment_images(50, MAIN_LOCATION+'\\val\good')
augment_images(50, MAIN_LOCATION+'\\val\\bad')
augment_images(50, MAIN_LOCATION+'\\test\good')
augment_images(50, MAIN_LOCATION+'\\test\\bad')