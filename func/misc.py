# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 15:45:25 2023

@author: Wang
"""

import numpy as np

# find nearest in array:

def find_array_index(data, element):
    idx = (np.abs(data - element)).argmin()
    d=data[idx]
    return idx, d
	
	
# Data normalization:

def norm_array(data):
    norm_value=np.amax(data)
    return data/norm_value