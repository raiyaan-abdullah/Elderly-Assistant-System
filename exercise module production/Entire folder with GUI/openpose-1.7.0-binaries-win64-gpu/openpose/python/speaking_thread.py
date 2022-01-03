import pyttsx3


import cv2 as cv
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

class SpeakingThread(QThread):
    speak_status=pyqtSignal(QObject)
    txt=""
    def speak(self, text):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 110)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
    def run(self):
        self.speak_status.emit(self)
        self.speak(self.txt)
