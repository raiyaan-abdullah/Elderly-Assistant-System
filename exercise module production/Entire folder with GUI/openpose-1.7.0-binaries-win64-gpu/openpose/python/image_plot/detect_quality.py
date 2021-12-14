#import Keras library
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, Activation, Dropout, Conv2D, MaxPooling2D, Flatten, GlobalMaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.layers import LSTM, GRU, SimpleRNN, Input, Bidirectional, TimeDistributed, BatchNormalization
from tensorflow.keras.layers import RandomFlip, RandomRotation, RandomZoom, RandomTranslation, RandomHeight
from tensorflow.keras.optimizers import Adam, SGD
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from tensorflow.keras.metrics import categorical_accuracy, binary_accuracy
from tensorflow.keras import regularizers
from tensorflow.keras import applications

import cv2
import numpy as np

video_x = 224
video_y = 224

file = cv2.imread("live_record\\1.jpg")

img = cv2.resize(file, (video_x,video_y))
img = np.reshape(img, (1,video_x,video_y,3))
model = load_model("exercise_quality_2_9x_efficientnet.hdf5")
print(model.predict(img))
