# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 00:07:25 2021

@author: Raiyaan Abdullah
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
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


import pandas as pd
import csv
import numpy as np

import datetime
import cv2


# demonstration of calculating metrics for a neural network model using sklearn
from sklearn.utils import shuffle
from sklearn.datasets import make_circles
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix


video_x = 224
video_y = 224

#import Keras library
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.layers import LSTM, GRU, SimpleRNN, Input, Bidirectional, TimeDistributed, BatchNormalization
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from tensorflow.keras.metrics import categorical_accuracy, binary_accuracy
from tensorflow.keras import regularizers




#taking train data

good_data_location = 'D:/Github Projects/Elderly-Assistance-System/elderly_assistance_system/exercise_module/image_plot/arm_movement_good'
bad_data_location = 'D:/Github Projects/Elderly-Assistance-System/elderly_assistance_system/exercise_module/image_plot/arm_movement_bad'

total_videos = len(os.listdir(good_data_location)) + len(os.listdir(bad_data_location))

X=np.zeros((total_videos , video_y, video_x, 3))   
Y=np.zeros((total_videos, 1))  


read_counter = 0

#need to make two identical for-loops into one later

#putting correct exercise data into array

for file in os.listdir(good_data_location):
    file = cv2.imread(os.path.join(good_data_location, file))
    img = cv2.resize(file, (video_x,video_y))
    '''
    cv2.imshow("view",img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys
    '''

    X[read_counter,:,:,:] = img[:,:,:]
    Y[read_counter] = 0
    read_counter = read_counter+1


#putting incorrect exercise data into array

for file in os.listdir(bad_data_location):
    file = cv2.imread(os.path.join(bad_data_location, file))
    img = cv2.resize(file, (video_x,video_y))
    '''
    cv2.imshow("view",img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys
    '''
    X[read_counter,:,:,:] = img[:,:,:]
    Y[read_counter] = 1
    read_counter = read_counter+1

    
#taking test data
good_data_location = 'D:/Github Projects/Elderly-Assistance-System/elderly_assistance_system/exercise_module/image_plot/test/good'
bad_data_location = 'D:/Github Projects/Elderly-Assistance-System/elderly_assistance_system/exercise_module/image_plot/test/bad'

total_videos = len(os.listdir(good_data_location)) + len(os.listdir(bad_data_location))

test_X=np.zeros((total_videos , video_y, video_x, 3))   
test_Y=np.zeros((total_videos, 1))  


read_counter = 0

#need to make two identical for-loops into one later

#putting correct exercise data into array

for file in os.listdir(good_data_location):
    file = cv2.imread(os.path.join(good_data_location, file))
    img = cv2.resize(file, (video_x,video_y))
    '''
    cv2.imshow("view",img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys
    '''

    test_X[read_counter,:,:,:] = img[:,:,:]
    test_Y[read_counter] = 0
    read_counter = read_counter+1


#putting incorrect exercise data into array

for file in os.listdir(bad_data_location):
    file = cv2.imread(os.path.join(bad_data_location, file))
    img = cv2.resize(file, (video_x,video_y))
    '''
    cv2.imshow("view",img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys
    '''
    test_X[read_counter,:,:,:] = img[:,:,:]
    test_Y[read_counter] = 1
    read_counter = read_counter+1



#training        
X, Y = shuffle(X, Y)

#to view tensorboard data run in the folder : tensorboard --logdir logs/fit

log_dir="logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
filepath="D:/Github Projects/Elderly-Assistance-System/elderly_assistance_system/exercise_module/image_plot/trained_models/ex_1b/2x/exercise_predict_1b_2x.{epoch:02d}-{val_loss:.2f}.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, save_best_only=True, verbose=1)


print("Training on ",len(X)," Video data")



# define cnn model
def define_model(video_y , video_x):
    model = Sequential()
 
    model.add(Conv2D(64, (7, 7), activation='relu',input_shape=(video_y , video_x, 3))) #64 (3,3) for exercise 1a
    model.add(BatchNormalization())
    model.add(MaxPooling2D((9, 9)))
    
    '''
    model.add(Conv2D(16, (5, 5), activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((5, 5)))
    '''

    model.add(Flatten())
    
    model.add(Dropout(0.5)) #0.3 for 1a
    
    model.add(Dense(64, kernel_regularizer=regularizers.l1_l2(l1=1e-4, l2=1e-3), activation='relu')) #64 for 1a
    model.add(Dropout(0.3)) #0.3 for 1a
    model.add(BatchNormalization())
    
    model.add(Dense(16, kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4), activation='relu'))
    model.add(BatchNormalization())
    model.add(Dense(2, activation='softmax'))
	# compile model
    opt = Adam(learning_rate=0.0002) #.0005 for ex 1a 
    model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

#model and parameters


model = define_model( video_y , video_x)
model.summary()

batch_size = 64
num_epochs = 150 # number of epochs

#callbacks=[EarlyStopping(patience=4, monitor='val_loss'),



#callbacks=[ModelCheckpoint(filepath=file_path, monitor='val_loss', verbose=1, mode='auto', period=2),tensorboard_callback]
callbacks=[tensorboard_callback,checkpoint]
#fit the model
history = model.fit(X, Y,
                 batch_size=batch_size,
                 shuffle=True,
                 epochs=num_epochs,
                 callbacks=callbacks,
                 validation_split=0.3)

#save the model
model.save("exercise_quality_1b_2x.hdf5")

#evaluation
print("Test results:")
test_loss, test_acc = model.evaluate(test_X,  test_Y, verbose=1)

#other matrics
# predict probabilities for test set
yhat_probs = model.predict(test_X, verbose=1)
# predict crisp classes for test set
yhat_classes = np.argmax(yhat_probs,axis=1)



# accuracy: (tp + tn) / (p + n)
accuracy = accuracy_score(test_Y, yhat_classes)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(test_Y, yhat_classes)
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(test_Y, yhat_classes)
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(test_Y, yhat_classes)
print('F1 score: %f' % f1)
# confusion matrix
matrix = confusion_matrix(test_Y, yhat_classes)
print("Confusion matrix:")
print(matrix)


'''
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
'''