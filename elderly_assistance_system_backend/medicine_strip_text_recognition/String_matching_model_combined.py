# -*- coding: utf-8 -*-
"""
Created on Mon May  3 02:32:51 2021

@author: Riad
"""

import csv
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
from word_generator_from_ocr_text import ngrams
from String_matching import string_matching_score
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


model= load_model("../medicine_name_predict.h5")
medicine_counts_model=[]

for med in medicine_list:
    medicine_counts_model.append(0)
ocr_text = "NanaNava"
#print(medicine_list)
for med in medicine_list:
    n=len(med)
    wordlist=ngrams(ocr_text.lower(),n)
    for word in wordlist:
        input_X= np.zeros((1,word_length , char_list_size))
        #print(word)
        for i, char in enumerate(word.lower()):
            input_X[0, i, char_to_index[char]] = 1
        prediction = model.predict(input_X)
        #print(np.max(prediction))
        pred=np.max(prediction)
        pred_index=np.argmax(prediction)
        predicted_med= medicine_list[pred_index]
        med_index=medicine_list.index(predicted_med)
        medicine_counts_model[med_index]=round(medicine_counts_model[med_index]+pred,2)

model_output=medicine_counts_model
string_matching_output= string_matching_score(medicine_list,ocr_text)
print("Output Score from model:         ",model_output)
print("Output Score from string matching: ",string_matching_output)
model_output_array=np.array(model_output)
string_matching_output_array=np.array(string_matching_output)
combined_score=0.7*model_output_array+0.3*string_matching_output_array
