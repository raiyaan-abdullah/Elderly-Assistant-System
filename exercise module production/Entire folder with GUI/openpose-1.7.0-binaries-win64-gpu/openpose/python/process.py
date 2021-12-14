import numpy as np
import cv2 as cv
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

class CameraThread(QThread):
    camera_status=pyqtSignal(QObject)
    def run(self):
        self.cap = cv.VideoCapture(0)
        #print(type(cap))
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            self.ret, frame = self.cap.read()
            #print(ret)
            # if frame is read correctly ret is True
            if not self.ret:
                print("Can't receive frame (stream end?). Exiting ...")
                self.camera_status.emit(self)
                break
            # Our operations on the frame come here
            self.gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            self.camera_status.emit(self)
            # Display the resulting frame
            cv.imshow('frame', self.gray)
            if cv.waitKey(1) == ord('q'):
                break
        # When everything done, release the capture
        self.cap.release()
        cv.destroyAllWindows()