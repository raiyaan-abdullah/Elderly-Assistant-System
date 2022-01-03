import schedule
import time
import requests
from datetime import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta
from easy_ocr_test import easy_ocr
import serial
from django import db
import sqlite3
from PyQt5.QtCore import pyqtSignal
import easyocr
import numpy as np
import time
import numpy as np
import cv2
from dateutil.relativedelta import relativedelta
import datetime as dt

import sqlite3
global fps



count=0


from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
import glob
class main_code_thread(QThread):
    status=pyqtSignal(QObject)
    print("Model Loading...")
    reader = easyocr.Reader(['en'], gpu=True)  # need to run only once to load model into memory
    print("Model loaded")


    message=""
    drawer_no="None"


    def validity(self,Time):
        time_now=datetime.now().time()
        time_now = datetime.combine(dt.date.today(), time_now)
        timedelta_obj = relativedelta(time_now, Time)
        if timedelta_obj.hours==0 and -59<=timedelta_obj.minutes<=59:
            return 1
        else:
            return 0

    #need to modify these code so that for every medicine name the serial write is that drawer number
    def drawer_activate(self,medicine):
        with serial.Serial('COM8', 9800, timeout=1) as ser:
            time.sleep(2)
            self.c.execute("SELECT * FROM medicine_medicine")  # got todays routine medicine list
            medicine_objects = self.c.fetchall()
            for obj in medicine_objects:
                if obj[1] == medicine:
                    drawer=str(obj[4])
                    self.drawer_no=drawer
                    print("drawer no: ",drawer)
                    self.status.emit(self)

                    encoded_string = drawer.encode()
                    byte_array = bytearray(encoded_string)
                    ser.write(byte_array)
                    time.sleep(2)
            # if medicine=='Provair':
            #     ser.write(b'P')   # send the pyte string 'H'
            #     time.sleep(2)   # wait 0.5 seconds
            # elif medicine=='E-CAP':
            #     ser.write(b'E')   # send the pyte string 'H'
            #     time.sleep(2)   # wait 0.5 seconds
            # elif medicine=='Fexo':
            #     ser.write(b'F')   # send the pyte string 'H'
            #     time.sleep(2)   # wait 0.5 seconds
            #





    # cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    # check a medicine is valid or not comparing with medication time and current time

    # image processing function 1
    def unsharp_mask(self,image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
        """Return a sharpened version of the image, using an unsharp mask."""
        blurred = cv2.GaussianBlur(image, kernel_size, sigma)
        sharpened = float(amount + 1) * image - float(amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if threshold > 0:
            low_contrast_mask = np.absolute(image - blurred) < threshold
            np.copyto(sharpened, image, where=low_contrast_mask)
        return sharpened

    # image processing function 2
    def process(self,img):
        img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                              31, 2)
        cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY, 31, 2)
        cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        return img




    def processing_pipeline(self,image):
        frame = cv2.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(frame, 130, 255, 0)
        kernel = np.ones((2, 2), np.uint8)
        dilated = cv2.dilate(frame.copy(), kernel, iterations=1)
        # gradient = cv.morphologyEx(dilated, cv.MORPH_GRADIENT, kernel)
        closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
        return closing


    def easy_ocr(self,medicine_name, medicine_ID, medicine_time):
        cap = cv2.VideoCapture(0)
        # cap=cv.VideoCapture('http://192.168.0.103:4747/mjpegfeed')
        prev_time = time.time()
        current_time = 0
        conn = sqlite3.connect('db.sqlite3')

        c = conn.cursor()
        # datetime object containing current date and time

        # alpha and beta are image processing parameter
        alpha = 1  # Contrast control (1.3.0)
        beta = 0  # Brightness control (0-100)

        while True:
            finished = 0
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Our operations on the frame come here
            try:
                print("1")

                # frame=processing_pipeline(frame)
                med = self.reader.readtext(frame, detail=0)
                print("3")
                med = list(map(str.lower, med))
                '''current_time=time.time()
                time_diff=current_time-prev_time
                fps = 1/time_diff
                prev_time=current_time'''
                print(med)
                if (len(med)):
                    print(medicine_name)
                    # Fenat, Napa... are some test medicine
                    # print(med)
                    if medicine_name.lower() in med:
                        print(medicine_name, " found")
                        self.message= medicine_name.capitalize()+" found"
                        self.status.emit(self)
                        finished = 1
                        Date = '"{}"'.format(dt.datetime.now().date())
                        print(Date)
                        c.execute("UPDATE medicine_history_medicinehistory SET consumed = 1 WHERE medicine_id=" + str(
                            medicine_ID) + " AND date=" + Date)
                        conn.commit()
                        T = '"{}"'.format(str(dt.datetime.now().time()))
                        c.execute(
                            "UPDATE medicine_history_medicinehistory SET time_of_consumption=" + T + " WHERE medicine_id=" + str(
                                medicine_ID) + " AND date=" + Date)
                        conn.commit()
                        print("commit completed..")
                        # finished = 1  # this variable is for terminating program after getting one correct strip in front of camera

                    # print(med)
                else:
                    print("Please show the medicine..")
                    self.message = "Please show the medicine.."
                    self.status.emit(self)
            except:
                print("Error happened in image processing")
            # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # Display the resulting frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            # org
            org = (50, 50)

            # fontScale
            fontScale = 1

            # Blue color in BGR
            color = (255, 0, 0)

            # Line thickness of 2 px
            thickness = 2

            # Using cv2.putText() method
            # image = cv2.putText(frame, "FPS: "+str(int(fps)), org, font,
            #                    fontScale, color, thickness, cv.LINE_AA)
            # Display the resulting frame

            if finished == 1:
                print("You have no more medicines. Thanks for taking your medicines")
                self.message = "You have no more medicines. Thanks for taking your medicines"
                self.status.emit(self)
                break
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def call_ocr_code(self):
        conn = sqlite3.connect('db.sqlite3')

        c = conn.cursor()
        c.execute("SELECT * FROM medicine_medicine") #got todays routine medicine list
        medicine_objects=c.fetchall()
        loopCount=0
        for obj in medicine_objects:
            #time_list.append(obj.time)
            datetime_object=datetime_object=datetime.strptime(obj[2], '%H:%M:%S')
            if(self.validity(dt.datetime.combine(dt.date.today(), datetime_object.time()))):  #check the medicine is correct for taking or not
                Date='"{}"'.format(dt.datetime.now().date())
                c.execute("SELECT * FROM medicine_history_medicinehistory WHERE medicine_id="+str(obj[0])+" AND date="+Date)
                con_medicine=c.fetchone()
                #print(con_medicine[1])

                if con_medicine[1]==1:
                    print("You have already taken your scheduled medicines.",obj[1])

                    self.message="You have already taken your scheduled medicines."
                    self.status.emit(self)
                else:
                    #drawer_activate(obj[1])
                    print("Time for ",obj[1]," ",obj[2])
                    t = datetime.strptime(obj[2], '%H:%M:%S')
                    t=t.strftime("%I:%M %p")
                    #t=obj[2].strftime("%I:%M %p")
                    self.message = "Time for "+str(obj[1]).capitalize()+" "+str(t)
                    self.drawer_no=str(obj[4])
                    self.status.emit(self)
                    self.easy_ocr(obj[1],obj[0],obj[2])



            else:
                loopCount+=1
            #missing_medicine_counter(obj)
        if loopCount==len(medicine_objects):
            #print(loopCount)
            print("Wrong time for medication")
            self.message = "Wrong time for medication"
            self.status.emit(self)
            return None


    def create_data(self):
        required_medicine=[] #The medicine history data that will be sent to server
        keys_to_remove = ["name","time","started"]

        fetch_url = 'http://127.0.0.1:8000/api/medicine/'
        destination_url = 'http://127.0.0.1:8000/api/medicine-history/'

        '''
        Example of data to be sent
        {
            "name": "Ranitid",
            "date":"2020-04-15",
            "time": "15:23:00",
            "consumed": True,
            "time_of_consumption": "15:23:00"
            
        }
        '''

        received = requests.get(fetch_url).json() #The medicine list data received sent from server
        today = datetime.today().strftime('%Y-%m-%d')
        new_keys = {"date" : today, "consumed" : "False", "time_of_consumption" : "00:00:00"}

        for medicine in received:
            for key in keys_to_remove:
                medicine.pop(key)
            medicine['medicine_id'] = medicine.pop('id')
            medicine.update(new_keys)
            required_medicine.append(medicine)



        for medicine in required_medicine:
            sent_data = requests.post(destination_url, data = medicine)
            print(sent_data)

    #schedule.every(5).minutes.do(create_data)



    def run(self):
        #self.create_data()

            #schedule.run_pending()
            #time.sleep(1)
        status=self.call_ocr_code()
        if status==0:
            #return "You have already taken your scheduled medicines."
            return 0
        #return message

#medicine_code()