import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter
from scipy.io import wavfile

# Constant.
INT16_HALF_MAX = 2**15

def read_and_normalize_wav(filename):
    '''Reads a wav file and returns the normalized data, rate, and time axis.'''
    rate, data = wavfile.read(filename)
    data_normalized = data / INT16_HALF_MAX
    time_axis = np.linspace(0, len(data)/rate, num=len(data))
    return rate, data_normalized, time_axis

def my_fft(data, rate):
    '''Returns the frequency spectrum of the data.'''
    # half_data_length = int(len(data)/2)
    fft_data = (np.fft.fft(data[:, 0])) / len(data) #![0:half_data_length]
    # freqs = np.linspace(0, rate/2, num=half_data_length)
    freqs = np.linspace(0, rate/2, num=len(data))
    return freqs, fft_data

def plot_frequency_domain(fft_data, freqs, title):
    '''Plots the frequency spectrum in dB scale.'''
    plt.figure()
    
    # for plotting purposes, only plot the first half of the data so we don't see the mirror:
    fft_data = fft_data[:int(len(fft_data)/2)]
    freqs = freqs[:int(len(freqs)/2)]
    
    fft_data_db = 20 * np.log10(fft_data)
    
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

def plot_time_domain(data, time_axis, title):
    '''Plots the time domain.
    data: raw data (not fft data)
    '''
    plt.figure()
    # data_db = 20 * np.log10(data)
    plt.plot(time_axis, data)
    plt.grid(True)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(title)
    # plt.show()

def freq_to_index(freq, sampling_rate, data_length):
    '''Returns the index of the frequency in the frequency spectrum.'''
    return int(freq / (sampling_rate/2) * data_length)

def index_to_freq(index, sampling_rate, data_length):
    '''Returns the frequency of the index in the frequency spectrum.'''
    return index / data_length * (sampling_rate/2)

def clarify_sound(fft_data, sampling_rate, low_freq, high_freq, damping_factor = 0.1, boost_factor = 100_000_000):
    '''Clarifies the sound by damping all data then boosting the frequency spectrum between low_freq and high_freq.
    damping_factor: the factor to damp all frequencies (linear scale). Default is 0.1.
    boost_factor: the factor to boost the desired frequencies only (linear scale). Default is 10.
    '''
    
    # index = freq/nyquist freq * number of samples. Nyquist freq = 1/2 * sampling rate 
    low_index = freq_to_index(low_freq, sampling_rate, len(fft_data))
    high_index = freq_to_index(high_freq, sampling_rate, len(fft_data))
    
    # damp all frequencies first then only boost the desired frequencies:
    fft_data *= damping_factor # damp all frequencies
    fft_data[low_index:high_index] *= boost_factor # boost the desired frequencies only
    
    return fft_data

def remove_noise(low_freq, high_freq, data, sampling_rate, damping_factor = 0.01):
    '''Removes noise by damping the frequency spectrum between low_freq and high_freq.'''
    
    low_index = freq_to_index(low_freq, sampling_rate, len(data))
    high_index = freq_to_index(high_freq, sampling_rate, len(data))
    
    data[low_index:high_index] *= damping_factor
    
    return data
    

#' Read and normalize wav file
rate1, data1, time1 = read_and_normalize_wav('sound1.wav')
rate2, data2, time2 = read_and_normalize_wav('sound2.wav')

# plot_time_domain(data1, time1, "Original Time domain of sound1.wav")
# plot_time_domain(data2, time2, "Original Time domain of sound2.wav")

#' Plot in the frequency domain
freqs1, fft_data1 = my_fft(data1, rate1)
freqs2, fft_data2 = my_fft(data2, rate2)

plot_frequency_domain(np.abs(fft_data1), freqs1, "Frequency domain of sound1.wav")
plot_frequency_domain(np.abs(fft_data2), freqs2, "Frequency domain of sound2.wav")

#' Clarify the sound
fft_data1_clarified = clarify_sound(fft_data1, rate1, 1000, 5000, damping_factor=0.11)
fft_data2_clarified = clarify_sound(fft_data2, rate2, 1000, 5000, damping_factor=0.11)

# plot_frequency_domain(np.abs(fft_data1_clarified), freqs1, f"Frequency domain of sound1.wav after clarification")
# plot_frequency_domain(np.abs(fft_data2_clarified), freqs2, "Frequency domain of sound2.wav after clarification")

#' ifft again
data1_ifft = np.fft.ifft(fft_data1_clarified)
data2_ifft = np.fft.ifft(fft_data2_clarified)

# plot_time_domain(data1_ifft, time1, f"Time domain of sound1.wav after clarification")
# plot_time_domain(data2_ifft, time2, "Time domain of sound2.wav after clarification")

#' remove noise
data_noise_removed1 = remove_noise(0, 70, fft_data1, rate1)
data_noise_removed1 = remove_noise(10000, index_to_freq(len(fft_data1)-1, rate1, len(fft_data1)), data_noise_removed1, rate1)
data_noise_removed2 = remove_noise(0, 70, fft_data2, rate2)
data_noise_removed2 = remove_noise(10000, index_to_freq(len(fft_data2)-1, rate2, len(fft_data2)), data_noise_removed2, rate2)

plot_frequency_domain(np.abs(data_noise_removed1), freqs1, "Frequency domain of sound1.wav after noise removal")
plot_frequency_domain(np.abs(data_noise_removed2), freqs2 , "Frequency domain of sound2.wav after noise removal")


data_noise_removed1_ifft = np.fft.ifft(data_noise_removed1)
data_noise_removed2_ifft = np.fft.ifft(data_noise_removed2)

plot_time_domain(data_noise_removed1_ifft, time1, "Time domain of sound1.wav after noise removal")
plot_time_domain(data_noise_removed2_ifft, time2, "Time domain of sound2.wav after noise removal")

#' write to a wav file
data1_int16 = np.int16(data_noise_removed1_ifft * INT16_HALF_MAX)
data2_int16 = np.int16(data_noise_removed2_ifft * INT16_HALF_MAX)
wavfile.write('new_sound1.wav', rate1, data1_int16)
wavfile.write('new_sound2.wav', rate2, data2_int16)



plt.show()
