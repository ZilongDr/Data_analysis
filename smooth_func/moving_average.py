# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:48:04 2023

@author: Wang
"""
import numpy as np


# Build moving average with convolution:
def moving_average(data, box_len): 
    mask=np.ones(box_len)/box_len
    y_smooth=np.convolve(data, mask, mode='same')
    return y_smooth