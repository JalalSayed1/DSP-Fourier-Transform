import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter
from scipy.io import wavfile

# Constant.
INT16_HALF_MAX = 2**15

def read_and_normalize_wav(filename):
    '''Reads a wav file and returns the normalized data, rate, and time axis.'''
    rate, data = wavfile.read(filename)
    data_normalized = data[:, 0] / INT16_HALF_MAX
    time_axis = np.linspace(0, len(data)/rate, num=len(data))
    return rate, data_normalized, time_axis

def my_fft(data, rate):
    '''Returns the frequency spectrum of the data.'''
    fft_data = (np.fft.fft(data)) / len(data)
    freqs = np.linspace(0, rate/2, num=len(data))
    return freqs, fft_data

def my_ifft(fft_data):
    '''Returns the time domain of the frequency spectrum.'''
    return np.fft.ifft(fft_data) * len(fft_data)

def plot_frequency_domain(fft_data, freqs, figure=None, legend=""):
    '''Plots the frequency spectrum in dB scale.'''
    if figure is None:
        figure = plt.figure()
    
    # for plotting purposes, only plot the first half of the data so we don't see the mirror:
    fft_data_half = fft_data[:int(len(fft_data)/2)]
    freqs = freqs[:int(len(freqs)/2)]
    
    fft_data_db = 20 * np.log10(fft_data_half)
    
    # label is to name this plot in the legend:
    plt.semilogx(freqs, fft_data_db, label=legend)
    plt.grid(True)
    
    # To show actual frequency values on the x-axis:
    axes = plt.gca()
    axes.xaxis.set_major_formatter(LogFormatter(labelOnlyBase=False))
    
    # Add grid for all x-axis values
    axes.xaxis.grid(True, which='both')
    
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    # plt.show()
    
    return figure

def plot_time_domain(data, time_axis, figure=None, legend=""):
    '''Plots the time domain.
    data: raw data (not fft data)
    figure: if None, create a new figure. Otherwise, plot on the given figure.
    '''
    if figure is None:
        figure = plt.figure()
    
    # label is to name this plot in the legend:
    plt.plot(time_axis, data, label=legend)
    plt.grid(True)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    # plt.show()
    
    return figure

def freq_to_index(freq, sampling_rate, data_length):
    '''Returns the index of the frequency in the frequency spectrum.'''
    return int(freq / (sampling_rate/2) * data_length)

def index_to_freq(index, sampling_rate, data_length):
    '''Returns the frequency of the index in the frequency spectrum.'''
    return index / data_length * (sampling_rate/2)

def clarify_sound(fft_data, sampling_rate, low_freq, high_freq, damping_factor = 0.11, boost_factor = 10):
    '''Clarifies the sound by damping all data then boosting the frequency spectrum between low_freq and high_freq.
    damping_factor: the factor to damp all frequencies (linear scale). Default is 0.1.
    boost_factor: the factor to boost the desired frequencies only (linear scale). Default is 10.
    '''
    
    # index = freq/nyquist freq * number of samples. Nyquist freq = 1/2 * sampling rate 
    low_index = freq_to_index(low_freq, sampling_rate, len(fft_data))
    high_index = freq_to_index(high_freq, sampling_rate, len(fft_data))
    
    # damp all frequencies first then only boost the desired frequencies:
    fft_data_new = fft_data * damping_factor # damp all frequencies
    fft_data_new[low_index:high_index] = fft_data_new[low_index:high_index] * boost_factor # boost the desired frequencies only
    
    return fft_data_new

def remove_noise(low_freq, high_freq, fft_data, sampling_rate, damping_factor = 0.01):
    '''Removes noise by damping the frequency spectrum between low_freq and high_freq.'''
    
    low_index = freq_to_index(low_freq, sampling_rate, len(fft_data))
    high_index = freq_to_index(high_freq, sampling_rate, len(fft_data))
    
    fft_data_new = fft_data[:]
    
    fft_data_new[low_index:high_index] = fft_data_new[low_index:high_index] * damping_factor
    
    return fft_data_new
    
#' figures for plotting
title1 = "Time domain of sound1.wav before and after noise removal"
title2 = "Frequency domain of sound1.wav before and after noise removal"
title3 = "Time domain of sound2.wav before and after noise removal"
title4 = "Frequency domain of sound2.wav before and after noise removal"

figure_time_domain_1 = plt.figure(title1)
figure_frequency_domain_1 = plt.figure(title2)
figure_time_domain_2 = plt.figure(title3)
figure_frequency_domain_2 = plt.figure(title4)

#' Read and normalize wav file
rate1, data1, time1 = read_and_normalize_wav('sound1.wav')
rate2, data2, time2 = read_and_normalize_wav('sound2.wav')

# figure_time_domain_1 = plot_time_domain(data1, time1, figure=figure_time_domain_1, legend="sound1.wav original")
# figure_time_domain_2 = plot_time_domain(data2, time2, figure=figure_time_domain_2, legend="sound2.wav original")

#' Plot in the frequency domain
freqs1, fft_data1 = my_fft(data1, rate1)
freqs2, fft_data2 = my_fft(data2, rate2)

plt.figure(figure_frequency_domain_1.number)
figure_frequency_domain_1 = plot_frequency_domain(np.abs(fft_data1), freqs1, figure=figure_frequency_domain_1, legend="sound1.wav original")
plt.figure(figure_frequency_domain_2.number)
figure_frequency_domain_2 = plot_frequency_domain(np.abs(fft_data2), freqs2, figure=figure_frequency_domain_2, legend="sound2.wav original")

#' ifft 
# data1_ifft = my_ifft(fft_data1)
# data2_ifft = my_ifft(fft_data2)

# plt.figure(figure_frequency_domain_1.number)
# figure_frequency_domain_1 = plot_time_domain(data1_ifft, time1, figure=figure_frequency_domain_1, legend="sound1.wav after fft")
# plt.figure(figure_frequency_domain_2.number)
# figure_frequency_domain_2 = plot_time_domain(data2_ifft, time2, figure=figure_frequency_domain_2, legend="sound2.wav after fft")

#' Clarify the sound
fft_data1_clarified = clarify_sound(fft_data1, rate1, 70, 3000, damping_factor=0.5, boost_factor=30)
fft_data2_clarified = clarify_sound(fft_data2, rate2, 70, 3000, damping_factor=0.9, boost_factor=50)

plt.figure(figure_frequency_domain_1.number)
figure_frequency_domain_1 = plot_frequency_domain(np.abs(fft_data1_clarified), freqs1, figure=figure_frequency_domain_1, legend="sound1.wav after clarification")
plt.figure(figure_frequency_domain_2.number)
figure_frequency_domain_2 = plot_frequency_domain(np.abs(fft_data2_clarified), freqs2, figure=figure_frequency_domain_2, legend="sound2.wav after clarification")

#' ifft 
# data1_ifft = my_ifft(fft_data1_clarified)
# data2_ifft = my_ifft(fft_data2_clarified)

# plt.figure(figure_frequency_domain_1.number)
# figure_time_domain_1 = plot_time_domain(data1_ifft, time1, figure=figure_figure_frequency_domain_domain_1, legend="sound1.wav after clarification")
# plt.figure(figure_frequency_domain_2.number)
# figure_time_domain_2 = plot_time_domain(data2_ifft, time2, figure=figure_figure_frequency_domain_domain_2, legend="sound2.wav after clarification")

#' remove noise
data_noise_removed1 = remove_noise(0, 70, fft_data1_clarified, rate1, damping_factor=0.001)
max_freq1 = index_to_freq(len(fft_data1)-1, rate1, len(fft_data1))
data_noise_removed1 = remove_noise(5000, max_freq1, data_noise_removed1, rate1, damping_factor=0.01)

data_noise_removed2 = remove_noise(0, 70, fft_data2_clarified, rate2, damping_factor=0.001)
max_freq2 = index_to_freq(len(fft_data2)-1, rate2, len(fft_data2))
data_noise_removed2 = remove_noise(5000, max_freq2, data_noise_removed2, rate2, damping_factor=0.01)

plt.figure(figure_frequency_domain_1.number)
figure_frequency_domain_1 = plot_frequency_domain(np.abs(data_noise_removed1), freqs1, figure=figure_frequency_domain_1, legend="sound1.wav after noise removal")
plt.figure(figure_frequency_domain_2.number)
figure_frequency_domain_2 = plot_frequency_domain(np.abs(data_noise_removed2), freqs2 , figure=figure_frequency_domain_2, legend="sound2.wav after noise removal")

#' ifft 
data_noise_removed1_ifft = my_ifft(data_noise_removed1)
data_noise_removed2_ifft = my_ifft(data_noise_removed2)

# figure_time_domain_1 = plot_time_domain(data_noise_removed1_ifft, time1, figure=figure_time_domain_1, legend="sound1.wav after")
# figure_time_domain_2 = plot_time_domain(data_noise_removed2_ifft, time2, figure=figure_time_domain_2, legend="sound2.wav after")

#' write to a wav file
data1_int16 = np.int16(data_noise_removed1_ifft * INT16_HALF_MAX)
data2_int16 = np.int16(data_noise_removed2_ifft * INT16_HALF_MAX)
wavfile.write('new_sound1.wav', rate1, data1_int16)
wavfile.write('new_sound2.wav', rate2, data2_int16) 



#' plotting
plt.figure(figure_time_domain_1.number)
figure_time_domain_1 = plot_time_domain(data_noise_removed1_ifft, time1, figure=figure_time_domain_1, legend="sound1.wav after")
figure_time_domain_1 = plot_time_domain(data1, time1, figure=figure_time_domain_1, legend="sound1.wav before")

plt.figure(figure_time_domain_2.number)
figure_time_domain_2 = plot_time_domain(data_noise_removed2_ifft, time2, figure=figure_time_domain_2, legend="sound2.wav after")
figure_time_domain_2 = plot_time_domain(data2, time2, figure=figure_time_domain_2, legend="sound2.wav before")

# plt.figure(figure_frequency_domain_1.number)
# figure_frequency_domain_1 = plot_frequency_domain(np.abs(data_noise_removed1), freqs1, figure=figure_frequency_domain_1, legend="sound1.wav after noise removal")
# figure_frequency_domain_1 = plot_frequency_domain(np.abs(fft_data1_clarified), freqs1, figure=figure_frequency_domain_1, legend="sound1.wav after clarification")
# figure_frequency_domain_1 = plot_frequency_domain(np.abs(fft_data1), freqs1, figure=figure_frequency_domain_1, legend="sound1.wav before")

# plt.figure(figure_frequency_domain_2.number)
# figure_frequency_domain_2 = plot_frequency_domain(np.abs(fft_data2_clarified), freqs2, figure=figure_frequency_domain_2, legend="sound2.wav after clarification")
# figure_frequency_domain_2 = plot_frequency_domain(np.abs(data_noise_removed2), freqs2 , figure=figure_frequency_domain_2, legend="sound2.wav after noise removal")
# figure_frequency_domain_2 = plot_frequency_domain(np.abs(fft_data2), freqs2 , figure=figure_frequency_domain_2, legend="sound2.wav before")


figure_time_domain_1.legend()
figure_time_domain_2.legend()
figure_frequency_domain_1.legend()
figure_frequency_domain_2.legend()

plt.show()

figure_time_domain_1.savefig("figures/" + title1 + ".svg", format='svg')
figure_frequency_domain_1.savefig("figures/" + title2 + ".svg", format='svg')
figure_time_domain_2.savefig("figures/" + title3 + ".svg", format='svg')
figure_frequency_domain_2.savefig("figures/" + title4 + ".svg", format='svg')
