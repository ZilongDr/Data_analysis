# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:52:35 2023

@author: Wang
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, linalg, sparse

def soft(x, T):
    threshold=1-np.divide(T, abs(x))
    comp=np.where(threshold<0, 0, threshold)
    y=np.multiply(comp, x)
    return y


def bpd_salsa(y, A, lamb, mu, Nit):
    '''
     x = bpd_salsa_sparsemtx(y, A, lambda, mu, Nit)
     BASIS PURSUIT DENOISING
     Minimize ||y - A x||_2^2 + lambda * || x ||_1
     where A is a sparse matrix
     
     INPUT
     y      : data
     A      : sparse matrix
     lamb : regularization parameter
     mu     : ADMM parameter
     Nit    : Number of iterations
     
     OUTPUT
     x      : solution to BPD problem
     
     [x, cost] = bpd_salsa_sparsemtx(...) returns cost function history
     
     
     The program implements SALSA (Afonso, Bioucas-Dias, Figueiredo,
     IEEE Trans Image Proc, 2010, p. 2345)
     '''
     
    AT=np.transpose(A)
    ATy = np.dot(AT,y)
    x=ATy
    d=np.zeros_like(x)

    [M, N]=np.shape(A)

    F=np.dot(AT, A)+ mu * sparse.eye(N)


    # Interation:
    for i in range(Nit):
        u=soft(x+d, 0.5*lamb/mu) - d
        x= np.linalg.lstsq(F, ATy + mu*u)[0]
        d=x-u

    
    return x

if __name__=='__main__':

    #%$
    # Create spike signal
    
    N = 100                    # N : length of signal
    s = np.zeros(N)
    k = [20, 45, 70]
    a = [2, -1, 1]
    for n, i in enumerate(k):
        s[i]=a[n]
    
    L = 4
    h = np.ones(L)/L         # h : impulse response
    
    M = N + L - 1
    w = 0.03 * np.random.randn(M)     # w : zero-mean Gaussian noise
    y = signal.convolve(h,s)+w        # y : observed data
    # Create convolution matrix
    
    h_pad=np.pad(h, pad_width=(0, N-1), mode='constant')
    first_row=np.zeros_like(s)
    first_row[0]=h[0]
    
    H=linalg.toeplitz(h_pad, first_row)
    
    
    # Define algorithm parameters
    lamb = 0.05                                      # lambda : regularization parameter
    Nit = 100                                     # Nit : number of iterations
    mu = 0.2                                         # mu : ADMM parameter
    
    x=bpd_salsa(y, H, lamb, mu, Nit)      
    
    plt.plot(x)
            
        