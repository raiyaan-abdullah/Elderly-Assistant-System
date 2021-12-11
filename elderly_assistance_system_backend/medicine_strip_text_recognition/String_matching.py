# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:13:15 2020

@author: User
"""


from fuzzywuzzy import process
from word_generator_from_ocr_text import ngrams


def string_matching_score(medicine_list,ocr_text):
    medicine_names = medicine_list
    
    medicine_counts=[]
    
    for med in medicine_names:
        medicine_counts.append(0)
        
    #print(medicine_counts)
    high=["",0]
    for med in medicine_names:
        n=len(med)
        wordlist=ngrams(ocr_text.lower(),n)
        for word in wordlist:
            
            #Ratios = process.extract(str2Match,strOptions)
            highest = process.extractOne(word,medicine_names)
            matched_med=highest[0]
            matched_med_per=highest[1]
            med_index=medicine_names.index(matched_med)
            medicine_counts[med_index]=round(medicine_counts[med_index]+(matched_med_per/100),2)
            if highest[1] > high[1]:
                '''if highest[0]==high[0]:
                    high[1]= highest[1]
                else:
                    high[]'''
                high[0]=highest[0]
                high[1]=highest[1]
    return medicine_counts
        
        
