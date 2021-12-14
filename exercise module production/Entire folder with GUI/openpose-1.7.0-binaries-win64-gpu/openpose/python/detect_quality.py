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
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
import glob
class detect_Thread(QThread):
    detection_status = pyqtSignal(list)
    scores=[]
    '''file1 = open("model_name.txt", "r")

    # \n is placed to indicate EOL (End of Line)
    name = file1.read()
    # file1.writelines(L)
    file1.close()'''
    '''modelName="exercise_quality_"+str(name)
    model_files = glob.glob('image_plot/*')
    # path = os.path.join("../../movenet/live_json", "1")
    #model = load_model("image_plot/exercise_quality_2_5x_resnet.hdf5")
    # print(files)
    for f in model_files:
        if modelName in f:
            print(f)
            model = load_model(f)
            break'''
    model=None

    video_x = 224
    video_y = 224
    def run(self):
        print("Detecting quality")
        file1 = open("model_name.txt", "r")

        # \n is placed to indicate EOL (End of Line)
        name = file1.read()
        # file1.writelines(L)
        file1.close()
        modelName = "exercise_quality_" + str(name)
        model_files = glob.glob('image_plot/*')
        # path = os.path.join("../../movenet/live_json", "1")
        # model = load_model("image_plot/exercise_quality_2_5x_resnet.hdf5")
        # print(files)
        for f in model_files:
            if modelName in f:
                print(f)
                self.model = load_model(f)
                break
        files = glob.glob('image_plot/live_record/*')
        #path = os.path.join("../../movenet/live_json", "1")
        # print(files)
        for f in files:
            print(f)

            file = cv2.imread(f)

            img = cv2.resize(file, (self.video_x,self.video_y))
            img = np.reshape(img, (1,self.video_x,self.video_y,3))

            self.scores.append(self.model.predict(img))

        self.detection_status.emit(self.scores)
