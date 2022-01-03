# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 02:55:36 2021

@author: Riad
"""

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow
import os
from main_code import main_code_thread
import schedule
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import pyqtSignal, Qt


class firstpage(QMainWindow):
    def __init__(self):
        super(firstpage,self).__init__()
        loadUi('main_page.ui',self)
        im1 = QtGui.QMovie('image4.jpg')

        self.img1.setMovie(im1)
        self.img1.setAlignment(Qt.AlignCenter)
        #self.img1.setScaledContents(True)
        im1.start()

        im2 = QtGui.QMovie('image3.jpg')

        self.img2.setMovie(im2)
        self.img2.setAlignment(Qt.AlignCenter)
        #self.img2.setScaledContents(True)
        im2.start()
        
        #timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.onTimeout)
        #timer.start(10) # 10 milliseconds
        #self.stop.clicked.connect(timer.stop)
        self.start.clicked.connect(self.showfun)
        #self.stop.clicked.connect(timer.stop)
        
    # def onTimeout(self):
    #     #schedule.every(5).seconds.do(medicine_code)
    #     medicine_code()
    #     self.totaluser.setText("Program Started")
        
    def showfun(self):
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.onTimeout)
        # timer.start(10) # 10 milliseconds
        # self.stop.clicked.connect(timer.stop)
        # self.stop.clicked.connect(self.Stop)
        sec_page=secondPage()
        widget.addWidget(sec_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
        #schedule.every(5).seconds.do(medicine_code)
        #text=medicine_code()
        #self.totaluser.setText(text)
    def Stop(self):
        #schedule.every(5).seconds.do(medicine_code)
        self.totaluser.setText("Program Stopped")

class secondPage(QMainWindow):
    def __init__(self):
        super(secondPage, self).__init__()
        global messages
        loadUi('second_page.ui', self)
        print("Loaded")
        self.thread= main_code_thread()
        self.thread.start()
        self.thread.status.connect(self.print_message)
        '''with open('message.txt', 'r') as f:
            messages=f.read()
            f.close()
        if messages=="Wrong time for medication":
            self.drawer.setText("                      None")
        self.status.setText("       "+messages)'''
        #print(messages)
    def print_message(self,val):
        st=val
        self.status.setText("Status: \n"+ st.message)
        self.drawer.setText("                                   Drawer No:"+st.drawer_no)

    

app=QApplication(sys.argv)
page=firstpage()
widget=QtWidgets.QStackedWidget()
widget.addWidget(page)
#widget.setFixedHeight(600)
#widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')