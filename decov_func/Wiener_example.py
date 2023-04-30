import numpy as np
from scipy.signal import fftconvolve
from scipy.signal import wiener

#-----------------------------
#This code assumes that the degraded signal and the blurring kernel are stored in text files called degraded_signal.txt and blurring_kernel.txt, #respectively. The code first calculates the Fourier transform of the blurring kernel and the power spectral density of the degraded signal. It then #calculates the transfer function of the Wiener filter and applies it to the degraded signal to obtain the restored signal. Finally, it uses the #wiener function from scipy.signal to perform the same deconvolution and prints the results of both implementations.
#----------------------------------------------------------------------------


# Load the degraded signal and the blurring kernel
degraded_signal = np.loadtxt('degraded_signal.txt')
blurring_kernel = np.loadtxt('blurring_kernel.txt')

# Calculate the Fourier transform of the blurring kernel
blurring_kernel_fft = np.fft.fft2(blurring_kernel, degraded_signal.shape)

# Calculate the power spectral density of the degraded signal
psd = np.abs(np.fft.fft2(degraded_signal)) ** 2 / np.prod(degraded_signal.shape)

# Calculate the Wiener filter transfer function
wiener_filter_tf = np.conj(blurring_kernel_fft) / (np.abs(blurring_kernel_fft) ** 2 + psd / np.mean(psd))

# Apply the Wiener filter to the degraded signal
restored_signal = np.real(np.fft.ifft2(wiener_filter_tf * np.fft.fft2(degraded_signal)))

# Apply the Wiener filter to the degraded signal using the scipy.signal.wiener function
restored_signal_scipy = wiener(degraded_signal, (blurring_kernel.shape[0], blurring_kernel.shape[1]))

# Print the results
print('Restored signal (custom implementation):\n', restored_signal)
print('Restored signal (scipy implementation):\n', restored_signal_scipy)
