# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 11:18:53 2023

@author: Wang
"""

# Define a ultrashort laser class:

from func import Gaussian_intensity as gs
from func import FFT as FT
from func import time_frequency_conversion as ft
from func import unit_conversion as ut
import numpy as np
import matplotlib.pyplot as plt

def THz_pulse(E0, t, tau, t_shift, omega_0, beta, phi):
    """
    Calculate the time domain THz pulses
    
    Parameter:
    t: time base in [s]
    tau: FWHM of the Gaussian pulse in [s]
    t_shift: time shift
    omega_0: central angular frequency in [rad/s]
    beta: linear temporal chirp
    return:
    THz pulse in time domain
    """
    #gauss_t=gs.calc_I_t(t, tau, t_shift)
    gauss2_t=gs.calc_I_t2(t, tau, t_shift)
    pulse=E0*gauss2_t*np.exp(1j*(omega_0*t+beta*(t**2)+phi))
    return pulse

if __name__=="__main__":
    omega_0=3.9 # in the unit of 2pi*THz
    t_ps=np.linspace(0,40, 1000) # in the unit of ps
    tau_ps=2 # in the unit of ps
    t_shift=10 # in the unit of ps
    phi=1
    beta_ps=-0.03 # in the unit of rad/ps2
    E0=100
    
    pulse=THz_pulse(E0, t_ps, tau_ps, t_shift, omega_0, beta_ps, phi)



    plt.plot(t_ps, np.real(pulse))
    plt.show()
    
    # Frequency domain:
    t=ut.ps_to_s(t_ps)
    ft=FT.fourier_transform(pulse, t, 10)
    f=ft[0]
    f_THz=ut.Hz_to_THz(f)
    Amp=ft[2]**2

    plt.plot(f_THz, Amp)
    plt.xlim(0,4)
    plt.show()
