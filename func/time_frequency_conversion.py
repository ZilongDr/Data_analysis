# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 11:09:29 2023

@author: Wang
"""


# Prepare time and frequency domain:

# time2freq(t,Nbw) which takes as an argument an array of times and returns an array of Nbw angular frequencies $\omega$ (rad.s$^{-1}$).
# freq2time(w,Nbt) which takes as an argument an array of angular frequencies and returns an array of Nbt times $t$ (s).

#One remark, even if it is absolutely not mandatory, we will work in general with symmetrical frequency and time domain (same number of points, and zero time and zero frequency at the center of the window). 
# This makes switching back and forth between the two domains easier.

import numpy as np

def time2freq(t,Nbw):
    """
    Parameters
    ----------
    t : array of floats
        time
    Nbw : integer
        Nunmber of points to be used. Nbw must be greater that Nbt=len(t) for ZERO-PADDING
    
    Returns
    -------
    w : angular frequency

    """
    # temporal sampling rate
    delta_t=t[1]-t[0] 
    # total temporal range
    Delta_t=(Nbw)*delta_t 
    # spectral sampling rate
    delta_w=2*np.pi/Delta_t 
    # total spectral range
    Delta_w=delta_w*Nbw 
    # Angular frequency
    w=np.linspace(-Delta_w/2,Delta_w/2,Nbw)
    return w

def freq2time(w,Nbt):
    """
    Parameters
    ----------
    w : array of floats
        angular frequency (must contains 0 frequency)
    Nbt : integer
        Nunmber of points to be used. Nbt must be greater that Nbw=len(w) for ZERO-PADDING
    
    Returns
    -------
    t : array of time (s)

    """
    # spectral sampling rate
    delta_w=w[1]-w[0] 
    # total spectral range
    Delta_w=Nbt*delta_w
    # temporal sampling rate
    delta_t=2.*np.pi/Delta_w
    # total temporal range
    Delta_t=delta_t*Nbt 
    # Array of time
    t=np.linspace(-Delta_t/2,Delta_t/2,Nbt)
    return t