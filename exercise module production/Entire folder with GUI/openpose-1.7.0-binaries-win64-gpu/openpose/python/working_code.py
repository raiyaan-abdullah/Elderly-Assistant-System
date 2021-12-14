import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
import os
import sys
import pyttsx3
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import time
from process import CameraThread
import cv2 as cv
from detect_quality import detect_Thread

from movenet_code_video_gui import movenet_Thread
from generate_image_graph_advanced_gui import graph_Thread

class mainpage(QMainWindow):
    def __init__(self):
        super(mainpage,self).__init__()
        loadUi('first_page.ui',self)
        self.exercise_1_gif.setScaledContents(True)

        movie1 = QtGui.QMovie('GUI GIFs/ex 1a part 1.gif')
        self.exercise_1_gif.setMovie(movie1)
        movie1.start()
        #displaying second exercise gui
        self.exercise_2_gif.setScaledContents(True)
        movie2 = QtGui.QMovie('GUI GIFs/ex 1b part 1.gif')
        self.exercise_2_gif.setMovie(movie2)
        movie2.start()
        #displaying third exercise gui
        self.exercise_3_gif.setScaledContents(True)
        movie3 = QtGui.QMovie('GUI GIFs/ex 2 part 1.gif')
        self.exercise_3_gif.setMovie(movie3)
        movie3.start()
        self.exercise_4_gif.setScaledContents(True)
        movie4 = QtGui.QMovie('GUI GIFs/ex 3 part 1.gif')
        self.exercise_4_gif.setMovie(movie4)
        movie4.start()
        self.exercise_1_button.clicked.connect(self.callex1a)
        self.exercise_2_button.clicked.connect(self.callex1b)
        self.exercise_3_button.clicked.connect(self.callex2)
        self.exercise_4_button.clicked.connect(self.callex3)
        self.camerathread_obj=None
    def callex1a(self):
        second=exercise_1a_1()
        file1 = open("model_name.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("1a")
        # file1.writelines(L)
        file1.close()
        widget.addWidget(second)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def callex1b(self):
        second=exercise_1b_1()
        file1 = open("model_name.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("1b")
        # file1.writelines(L)
        file1.close()
        widget.addWidget(second)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def callex2(self):
        second=exercise_2_1()
        file1 = open("model_name.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("2")
        # file1.writelines(L)
        file1.close()
        widget.addWidget(second)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def callex3(self):
        second=exercise_3_1()
        file1 = open("model_name.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("3")
        # file1.writelines(L)
        file1.close()
        widget.addWidget(second)
        widget.setCurrentIndex(widget.currentIndex()+1)

class TimeThread(QThread):
    timer_value=pyqtSignal(int)
    def run(self):
        for i in range(6,-1,-1):
            #print(i)
            time.sleep(1)
            self.timer_value.emit(i)
        #print(int(time.time()))
        #timer_value.emit(int(time.time()))

class exercise_1a_1(QMainWindow):
    def __init__(self):
        super(exercise_1a_1,self).__init__()
        loadUi('exercise_1_page_1.ui',self)
        movie1 = QtGui.QMovie('GUI GIFs/ex 1a part 1.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        self.startButton.clicked.connect(self.movenet_thread_call)
        file1 = open("myfile.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("0")
        # file1.writelines(L)
        file1.close()

    def movenet_thread_call(self):
        print("Camera opening...")
        self.time.setText("Please wait.. Camera opening...")
        start = time.time()
        self.TThread = TimeThread()

        self.movenetThread = movenet_Thread()

        self.movenetThread.start()
        self.movenetThread.movenet_status.connect(self.timer_thread_call)
        self.movenetThread.finished.connect(self.okay)

    
    def timer_thread_call(self,val):
        #print(val.ret)
        self.movenet_obj=val
        if val.ret==True:
            if self.TThread.isRunning() is False:
                self.TThread.start()

            self.TThread.timer_value.connect(self.timer_value_show)
            self.TThread.finished.connect(self.timeOver)
    def timer_value_show(self, val):
        self.time.setText("Time Remaining : "+str(val)+" sec")


    def timeOver(self):
        self.time.setText("                  Time Over")
        print("Time Over")
        #self.movenet_obj.cap.release()
        
        #self.movenetThread.terminate()
        #cv.destroyWindow('frame')
        

        #print("Time Over")
    def okay(self):
        print("Camera run successfully")
        self.nextpagecall()
    
    def nextpagecall(self):
        third=exercise_1a_2()
        widget.addWidget(third)
        widget.setCurrentIndex(widget.currentIndex()+1)

class exercise_1a_2(QMainWindow):
    def __init__(self):
        super(exercise_1a_2,self).__init__()
        loadUi('exercise_1_page_2.ui',self)
        movie1 = QtGui.QMovie('GUI GIFs/ex 1a part 2.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        file1 = open("myfile.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("1")
        # file1.writelines(L)
        file1.close()
        self.movenet_thread_call_again()
        #self.startButton.clicked.connect(self.camera_thread_call)

    def movenet_thread_call_again(self):
        print("Camera opening...")
        self.time.setText("Please wait.. Camera opening...")
        start = time.time()
        self.TThread = TimeThread()

        self.movenetThread = movenet_Thread()

        self.movenetThread.start()
        self.movenetThread.movenet_status.connect(self.timer_thread_call)
        self.movenetThread.finished.connect(self.okay)

    def timer_thread_call(self, val):
        # print(val.ret)
        self.movenet_obj = val
        self.movenet_obj.count = 1
        if val.ret == True:
            if self.TThread.isRunning() is False:
                self.TThread.start()

            self.TThread.timer_value.connect(self.timer_value_show)
            self.TThread.finished.connect(self.timeOver)
    def timer_value_show(self, val):
        self.time.setText("Time Remaining : "+str(val)+" sec")


    def timeOver(self):
        self.time.setText("                  Time Over")
        #elf.camerathread_obj.cap.release()
        #self.camthread.terminate()
    def okay(self):
        print("Camera run successfully")
        pro_page=Result_page()
        widget.addWidget(pro_page)
        widget.setCurrentIndex(widget.currentIndex()+1)


# for second exercise

class exercise_1b_1(QMainWindow):
    def __init__(self):
        super(exercise_1b_1, self).__init__()
        loadUi('exercise_1b_page_1.ui', self)
        movie1 = QtGui.QMovie('GUI GIFs/ex 1b part 1.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        self.startButton.clicked.connect(self.movenet_thread_call)
        file1 = open("myfile.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("0")
        # file1.writelines(L)
        file1.close()

    def movenet_thread_call(self):
        print("Camera opening...")
        self.time.setText("Please wait.. Camera opening...")
        start = time.time()
        self.TThread = TimeThread()

        self.movenetThread = movenet_Thread()

        self.movenetThread.start()
        self.movenetThread.movenet_status.connect(self.timer_thread_call)
        self.movenetThread.finished.connect(self.okay)

    def timer_thread_call(self, val):
        # print(val.ret)
        self.movenet_obj = val
        if val.ret == True:
            if self.TThread.isRunning() is False:
                self.TThread.start()

            self.TThread.timer_value.connect(self.timer_value_show)
            self.TThread.finished.connect(self.timeOver)

    def timer_value_show(self, val):
        self.time.setText("Time Remaining : " + str(val) + " sec")

    def timeOver(self):
        self.time.setText("                  Time Over")
        print("Time Over")
        # self.movenet_obj.cap.release()

        # self.movenetThread.terminate()
        # cv.destroyWindow('frame')

        # print("Time Over")

    def okay(self):
        print("Camera run successfully")
        self.nextpagecall()

    def nextpagecall(self):
        third = exercise_1b_2()
        widget.addWidget(third)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class exercise_1b_2(QMainWindow):
    def __init__(self):
        super(exercise_1b_2, self).__init__()
        loadUi('exercise_1b_page_2.ui', self)
        movie1 = QtGui.QMovie('GUI GIFs/ex 1b part 2.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        file1 = open("myfile.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("1")
        # file1.writelines(L)
        file1.close()
        self.movenet_thread_call_again()
        # self.startButton.clicked.connect(self.camera_thread_call)

    def movenet_thread_call_again(self):
        print("Camera opening...")
        self.time.setText("Please wait.. Camera opening...")
        start = time.time()
        self.TThread = TimeThread()

        self.movenetThread = movenet_Thread()

        self.movenetThread.start()
        self.movenetThread.movenet_status.connect(self.timer_thread_call)
        self.movenetThread.finished.connect(self.okay)

    def timer_thread_call(self, val):
        # print(val.ret)
        self.movenet_obj = val
        self.movenet_obj.count = 1
        if val.ret == True:
            if self.TThread.isRunning() is False:
                self.TThread.start()

            self.TThread.timer_value.connect(self.timer_value_show)
            self.TThread.finished.connect(self.timeOver)

    def timer_value_show(self, val):
        self.time.setText("Time Remaining : " + str(val) + " sec")

    def timeOver(self):
        self.time.setText("                  Time Over")
        # elf.camerathread_obj.cap.release()
        # self.camthread.terminate()

    def okay(self):
        print("Camera run successfully")
        pro_page = Result_page()
        widget.addWidget(pro_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# third exercise
class exercise_2_1(QMainWindow):
    def __init__(self):
        super(exercise_2_1, self).__init__()
        loadUi('exercise_2_page_1.ui', self)
        movie1 = QtGui.QMovie('GUI GIFs/ex 2 part 1.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        self.startButton.clicked.connect(self.movenet_thread_call)
        file1 = open("myfile.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("0")
        # file1.writelines(L)
        file1.close()

    def movenet_thread_call(self):
        print("Camera opening...")
        self.time.setText("Please wait.. Camera opening...")
        self.TThread = TimeThread()

        self.movenetThread = movenet_Thread()

        self.movenetThread.start()
        self.movenetThread.movenet_status.connect(self.timer_thread_call)
        self.movenetThread.finished.connect(self.okay)

    def timer_thread_call(self, val):
        # print(val.ret)
        self.movenet_obj = val
        if val.ret == True:
            if self.TThread.isRunning() is False:
                self.TThread.start()

            self.TThread.timer_value.connect(self.timer_value_show)
            self.TThread.finished.connect(self.timeOver)

    def timer_value_show(self, val):
        self.time.setText("Time Remaining : " + str(val) + " sec")

    def timeOver(self):
        self.time.setText("                  Time Over")
        print("Time Over")
        # self.movenet_obj.cap.release()

        # self.movenetThread.terminate()
        # cv.destroyWindow('frame')

        # print("Time Over")

    def okay(self):
        print("Camera run successfully")
        self.nextpagecall()

    def nextpagecall(self):
        third = exercise_2_2()
        widget.addWidget(third)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class exercise_2_2(QMainWindow):
    def __init__(self):
        super(exercise_2_2, self).__init__()
        loadUi('exercise_2_page_2.ui', self)
        movie1 = QtGui.QMovie('GUI GIFs/ex 2 part 2.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        file1 = open("myfile.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("1")
        # file1.writelines(L)
        file1.close()
        self.movenet_thread_call_again()
        # self.startButton.clicked.connect(self.camera_thread_call)

    def movenet_thread_call_again(self):
        print("Camera opening...")
        self.time.setText("Please wait.. Camera opening...")
        start = time.time()
        self.TThread = TimeThread()

        self.movenetThread = movenet_Thread()

        self.movenetThread.start()
        self.movenetThread.movenet_status.connect(self.timer_thread_call)
        self.movenetThread.finished.connect(self.okay)

    def timer_thread_call(self, val):
        # print(val.ret)
        self.movenet_obj = val
        self.movenet_obj.count = 1
        if val.ret == True:
            if self.TThread.isRunning() is False:
                self.TThread.start()

            self.TThread.timer_value.connect(self.timer_value_show)
            self.TThread.finished.connect(self.timeOver)

    def timer_value_show(self, val):
        self.time.setText("Time Remaining : " + str(val) + " sec")

    def timeOver(self):
        self.time.setText("                  Time Over")
        # elf.camerathread_obj.cap.release()
        # self.camthread.terminate()

    def okay(self):
        print("Camera run successfully")
        pro_page = Result_page()
        widget.addWidget(pro_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

# 4th exercise




class exercise_3_1(QMainWindow):
    def __init__(self):
        super(exercise_3_1, self).__init__()
        loadUi('exercise_3_page_1.ui', self)
        movie1 = QtGui.QMovie('GUI GIFs/ex 3 part 1.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        file1 = open("myfile.txt", "w")

        # \n is placed to indicate EOL (End of Line)
        file1.write("0")
        # file1.writelines(L)
        file1.close()

        self.startButton.clicked.connect(self.movenet_thread_call)

    def movenet_thread_call(self):
        print("Camera opening...")
        self.time.setText("Please wait.. Camera opening...")
        start = time.time()
        self.TThread = TimeThread()

        self.movenetThread = movenet_Thread()

        self.movenetThread.start()
        self.movenetThread.movenet_status.connect(self.timer_thread_call)
        self.movenetThread.finished.connect(self.okay)

    def timer_thread_call(self, val):
        # print(val.ret)
        self.movenet_obj = val
        if val.ret == True:
            if self.TThread.isRunning() is False:
                self.TThread.start()

            self.TThread.timer_value.connect(self.timer_value_show)
            self.TThread.finished.connect(self.timeOver)

    def timer_value_show(self, val):
        self.time.setText("Time Remaining : " + str(val) + " sec")

    def timeOver(self):
        self.time.setText("                  Time Over")
        print("Time Over")
        # self.movenet_obj.cap.release()

        # self.movenetThread.terminate()
        # cv.destroyWindow('frame')

        # print("Time Over")

    def okay(self):
        print("Camera run successfully")
        self.nextpagecall()

    def nextpagecall(self):
        third = Result_page()
        widget.addWidget(third)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class processing_page(QMainWindow):
    def __init__(self):
        super(processing_page,self).__init__()
        loadUi('loading_page.ui',self)
        movie1 = QtGui.QMovie('loading.gif')
        self.gif.setMovie(movie1)
        movie1.start()
        #time.sleep(1)
        try:

            self.call_result_page()
        except:
            print("failed")
        #print("result_page called")


class Result_page(QMainWindow):
    def __init__(self):
        super(Result_page,self).__init__()
        loadUi('result_page.ui',self)
        print("result_page called")
        self.title.setText("We are processing Your Video....")
        self.step.setText("")
        self.call_graph_generation_model()
        self.pushButton.clicked.connect(self.call_mainpage)

    def call_graph_generation_model(self):
        print("Camera opening...")

        self.graphThread = graph_Thread()

        self.graphThread.start()
        self.graphThread.finished.connect(self.detection_scores)

        #self.image_show(value=1)

    def speak(text):
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 100)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()

    def detection_scores(self):
        self.detThread = detect_Thread()

        self.detThread.start()
        self.detThread.detection_status.connect(self.waiting)
        self.detThread.finished.connect(self.showScore)


    def call_mainpage(self):
        main_page = mainpage()
        widget.addWidget(main_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def waiting(self,value):
        self.score=value
    def showScore(self):
        file1 = open("myfile.txt", "r")

        # \n is placed to indicate EOL (End of Line)
        count = file1.read()

        # file1.writelines(L)
        file1.close()
        score_array = []
        if int(count) == 0:

            first=self.score[0].tolist()
            score_array.append(first)
        else:
            first = self.score[0].tolist()
            second=self.score[1].tolist()

            score_array.append(first)
            score_array.append(second)

        good=0
        bad=0
        good_score=[]
        bad_score=[]
        for sc in score_array:

            if round(sc[0][0],2)>=0.7:
                good +=1
                good_score.append(sc[0][0])
            else:
                good_score.append(sc[0][0])
                bad +=1
        if int(count) ==0:
            if good==1:
                self.title.setText("           Congratualtions !!! ")
                self.step.setText("You have done perfectly! Your Score is " + str(round(good_score[0] * 100, 2)) + " %")
                movie1 = QtGui.QMovie('correct.png')
                self.gif.setMovie(movie1)
            else:
                self.title.setText("           Sorry !!! ")
                self.step.setText("Please try again.. Score is low..")
                movie1 = QtGui.QMovie('incorrect.png')
                self.gif.setMovie(movie1)
                movie1.start()
        else:

            if good==2:

                self.title.setText("           Congratulations !!! ")
                self.step.setText("You have done perfectly! Your Score is "+str(round((sum(good_score) / len(good_score)*100),2))+" %")
                movie1 = QtGui.QMovie('correct.png')
                self.gif.setMovie(movie1)
                movie1.start()
            elif good == 1:
                self.title.setText("           Well Done !!! ")
                self.step.setText("You have done well in one part, other one was not good")
                movie1 = QtGui.QMovie('correct.png')
                self.gif.setMovie(movie1)
                movie1.start()
            else:
                self.title.setText("           Sorry !!! ")
                self.step.setText("Please try again.. Score is low..")
                movie1 = QtGui.QMovie('incorrect.png')
                self.gif.setMovie(movie1)
                movie1.start()
        print(self.score)

    def okay(self):
        print("Finished graph generation")
        pro_page=processing_page()
        widget.addWidget(pro_page)
        widget.setCurrentIndex(widget.currentIndex()+1)


app=QApplication(sys.argv)
page=mainpage()
widget=QtWidgets.QStackedWidget()
widget.addWidget(page)
#widget.setFixedHeight(600)
#widget.setFixedWidth(800)
widget.showMaximized()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')