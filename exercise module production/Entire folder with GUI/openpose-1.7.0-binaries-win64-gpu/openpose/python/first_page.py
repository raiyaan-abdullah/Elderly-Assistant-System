# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first_page.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, subprocess
from PyQt5.QtCore import QThread



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(999, 686)
        MainWindow.setStyleSheet("background-color: rgb(222, 242, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.excercise_ques = QtWidgets.QLabel(self.centralwidget)
        self.excercise_ques.setStyleSheet("font: 75 24pt \"MS Shell Dlg 2\";")
        self.excercise_ques.setObjectName("excercise_ques")
        self.verticalLayout.addWidget(self.excercise_ques)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.exercise_1 = QtWidgets.QLabel(self.centralwidget)
        self.exercise_1.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.exercise_1.setObjectName("exercise_1")
        self.horizontalLayout_2.addWidget(self.exercise_1)
        self.exercise_2 = QtWidgets.QLabel(self.centralwidget)
        self.exercise_2.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";")
        self.exercise_2.setObjectName("exercise_2")
        self.horizontalLayout_2.addWidget(self.exercise_2)
        self.exercise_3 = QtWidgets.QLabel(self.centralwidget)
        self.exercise_3.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";\n"
"")
        self.exercise_3.setObjectName("exercise_3")
        self.horizontalLayout_2.addWidget(self.exercise_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.exercise_1_gif = QtWidgets.QLabel(self.centralwidget)
        self.exercise_1_gif.setObjectName("exercise_1_gif")
        self.horizontalLayout_3.addWidget(self.exercise_1_gif)
        self.exercise_2_gif = QtWidgets.QLabel(self.centralwidget)
        self.exercise_2_gif.setObjectName("exercise_2_gif")
        self.horizontalLayout_3.addWidget(self.exercise_2_gif)
        self.exercise_3_gif = QtWidgets.QLabel(self.centralwidget)
        self.exercise_3_gif.setObjectName("exercise_3_gif")
        self.horizontalLayout_3.addWidget(self.exercise_3_gif)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.exercise_1_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exercise_1_button.sizePolicy().hasHeightForWidth())
        self.exercise_1_button.setSizePolicy(sizePolicy)
        self.exercise_1_button.setStyleSheet("\n"
"QPushButton {\n"
"    font: 18pt \"MS Shell Dlg 2\";\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background-color: rgb(14, 255, 34);\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(7, 255, 119);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        self.exercise_1_button.setObjectName("exercise_1_button")
        self.horizontalLayout_4.addWidget(self.exercise_1_button)
        self.exercise_2_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exercise_2_button.sizePolicy().hasHeightForWidth())
        self.exercise_2_button.setSizePolicy(sizePolicy)
        self.exercise_2_button.setStyleSheet("\n"
"QPushButton {\n"
"    font: 18pt \"MS Shell Dlg 2\";\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background-color: rgb(14, 255, 34);\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(7, 255, 119);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        self.exercise_2_button.setObjectName("exercise_2_button")
        self.horizontalLayout_4.addWidget(self.exercise_2_button)
        self.exercise_3_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exercise_3_button.sizePolicy().hasHeightForWidth())
        self.exercise_3_button.setSizePolicy(sizePolicy)
        self.exercise_3_button.setStyleSheet("\n"
"QPushButton {\n"
"    font: 18pt \"MS Shell Dlg 2\";\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background-color: rgb(14, 255, 34);\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(7, 255, 119);\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }")
        self.exercise_3_button.setObjectName("exercise_3_button")
        self.horizontalLayout_4.addWidget(self.exercise_3_button)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Exercise Module"))
        self.excercise_ques.setText(_translate("MainWindow", "Which exercise routine do you want to perform?"))
        self.exercise_1.setText(_translate("MainWindow", "               Arm flexion and \n"
"                  extension"))
        self.exercise_2.setText(_translate("MainWindow", "               Arm abduction and\n"
"                  adduction"))
        self.exercise_3.setText(_translate("MainWindow", "               Arm lateral and medial\n"
"                 rotation"))
        self.exercise_1_gif.setScaledContents(True)
        movie1 = QtGui.QMovie('Arm flexion and extension​.gif')
        self.exercise_1_gif.setMovie(movie1)
        movie1.start()
        #displaying second exercise gui
        self.exercise_2_gif.setScaledContents(True)
        movie2 = QtGui.QMovie('Arm abduction and adduction​.gif')
        self.exercise_2_gif.setMovie(movie2)
        movie2.start()
        #displaying third exercise gui
        self.exercise_3_gif.setScaledContents(True)
        movie3 = QtGui.QMovie('Arm circumduction.gif')
        self.exercise_3_gif.setMovie(movie3)
        movie3.start()
        '''self.exercise_1_gif.setText(_translate("MainWindow", "TextLabel"))
        self.exercise_2_gif.setText(_translate("MainWindow", "TextLabel"))
        self.exercise_3_gif.setText(_translate("MainWindow", "TextLabel"))'''
        self.exercise_1_button.setText(_translate("MainWindow", "Start Exercise"))
        self.exercise_2_button.setText(_translate("MainWindow", "Start Exercise"))
        self.exercise_3_button.setText(_translate("MainWindow", "Start Exercise"))
        self.exercise_1_button.clicked.connect(self.page_call)
        #subprocess.call(['python exercise_1_page_1.py'])



    def page_call(self):
            sys.exit(0)
            subprocess.call(['python exercise_1_page_1.py'])

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
