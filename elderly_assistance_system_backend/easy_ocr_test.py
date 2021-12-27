# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 01:04:56 2021

@author: ASUS
"""

import easyocr
import numpy as np
import time
import numpy as np
import cv2
from dateutil.relativedelta import relativedelta
import datetime as dt

import sqlite3
global fps

conn=sqlite3.connect('db.sqlite3')

c=conn.cursor()
# datetime object containing current date and time

#alpha and beta are image processing parameter
alpha = 1 # Contrast control (1.3.0)
beta = 0 # Brightness control (0-100)

'''def missing_medicine_counter(missing_object):
    Time=dt.datetime.combine(dt.date.today(), missing_object.time)
    time_now=dt.datetime.now().time()
    time_now = dt.datetime.combine(dt.date.today(), time_now)
    timedelta_obj = relativedelta(time_now, Time)
    if 0<=timedelta_obj.hours<23 and timedelta_obj.minutes>0:
        try:
            con_medicine=MedicineHistory.objects.get(name=missing_object.name,time=missing_object.time,date=dt.datetime.now().date())
        except:

            trig_medicine=MedicineHistory(name=missing_object.name,date=dt.datetime.now().date(),time=missing_object.time,consumed=False,time_of_consumption=dt.datetime.now().time())
            print("You misses ",trig_medicine.name)
            trig_medicine.save()
    else:
        return 0'''

#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
#check a medicine is valid or not comparing with medication time and current time
def validity(Time):
    time_now=dt.datetime.now().time()
    time_now = dt.datetime.combine(dt.date.today(), time_now)
    timedelta_obj = relativedelta(time_now, Time)
    if timedelta_obj.hours==0 and -55<=timedelta_obj.minutes<=55:
        return 1
    else:
        return 0

#image processing function 1
def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
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
#image processing function 2
def process(img):
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    return img


print("Model Loading...")
reader = easyocr.Reader(['en'],gpu=True) # need to run only once to load model into memory
print("Model loaded")
cap = cv2.VideoCapture(0)
#cap=cv.VideoCapture('http://192.168.0.103:4747/mjpegfeed')
prev_time=time.time()
current_time=0

def processing_pipeline(image):
    frame=cv2.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(frame, 130,255,0)
    kernel = np.ones((2,2),np.uint8)
    dilated = cv2.dilate(frame.copy(), kernel, iterations=1)
    #gradient = cv.morphologyEx(dilated, cv.MORPH_GRADIENT, kernel)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    return closing


if not cap.isOpened():
    print("Cannot open camera")
    exit()

def easy_ocr(medicine_name,medicine_ID,medicine_time):

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

            #frame=processing_pipeline(frame)
            med = reader.readtext(frame, detail = 0)
            print("3")
            med=list(map(str.lower, med))
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
                    #finished = 1  # this variable is for terminating program after getting one correct strip in front of camera

                # print(med)
            else:
                print("Show Madicine..")
        except:
            print("Error happened in image processing")
        #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
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
        cv2.imshow('frame', frame)
        if finished == 1:
            print("You have no more medicines. Thanks for taking your medicines")
            break
        if cv2.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()