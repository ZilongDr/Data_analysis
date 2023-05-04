# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 22:48:26 2023

@author: Wang
"""

import pywt
def SWT_Wavelet(data, w, l, max_num):
    coeff=pywt.swt(data, wavelet=w,level=l, norm=True)  
    coeff_new=[]
    for k in range(0,l,1):
        #print(k)
        cA=coeff[k][0]
        cD=coeff[k][1] # get cD parameter of each level
        
        T_cD_k=max_num
        
        cD_k_new=pywt.threshold(cD, T_cD_k, mode='soft')
        coeff_new.append((cA,cD_k_new))
        y_denoised=pywt.iswt(coeff_new, w, norm=True)

    return (y_denoised, coeff, coeff_new) 

