# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 21:32:11 2021

@author: Riad
"""

import random as rnd
import string
import math
from pandas.core.common import flatten

given_name='ranitid'
''' thresh is a value that refers at best how many letter will be deleted in
optimized_delete function '''
thresh=3
def delete_random(name):
    random_position=rnd.randint(0, len(name)-1)
    modified=name[0:random_position]+name[random_position+1:]
    return modified.lower()

def delete(name,position):
    modified=name[0:position]+name[position+1:]
    return modified.lower()

def optimized_delete(name):
    modified=[]
    if len(name)>thresh:
        delete_char=len(name)-thresh+1
        #print(delete_char)
        for i in range(1,delete_char):
            random_position=rnd.randint(0, len(name)-i)
            modified.append((name[0:random_position]+name[random_position+i:]).lower())
    return modified
        

def Replace(name,position):
    working_name=name[:]
    inter_char=working_name[position]
    replace_with=rnd.choice(string.ascii_letters)
    if inter_char != replace_with:
        if position==0:
            modified=(str(replace_with)+name[position+1:len(name)]).lower()
        else:
            modified=(name[0:position-1]+str(replace_with)+name[position:len(name)]).lower()
        #print("modified on ", position, modified)
        return modified
    else:
        return Replace(working_name,position)
    
def Insert(name,position):
    inter_char=name[position]
    insert_with=rnd.choice(string.ascii_letters)
    if inter_char != insert_with:
        modified=(name[0:position]+str(insert_with)+name[position:]).lower()
        return modified
    else:
        return Insert(name,position)
    

def edit(input_name, number_of_word):
    gen_words=[]
    n=math.ceil(number_of_word/10)
    #print(n)
    for i in range(n):
        for j in range(0,6):    
            gen_words.append(Replace(input_name,rnd.randint(0, len(input_name)-1)))
        gen_words.append(Insert(input_name,rnd.randint(0, len(input_name)-1)))
        gen_words.append(optimized_delete(input_name))
        gen_words.append(delete_random(input_name))
        gen_words.append(delete(input_name,0))
        gen_words.append(delete(input_name,len(input_name)-1))
    return gen_words
                         
'''' it generates 100 words but all of them are not unique. Unique word number little
bit less than 100. 10 multiple is for we have 10 edit operation on given string
6 replace, 1 insert, 1 random delete and 2 positional delete . Increase 100 to 150 or
bigger to get more generated word'''
def train_data_generate(given_name):
    generated=edit(given_name,100) #use 10 multiple
    generated=list(flatten(generated))
    gen_set=set(generated)
    generated=list(gen_set)
    #print(len(generated),"words generated for ",given_name,":\n",generated)
    return generated


#train_data_generate((given_name))
#print(rnd.choice(string.ascii_letters))