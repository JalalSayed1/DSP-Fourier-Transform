from scipy.io import wavfile
import numpy as np

# Constant
INT16_HALF_MAX = 2**15


def read_and_normalize_wav(filename):
    '''Reads a wav file and returns the normalized data, rate, and time axis.'''
    rate, data = wavfile.read(filename)
    data_normalized = data[:, 0] / INT16_HALF_MAX
    time_axis = np.linspace(0, len(data)/rate, num=len(data))
    return rate, data_normalized, time_axis


def read_file(filename):
    sampling_rate, data, time = read_and_normalize_wav(filename)
    freqs, fft_data = my_fft(data, sampling_rate)
    return sampling_rate, data, freqs, fft_data, time


def get_low_high_index(low_freq, high_freq, sampling_rate, len_of_data):
    # index = freq/nyquist freq * number of samples. Nyquist freq = 1/2 * sampling rate
    low_index = freq_to_index(low_freq, sampling_rate, len_of_data)
    high_index = freq_to_index(high_freq, sampling_rate, len_of_data)
    return low_index, high_index


def write_wav(filename, rate, fft_data):
    '''Writes a wav file.
    filename: must end with .wav'''
    data = my_ifft(fft_data)
    data_int16 = np.int16(data * INT16_HALF_MAX)
    wavfile.write(filename, rate, data_int16)


def my_fft(data, rate):
    '''Returns the frequency spectrum of the data.'''
    fft_data = (np.fft.fft(data)) / len(data)
    freqs = np.linspace(0, rate/2, num=len(data))
    return freqs, fft_data


def my_ifft(fft_data):
    '''Returns the time domain of the frequency spectrum.'''
    return np.fft.ifft(fft_data) * len(fft_data)


def freq_to_index(freq, sampling_rate, data_length):
    '''Returns the index of the frequency in the frequency spectrum.'''
    return int(freq / (sampling_rate/2) * data_length)


def index_to_freq(index, sampling_rate, data_length):
    '''Returns the frequency of the index in the frequency spectrum.'''
    return int(index / data_length * (sampling_rate/2))


def save_svg(filename, figure):
    '''Saves the figure as an svg file.
    filename: must end with .svg'''
    figure.savefig(filename, format="svg")
