import tensorflow as tf
import cv2
import numpy as np
from tensorflow.keras import models
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras import applications
import os

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

directory='D:/Github Projects/Elderly-Assistant-System/exercise_module/data/arm_lateral_and_medial_rotation_7x/train/incorrect/'

model = models.load_model('exercise_quality_2_7x_resnet.hdf5')

opt = Adam(learning_rate=0.0005) #.0005 for ex 1a 
model.compile(optimizer=opt, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
 

for image in os.listdir(directory):
    img_path = os.path.join(directory, image)
    file = cv2.imread(img_path)
    
    img = cv2.resize(file, (video_x,video_y))
    img = np.reshape(img, (1,video_x,video_y,3))
    img = applications.resnet.preprocess_input(img)
    prediction = model.predict(img, verbose=0)
    '''
    if np.argmax(prediction) == 0:
        print(image+" is correct")
    '''
    if np.argmax(prediction) == 1:
        print(image+" is incorrect")



