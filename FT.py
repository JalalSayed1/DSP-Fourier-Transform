import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

'''
data_n.shape = (number of samples, number of channels)
    number of channels = 2 for stereo, 1 for mono
    
data_n.dtype = int16 (−32,768 to 32,767 )

'''
rate_1, data_1 = wavfile.read('sound1.wav')
rate_2, data_2 = wavfile.read('sound2.wav')

#' print info:
print(f"rate_1 = {rate_1}") # 44100
print(f"rate_2 = {rate_2}") # 44100
print(f"data_1.shape = {data_1.shape}") # (498816, 2) 
print(f"data_2.shape = {data_2.shape}") # (465408, 2)
print(f"data_1.dtype = {data_1.dtype}") #  int16 (−32,768 to 32,767 )
print(f"data_2.dtype = {data_2.dtype}") #  int16
print(f"data_1.max = {data_1.max()}") # 32767 (clipped)
print(f"data_1.min = {data_1.min()}") # -32768 (clipped)
print(f"data_2.max = {data_2.max()}") # 14554 (not clipped)
print(f"data_2.min = {data_2.min()}") # -13712 (not clipped)

#' plot in time domain:
plt.figure(1)

# subplot(rows, columns, panel number):
plt.subplot(2, 1, 1) # 2 rows, 1 column, panel 1 (top):
plt.plot(data_1[:, 0]) # take the first column
plt.title('sound1.wav')

plt.subplot(2, 1, 2) # 2 rows, 1 column, panel 2 (bottom):
plt.plot(data_2[:, 0])
plt.title('sound2.wav')

# auto-adjust the spacing between subplots:
plt.tight_layout()

#' in the frequency domain:
plt.figure(2)

plt.subplot(2, 1, 1)
fft_data_1 = np.fft.fft(data_1[:, 0])
plt.plot(np.abs(fft_data_1)) # abs() to only plot the magnitude (not phase)
plt.title('sound1.wav')

plt.subplot(2, 1, 2)
fft_data_2 = np.fft.fft(data_2[:, 0])
plt.plot(np.abs(fft_data_2))
plt.title('sound2.wav')

plt.tight_layout()




plt.show()

