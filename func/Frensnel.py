# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 11:17:34 2023

@author: Wang
"""

from __future__ import division, print_function, absolute_import
from numpy.lib import scimath

import sys

import numpy as np


#Snell law calculate refractive angle theta_t
def Snell (theta_i,n_i,n_t):
    """
    Parameters
    ----------
    theta_i: float, incident angle (in rad)
    n_i: float, refractive index of medium of indicent beam (unitless)
    n_t: float, refractive index of medium of refractive beam (unitless)

    Returns
    -------
    refractive angle (in rad) following the equation:
    theta_t=n_i*sin(theta_i)/n_t
    If abs(a) exceeding 1, return complex value.
    """
    a=n_i*np.sin(theta_i)/n_t
    theta_t=scimath.arcsin(a)
    return theta_t

#Frensnel equation transmission for s and p polarization:
def Frensnel_trans(theta_i,n_i,n_t):
    """
    Parameters
    ----------
    theta_i: float, incident angle (in rad)
    n_i: float, refractive index of medium of indicent beam (unitless)
    n_t: float, refractive index of medium of refractive beam (unitless)

    Returns
    -------
    Transmission vector, t=E_t/E_i, first element: t_s, second element: t_p
    
    """
    theta_t=np.real(Snell(theta_i,n_i,n_t))
    t=np.empty((2,1))
    t_p=2*n_i*np.cos(theta_i)/(n_i*np.cos(theta_t)+n_t*np.cos(theta_i))
    t_s=2*n_i*np.cos(theta_i)/(n_i*np.cos(theta_i)+n_t*np.cos(theta_t))
    return t_s,t_p

#Frensnel equation reflection for s and p polarization:
def Frensnel_refl(theta_i,n_i,n_t):
    """
    Parameters
    ----------
    theta_i: float, incident angle (in rad)
    n_i: float, refractive index of medium of indicent beam (unitless)
    n_t: float, refractive index of medium of refractive beam (unitless)

    Returns
    -------
    Rransmission vector, r=E_r/E_i, first element: r_s, second element: r_p
    
    """
    
    theta_t=np.real(Snell(theta_i,n_i,n_t))
    r=np.empty((2,1))
    r_p=(n_i*np.cos(theta_t)-n_t*np.cos(theta_i))/(n_i*np.cos(theta_t)+n_t*np.cos(theta_i))
    r_s=(n_i*np.cos(theta_i)-n_t*np.cos(theta_t))/(n_i*np.cos(theta_i)+n_t*np.cos(theta_t))
    return r_s,r_p


# Define Brewster angle condition:
def Brewster(n_i,n_t):
    """
    Parameters
    ----------
    n_i: float, refractive index of medium of indicent beam (unitless)
    n_t: float, refractive index of medium of refractive beam (unitless)

    Returns
    -------
    Brewster angle (in rad) following the equation:
    theta_B=arctan(n_t/n_i)
    """
    theta_B=np.arctan2(n_t,n_i)
    return theta_B

# Define Critial angle of total internal reflection condition:
def Internal_refl(n_rare,n_dense):
    """
    Parameters
    ----------
    n_rare: float, refractive index of (rarer) medium of indicent beam (unitless)
    n_denser: float, refractive index of (denser) medium of refractive beam (unitless)

    Returns
    -------
    Cristial angle (in rad) following the equation:
    theta_c=arcsin(n_rare/n_dense)
    """
    theta_c=np.arcsin(n_rare/n_dense)
    return theta_c