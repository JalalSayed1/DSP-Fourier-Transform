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

time1 = np.linspace(0, len(data_1)/rate_1, num=len(data_1))
time2 = np.linspace(0, len(data_2)/rate_2, num=len(data_2))

#normalize:
# half of the max value of int16 is 2**15:
data_1 = data_1 / 2**15 
data_2 = data_2 / 2**15

# data_1 = 2 * (data_1 - np.min(data_1)) / (np.max(data_1) - np.min(data_1)) - 1
# data_2 = 2 * (data_2 - np.min(data_2)) / (np.max(data_2) - np.min(data_2)) - 1


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
plt.plot(time1, data_1[:, 0]) # take the first column
plt.title('sound1.wav')

plt.subplot(2, 1, 2) # 2 rows, 1 column, panel 2 (bottom):
plt.plot(time2, data_2[:, 0])
plt.title('sound2.wav')

# auto-adjust the spacing between subplots:
plt.tight_layout()

#' in the frequency domain:
plt.figure(2)

plt.subplot(2, 1, 1)
# divide by number of samples to normalize (so data is always below 0dB):
fft_data_1 = np.abs(np.fft.fft(data_1[:, 0])[0:int(len(data_1)/2)]) / len(data_1)
# convert data to dB:
fft_data_1 = np.log10(fft_data_1) * 20

# create frequency axis from 0 to Nyquist frequency (half the sampling rate):
freqs = np.linspace(0, rate_1/2, num=int(len(data_1)/2))

plt.plot(freqs, fft_data_1)
plt.semilogx()
plt.grid(True)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (dB)")
plt.title('sound1.wav')


# plt.subplot(2, 1, 2)


plt.tight_layout()




plt.show()

