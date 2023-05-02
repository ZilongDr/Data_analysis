# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 11:09:47 2023

@author: Wang
"""
import numpy as np
from scipy.fft import fft, fftshift, ifft, next_fast_len, fftfreq, rfft, rfftfreq, irfft
from scipy.constants import h, hbar, c, e, pi
import matplotlib.pyplot as plt
def FFT (time_base,data, N):
    """Do the Fourier transform on the data and output the frequency axis

    Args:
        time_base (1d array, float): time axis in [s]
        data (1d array, float): time response
        N (Int): total number of points including zero padding

    Returns:
        tuple: (freq: frequecy axis, start from zero, just consider positive frequency, in the unit of [Hz],   
    Complex FFT results)
    """      
    # Set number of zero padding to the data:
    '''
    N=np.size(time_base) #Number of samples
    zeroN=zeroN_factor*N
    totalN=zeroN+N
    '''
    #totalN=zeroN_factor
    #zeropadded_y=np.zeros(totalN)
    #zeropadded_y[:N]=data    
    
    #totalN_opt=totalN
    delta_t=time_base[1]-time_base[0] #sampling 'time', in the unit of [s]
    #fs=1/delta_t #Sampling rate [Hz]
    #D_t=time_base[-1]-time_base[0] # Calculate time range
    # 'Frequency' domain:
    #delta_f=1/D_t # frequency spacing [Hz]
    #Df=N*delta_f # frequency range [Hz]
    #freq=np.linspace(0,Df/2, int(totalN_opt/2) )
    # prepare the 'frequecy' axis in Hz
    freq=rfftfreq(N, delta_t)
    #freq=freq_full[0:len(freq_full)//2]
    # Do the FFT using rfft so that only the positive frequency are taken:

    F=rfft(data, N)
    #F_processed=F[0:totalN_opt//2] # Take the unpad data
    #Phase=np.unwrap(np.angle(F_processed, deg=False))
    
    return (freq, F)

def IFFT(freq, data, N):
    """Do the inverse FFT by adding negative frequency component

    Args:
        freq (np array, float): Frequency axis in [Hz]
        data (np array, complex): Complex frequency response 
        N (Int): total length of original data, including zero padding length

    Returns:
        tuple: (time axis in [s], complex time domain response) 
    """   
    # calculate time base:
    df=freq[1]-freq[0]
    dt=1/(data.size*df)
    
    
    y=irfft(data, N)
    t=np.arange(y.size)*dt
    
    return (t, y)