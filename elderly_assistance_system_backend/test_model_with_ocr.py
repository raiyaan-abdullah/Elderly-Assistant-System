# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 17:24:00 2021

@author: Riad
"""

import csv
from word_generate import train_data_generate 
import numpy as np
import tensorflow as tf
import pytesseract
import cv2
from east_detector import text_boundary,imcrop

from tensorflow.keras.models import load_model

#model= load_model("shortlist_checkpoints/medicine_name_predict.30-0.16.hdf5")
print("Model Loaded")
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)

from tensorflow.keras.models import load_model

#define char and medicine list
char_list = [' ', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','+','(',')',',','-','[',']','%','/','&','.','\'']

char_list_size = len(char_list)

word_length = 80

medicine_list=[]
companies=["shortlist_new.csv"]
for company in companies:
    with open(company) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            medicine_list.append(row[0].lower())

med_list_size = len(medicine_list)

char_to_index = {x: i for i, x in enumerate(char_list)}

'''def matching_medicine(med_name):
    input_name=med_name.lower()
    prediction = model.predict(input_name)    
    pred_index=np.argmax(prediction)
    return(medicine_list[pred_index])'''
        




pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

cap = cv2.VideoCapture(0)

alpha=0.9
beta=0
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
def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

def image_area(img):
    h,w,_=img.shape
    area=h*w
    return area

import re

def charFilter(myString):
    return re.sub('[^A-Z]+', '', myString, 0, re.I)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    adjusted = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
    bound_box=text_boundary(adjusted)
    gamma_adjusted=adjust_gamma(frame, gamma=3.5)
    med=pytesseract.image_to_string(gamma_adjusted)
    arr = med.split('\n')[0:-1]
    med = '\n'.join(arr)
    gamma_adjusted=adjust_gamma(frame, gamma=0.5)
    med=charFilter(pytesseract.image_to_string(gamma_adjusted))
    arr = med.split('\n')[0:-1]
    med = '\n'.join(arr)
        
    #print("Model Loaded")
    med+=pytesseract.image_to_string(adjusted)
    arr = med.split('\n')[0:-1]
    med = '\n'.join(arr)
    for b in bound_box:
        crop=imcrop(adjusted, b)
        if image_area(crop)>1000:
            pr=process(crop)
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            ret,pr_b = cv2.threshold(pr,127,255,cv2.THRESH_BINARY)
            # do adaptive threshold on gray image
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 15)
            
            # make background of input white where thresh is white
            result = crop.copy()
            result[thresh==255] = (255,255,255)
            med+=pytesseract.image_to_string(result)   #text for processing 2
            arr = med.split('\n')[0:-1]
            med = '\n'.join(arr)
            med+=pytesseract.image_to_string(pr_b)   #text for processing 2
            arr = med.split('\n')[0:-1]
            med = '\n'.join(arr)
            med=charFilter(med)
            #ret,thresh4 = cv2.threshold(pr,180,255,cv2.THRESH_TOZERO)
            #ret,thresh3 = cv2.threshold(pr,180,255,cv2.THRESH_TRUNC)
            #med+=pytesseract.image_to_string(thresh3) #text for processing 1
            
            #med+=pytesseract.image_to_string(thresh4) #text for processing 3
            #med+=pytesseract.image_to_string(thresh3) #text for processing 4
            text=med.split()
            if text:
                print(text)
            
    # Display the resulting frame
    cv2.imshow('frame',adjusted)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()