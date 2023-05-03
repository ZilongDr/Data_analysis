# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 11:10:43 2023

@author: Wang
"""

# Define Gaussian shape in intensity
# In time:
import numpy as np

def calc_I_t(t, fwhm_t,t_shift): 
    """
    Parameters
    ----------
    t : array of float (symmetric with respect to 0)
        time (s)
    fwhm_t : float
        Full width Half Maximum in time

    Returns
    -------
    array of floats
        Gaussian temporal enveloppe (Intensity) of the pulse
    """
    return np.exp(-4*np.log(2)*(t-t_shift)**2/fwhm_t**2)

def calc_I_t2(t, fwhm_t, t_shift):
    """Calculate temporal waveform of THz electric field

    Args:
        t (array): time (s), symmetric with respect to 0
        fwhm_t (float): full width half maximum in time
        t_shift (float): time shift

    Returns:
        array of floats: Gaussian temporal enveloppe of the pulse
    """
    return (2/(fwhm_t**2))*np.exp(-(t-t_shift)**2/fwhm_t**2)-4*(((t-t_shift)**2)/(fwhm_t**2))*np.exp(-(t-t_shift)**2/fwhm_t**2)

# In frequency:
def calc_I_w(w, w0, fwhm_w): 
    """
    Parameters
    ----------
    w :  array of float (must contain the 0 frequency)
        angular frequency (rad.s^{-1})
    w0 : float
        central angular frequency
    fwhm_w : float
        Full width Half Maximum in angular frequency

    Returns
    ------
    array of floats
        Gaussian Intensity Spectrum
    """
    return np.exp(-4*np.log(2)*(w-w0)**2/fwhm_w**2)
