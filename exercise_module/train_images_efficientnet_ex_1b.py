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
from tensorflow.keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten, GlobalMaxPooling2D, GlobalAveragePooling2D,Conv1D,MaxPooling1D,GlobalAveragePooling1D
from tensorflow.keras.layers import LSTM, GRU, SimpleRNN, Input, Bidirectional, TimeDistributed, BatchNormalization
from tensorflow.keras.layers import RandomFlip, RandomRotation, RandomZoom, RandomTranslation, RandomHeight
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from tensorflow.keras.metrics import categorical_accuracy, binary_accuracy
from tensorflow.keras import regularizers
from tensorflow.keras import applications
from tensorflow.keras.preprocessing import image_dataset_from_directory


train_ds = image_dataset_from_directory(
    directory='D:/Github Projects/Elderly-Assistant-System/exercise_module/data/arm_abduction_and_adduction_5x/train/',
    labels='inferred',
    label_mode='int',
    batch_size=64,
    image_size=(video_x, video_y))


#taking val data

val_good_location = 'D:/Github Projects/Elderly-Assistant-System/exercise_module/data/arm_abduction_and_adduction_5x/val/correct'
val_bad_location = 'D:/Github Projects/Elderly-Assistant-System/exercise_module/data/arm_abduction_and_adduction_5x/val/incorrect'

total_videos = len(os.listdir(val_good_location)) + len(os.listdir(val_bad_location))

val_X=np.zeros((total_videos , video_y, video_x, 3))   
val_Y=np.zeros((total_videos, 1))  


read_counter = 0

#need to make two identical for-loops into one later

#putting correct exercise data into array

for file in os.listdir(val_good_location):
    file = cv2.imread(os.path.join(val_good_location, file))
    img = cv2.resize(file, (video_x,video_y))
    '''
    cv2.imshow("view",img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys
    '''

    val_X[read_counter,:,:,:] = img[:,:,:]
    val_Y[read_counter] = 0
    read_counter = read_counter+1


#putting incorrect exercise data into array

for file in os.listdir(val_bad_location):
    file = cv2.imread(os.path.join(val_bad_location, file))
    img = cv2.resize(file, (video_x,video_y))
    '''
    cv2.imshow("view",img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys
    '''
    val_X[read_counter,:,:,:] = img[:,:,:]
    val_Y[read_counter] = 1
    read_counter = read_counter+1    


#taking test data

test_good_location = 'D:/Github Projects/Elderly-Assistant-System/exercise_module/data/arm_abduction_and_adduction_5x/test/correct'
test_bad_location = 'D:/Github Projects/Elderly-Assistant-System/exercise_module/data/arm_abduction_and_adduction_5x/test/incorrect'

total_videos = len(os.listdir(test_good_location)) + len(os.listdir(test_bad_location))

test_X=np.zeros((total_videos , video_y, video_x, 3))   
test_Y=np.zeros((total_videos, 1))  


read_counter = 0

#need to make two identical for-loops into one later

#putting correct exercise data into array

for file in os.listdir(test_good_location):
    file = cv2.imread(os.path.join(test_good_location, file))
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

for file in os.listdir(test_bad_location):
    file = cv2.imread(os.path.join(test_bad_location, file))
    img = cv2.resize(file, (video_x,video_y))
    '''
    cv2.imshow("view",img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys
    '''
    test_X[read_counter,:,:,:] = img[:,:,:]
    test_Y[read_counter] = 1
    read_counter = read_counter+1


#need to fix train, val and test data reading to one loop

#training        
#train_X, train_Y = shuffle(train_X, train_Y)


#need to fix train, val and test data reading to one loop
def preprocess(images, labels):
    return tf.keras.applications.efficientnet.preprocess_input(images), labels
train_ds = train_ds.map(preprocess)

val_X = applications.efficientnet.preprocess_input(val_X)
test_X = applications.efficientnet.preprocess_input(test_X)


#to view tensorboard data run in the folder : tensorboard --logdir logs/fit

log_dir="logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
filepath="D:/Github Projects/Elderly-Assistant-System/exercise_module/trained_models/arm_abduction_and_adduction/5x/exercise_predict_1b_5x_efficientnet.{epoch:02d}-{val_loss:.2f}.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss',save_best_only=True, verbose=1)


#print("Training on ",len(train_X)," Video data")



#Code taken from: https://github.com/keras-team/keras/issues/9214

def define_model():
    
    data_augmentation = Sequential(
    [
        RandomTranslation(height_factor=(-0.2,0.2), width_factor=0.2, fill_mode="wrap"),
        RandomHeight(factor=(-0.2, 0.3))
    ]
    )
    
    base_model = applications.EfficientNetB0(weights='imagenet', include_top=False)

    inputs = Input(shape=(224, 224, 3))
    #x = data_augmentation(inputs)
    x = base_model(inputs)
    #x = BatchNormalization()(x)
    x = Dropout(0.3)(x)
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(32, activation='relu')(x)

    #x = BatchNormalization()(x)
    predictions = Dense(2, activation='softmax')(x)
    model = Model(inputs=inputs, outputs=predictions)

    print("Number of layers in the base model: ", len(base_model.layers))

    #fine_tune_at = 165
    #for layer in base_model.layers[:fine_tune_at]:
    for layer in base_model.layers:
        layer.trainable = False
        
    opt = Adam(learning_rate=0.0001) #.0005 for ex 1b 
    model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model



model = define_model()
model.summary()


batch_size = 64
num_epochs = 100 # number of epochs

#callbacks=[EarlyStopping(patience=4, monitor='val_loss'),



#callbacks=[ModelCheckpoint(filepath=file_path, monitor='val_loss', verbose=1, mode='auto', period=2),tensorboard_callback]
callbacks=[tensorboard_callback,checkpoint]
#fit the model
history = model.fit(train_ds,
                 batch_size=batch_size,
                 shuffle=True,
                 epochs=num_epochs,
                 callbacks=callbacks,
                 validation_data=(val_X, val_Y),
                 )

#save the model
model.save("exercise_quality_1b_5x_efficientnet.hdf5")

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