from utils import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogFormatter


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
    plt.title("Frequency domain with " + legend)

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
    plt.title("Time domain with " + legend)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    # plt.show()

    return figure


def main():
    # read wav file:
    sampling_rate1, data1, freqs1, fft_data1, time1 = read_file(
        "original1cm.wav")
    sampling_rate2, data2, freqs2, fft_data2, time2 = read_file(
        "original1m.wav")

    # plot freq domain
    plot_frequency_domain_1 = plt.figure()
    # plot_frequency_domain_1.title
    plot_frequency_domain_1 = plot_frequency_domain(np.abs(
        fft_data1), freqs1, legend="original1cm.wav", figure=plot_frequency_domain_1)

    plot_frequency_domain_2 = plt.figure()
    plot_frequency_domain_2 = plot_frequency_domain(np.abs(
        fft_data2), freqs2, legend="original1m.wav", figure=plot_frequency_domain_2)

    # plot time domain
    plot_time_domain_1 = plt.figure()
    plot_time_domain_1 = plot_time_domain(
        data1, time1, legend="original1cm.wav", figure=plot_time_domain_1)

    plot_time_domain_2 = plt.figure()
    plot_time_domain_2 = plot_time_domain(
        data2, time2, legend="original1m.wav", figure=plot_time_domain_2)

    plot_time_domain_1.legend()
    plot_time_domain_2.legend()
    plot_frequency_domain_1.legend()
    plot_frequency_domain_2.legend()

    plt.show()


if __name__ == "__main__":
    main()
