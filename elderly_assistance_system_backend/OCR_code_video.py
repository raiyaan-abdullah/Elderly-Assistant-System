# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 23:13:17 2020

@author: User
"""


import numpy as np
import cv2
from medicine.models import Medicine
import os
from medicine_history.models import MedicineHistory
import pytesseract
from east_detector import text_boundary,imcrop  #this is for getting the text box in image which coded manually
from datetime import datetime
from dateutil.relativedelta import relativedelta
import datetime as dt
from medicine_strip_text_recognition.medicine_detect_db import matching_medicine

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
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
    if timedelta_obj.hours==0 and -45<=timedelta_obj.minutes<=45:
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




def ocr(medicine_name,medicine_ID,medicine_time):
    url = "http://192.168.0.5:4747/video"
    cap = cv2.VideoCapture(url,cv2.CAP_DSHOW)
    while(True):
        finished=0
        # Capture frame-by-frame

        ret, frame = cap.read()
        print(ret)
        med=''
        # Our operations on the frame come here
        try:
            adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            bound_box=text_boundary(adjusted)
            #print("Model Loaded")
            med+=pytesseract.image_to_string(adjusted)
            for b in bound_box:
                crop=imcrop(adjusted, b)
                sharpened_image = unsharp_mask(crop)
                pr=process(crop)
                gray = cv2.cvtColor(sharpened_image, cv2.COLOR_BGR2GRAY)
                ret,pr_b = cv2.threshold(pr,127,255,cv2.THRESH_BINARY)
                ret,thresh4 = cv2.threshold(pr,180,255,cv2.THRESH_TOZERO)
                ret,thresh3 = cv2.threshold(pr,180,255,cv2.THRESH_TRUNC)
                med=pytesseract.image_to_string(thresh3) #text for processing 1
                med+=pytesseract.image_to_string(gray)   #text for processing 2
                med+=pytesseract.image_to_string(thresh4) #text for processing 3
                med+=pytesseract.image_to_string(thresh3) #text for processing 4

                if (med):
                    # Fenat, Napa... are some test medicine
                    #print(med)
                    matched_medicine=matching_medicine(med)
                    if medicine_name.lower == matched_medicine.lower:
                        print(medicine_name," found")
                        try:
                            con_medicine=MedicineHistory.objects.get(medicine_id=int(medicine_ID), date=dt.datetime.now().date())
                            if con_medicine.consumed==True:
                                print("Already taken")
                            else:
                                con_medicine.consumed=True
                                con_medicine.time_of_consumption=dt.datetime.now().time()
                                con_medicine.save()
                                finished=1 #this variable is for terminating program after getting one correct strip in front of camera
                        except:
                            #print(obj.id)
                            print("Medicine is not registered on medicine history page")
                            
                
                    #print(med)
                else:
                    print("Show Madicine..")
        except:
            print("Error happened in image processing")
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if finished==1:
            print("You have no more medicines. Thanks for taking your medicines")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
'''medicine_objects=Medicine.objects.all() #got todays routine medicine list
loopCount=0
for obj in medicine_objects:
    #time_list.append(obj.time)
    if(validity(dt.datetime.combine(dt.date.today(), obj.time))):  #check the medicine is correct for taking or not
        try:
            con_medicine=MedicineHistory.objects.get(medicine_id=int(obj.id),date=dt.datetime.now().date())
            if con_medicine.consumed==True:
                print("You have already taken your scheduled medicines.",obj.name)
            else:
                print("Time for ",obj.name," ",obj.time)
                ocr(obj.name,obj.id,obj.time)


        except:
            #print(obj.id)
            pass
    else:
        loopCount+=1
    #missing_medicine_counter(obj)
if loopCount==len(medicine_objects):
    #print(loopCount)
    print("Wrong time for medication")'''