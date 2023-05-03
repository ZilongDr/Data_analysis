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

# Convert from DataFrame to np, remove nan
def convert_to_np(data):
    """" Convert DataFrame to np array

    Args:
        data (DataFrame):Pandas dataframe

    Returns:
        numpy array: numpy array with no nan
    """
    data=np.array(data.dropna())
    return data