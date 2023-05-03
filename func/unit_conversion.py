# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 14:28:53 2023

@author: Wang
"""
from scipy.constants import h, hbar, c, e, pi

def THz_to_Hz(f_THz):
    return f_THz*1e12

def Hz_to_THz(f_Hz):
    return f_Hz*1e-12

def nm_to_m(l_nm):
    return l_nm*1e-9

def Hz_to_rad(f_Hz):
    # Convert Hz to angular frequency
    return 2*pi*f_Hz

def m_to_nm(l_m):
    return l_m*1e9

def Hz_to_lamb(f_Hz):
    # convert to wavelength
    #in the unit of m
    return c/f_Hz
    
def ps_to_s(t_ps):
    # convert ps to second
    return t_ps*1e-12

def s_to_ps(t_s):
    # convert s to ps
    return t_s*1e12