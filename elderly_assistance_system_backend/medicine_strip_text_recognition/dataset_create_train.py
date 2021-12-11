# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 00:07:25 2021

@author: Raiyaan Abdullah
"""

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

import os
#WARNING: this chdir line is dangerous, need to rethink approach
os.chdir('D:/Github Projects/Elderly-Assistance-System/elderly_assistance_system/elderly_assistance_system_backend/medicine_strip_text_recognition')

from word_generate import train_data_generate 
import pandas as pd
import csv
import numpy as np
from sklearn.utils import shuffle
import datetime


#import Keras library
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.layers import LSTM, Input, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from tensorflow.keras.metrics import categorical_accuracy

#to view tensorboard data run in the folder : tensorboard --logdir logs/fit

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)



#define char and medicine list
char_list = [' ', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','+','(',')',',','-','[',']','%','/','&','.','\'']

char_list_size = len(char_list)

word_length = 80

medicine_list=[]
companies=["medicine_list.csv"]
for company in companies:
    with open(company) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            medicine_list.append(row[0].lower())

med_list_size = len(medicine_list)

#create random wrong names from medicine list

input_list=[]
target_list=[]
for index,medicine in enumerate(medicine_list):
    wrong_detection = train_data_generate(medicine)
    for data in wrong_detection:
        #print(index,' ',medicine)
        input_list.append(data)
        target_list.append(index)

char_to_index = {x: i for i, x in enumerate(char_list)}
medicine_to_index = {x: i for i, x in enumerate(medicine_list)}
   
#make X and Y with one hot encoded vectors
X=np.zeros((len(input_list), word_length , char_list_size))   
Y=np.zeros((len(input_list), med_list_size))        

for i, medicine in enumerate(input_list):
    for t, char in enumerate(medicine):
        X[i, t, char_to_index[char]] = 1
        Y[i, target_list[i]] = 1
        
X, Y = shuffle(X, Y)

print("Training on ",len(X)," Medicine")



def bidirectional_lstm_model( word_length , char_list_size):
    print('Build LSTM model.')
    model = Sequential()
    model.add(Bidirectional(LSTM(rnn_size, activation="relu"),input_shape=(word_length, char_list_size)))
    model.add(Dropout(0.6))
    model.add(Dense(med_list_size))
    model.add(Activation('softmax'))
    
    optimizer = Adam(lr=learning_rate)
    #callbacks=[EarlyStopping(patience=2, monitor='val_loss')]
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=[categorical_accuracy])
    print("model built!")
    return model

#model and parameters
rnn_size = 256 # size of RNN
learning_rate = 0.001 #learning rate

model = bidirectional_lstm_model( word_length , char_list_size)
model.summary()

batch_size = 32 # minibatch size
num_epochs = 20 # number of epochs
import shutil
#callbacks=[EarlyStopping(patience=4, monitor='val_loss'),
delete_path="shortlist_checkpoints"
file_path="shortlist_checkpoints/medicine_name_predict.{epoch:02d}-{val_loss:.2f}.hdf5"
#shutil.rmtree(delete_path)
callbacks=[ModelCheckpoint(filepath=file_path, monitor='val_loss', verbose=1, mode='auto', period=2),tensorboard_callback]
#fit the model
history = model.fit(X, Y,
                 batch_size=batch_size,
                 shuffle=True,
                 epochs=num_epochs,
                 callbacks=callbacks,
                 validation_split=0.1)

#save the model
model.save("medicine_name_predict.h5")

import matplotlib.pyplot as plt
import numpy as np

N = num_epochs
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), history.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), history.history["val_loss"], label="val_loss")

plt.title("Loss on Training Set")
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.legend(loc="upper right")
plt.figure()
plt.plot(np.arange(0, N), history.history["categorical_accuracy"], label="categorical_accuracy")
plt.plot(np.arange(0, N), history.history["val_categorical_accuracy"], label="val_categorical_accuracy")
plt.title("Accuracy on Training Set")
plt.xlabel("Epoch #")
plt.ylabel("Accuracy")
plt.legend(loc="lower right")