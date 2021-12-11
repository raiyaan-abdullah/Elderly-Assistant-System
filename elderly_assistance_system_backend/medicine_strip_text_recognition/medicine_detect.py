# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 21:52:32 2021

@author: Raiyaan Abdullah
"""

import csv
from word_generate import train_data_generate 
import numpy as np
import tensorflow as tf

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

from tensorflow.keras.models import load_model

#define char and medicine list
char_list = [' ', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','+','(',')',',','-','[',']','%','/','&','.','\'']

char_list_size = len(char_list)

word_length = 80

medicine_list=[]
companies=["shortlist_new.csv"]
for company in companies:
    with open(company) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            medicine_list.append(row[0].lower())

med_list_size = len(medicine_list)

char_to_index = {x: i for i, x in enumerate(char_list)}


input_name="brod"   

input_name=input_name.lower()         
input_X= np.zeros((1,word_length , char_list_size))

for i, char in enumerate(input_name):
    input_X[0, i, char_to_index[char]] = 1
        
model= load_model("shortlist_checkpoints\medicine_name_predict.30-0.06.hdf5")
prediction = model.predict(input_X)
print(np.max(prediction))
pred_index=np.argmax(prediction)
print(medicine_list[pred_index])