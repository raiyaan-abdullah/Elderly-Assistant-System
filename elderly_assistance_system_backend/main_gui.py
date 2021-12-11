# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 02:55:36 2021

@author: Riad
"""

import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
import os
from main_code import medicine_code
import schedule

class firstpage(QDialog):
    def __init__(self):
        super(firstpage,self).__init__()
        loadUi('firstpage.ui',self)
        
        #timer = QtCore.QTimer(self)
        #timer.timeout.connect(self.onTimeout)
        #timer.start(10) # 10 milliseconds
        #self.stop.clicked.connect(timer.stop)
        self.showButton.clicked.connect(self.showfun)
        #self.stop.clicked.connect(timer.stop)
        
    def onTimeout(self):
        #schedule.every(5).seconds.do(medicine_code)
        medicine_code()
        self.totaluser.setText("Program Started")
        
    def showfun(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.onTimeout)
        timer.start(10) # 10 milliseconds
        self.stop.clicked.connect(timer.stop)
        self.stop.clicked.connect(self.Stop)
        
        #schedule.every(5).seconds.do(medicine_code)
        #text=medicine_code()
        #self.totaluser.setText(text)
    def Stop(self):
        #schedule.every(5).seconds.do(medicine_code)
        self.totaluser.setText("Program Stopped")


    

app=QApplication(sys.argv)
page=firstpage()
widget=QtWidgets.QStackedWidget()
widget.addWidget(page)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')