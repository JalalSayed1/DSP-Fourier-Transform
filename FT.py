import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter
from scipy.io import wavfile

# Constants
INT16_HALF_MAX = 2**15

def read_and_normalize_wav(filename):
    '''Reads a wav file and returns the normalized data, rate, and time axis.'''
    rate, data = wavfile.read(filename)
    data_normalized = data / INT16_HALF_MAX
    time_axis = np.linspace(0, len(data)/rate, num=len(data))
    return rate, data_normalized, time_axis

def plot_frequency_domain(rate, data, title):
    '''Plots the frequency spectrum in dB scale.'''
    plt.figure()
    half_data_length = int(len(data)/2)
    fft_data = np.abs(np.fft.fft(data[:, 0])[0:half_data_length]) / len(data)
    fft_data_db = 20 * np.log10(fft_data)
    freqs = np.linspace(0, rate/2, num=half_data_length)
    
    plt.semilogx(freqs, fft_data_db)
    plt.grid(True)
    
    axes = plt.gca()
    axes.xaxis.set_major_formatter(LogFormatter(labelOnlyBase=False))
    
    # Add grid for all x-axis values
    axes.xaxis.grid(True, which='both')  # This line ensures the grid for both major and minor ticks
    # ax.yaxis.grid(True)
    
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.title(title)
    # plt.show()

# Read and normalize wav file
rate1, data1, time1 = read_and_normalize_wav('sound1.wav')
rate2, data2, time2 = read_and_normalize_wav('sound2.wav')

# Plot in the frequency domain
plot_frequency_domain(rate1, data1, 'sound1.wav')
plot_frequency_domain(rate2, data2, 'sound2.wav')

plt.show()
