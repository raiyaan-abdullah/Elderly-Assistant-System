# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 02:36:58 2021

@author: Raiya
"""
import os 

os.system('python openpose_python.py --video movenet/record.mp4 --net_resolution 528x272 --write_json movenet/live_json/')