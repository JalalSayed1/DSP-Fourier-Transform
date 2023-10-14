from utils import *
from improver import *
from timefreqplot import *


def remove_noise(fft_data, sampling_rate, low_freq, high_freq, damping_factor=0.01):
    '''Removes noise by damping the frequency spectrum between low_freq and high_freq.'''

    low_index1, high_index1 = get_low_high_index(
        low_freq, high_freq, sampling_rate, len(fft_data))

    # ' Remove noise:
    fft_data[low_index1:high_index1] *= damping_factor

    return fft_data


def main():
    # read wav file:
    sampling_rate1, data1, freqs1, fft_data1, time1 = read_file(
        "original1cm.wav")
    sampling_rate2, data2, freqs2, fft_data2, time2 = read_file(
        "original1m.wav")

    max_freq1 = index_to_freq(len(fft_data1)-1, sampling_rate1, len(fft_data1))
    max_freq2 = index_to_freq(len(fft_data2)-1, sampling_rate2, len(fft_data2))

    # clarify sound:
    fft_data_clarified1 = clarify_sound(
        fft_data1, sampling_rate1, 70, 3000, damping_factor=0.5, boost_factor=30)
    fft_data_clarified2 = clarify_sound(
        fft_data2, sampling_rate2, 70, 3000, damping_factor=0.9, boost_factor=50)

    fft_data_noise_removed1 = remove_noise(
        fft_data_clarified1, sampling_rate1, 0, 70, 0.001)
    fft_data_noise_removed1 = remove_noise(
        fft_data_clarified1, sampling_rate1, 5000, max_freq1, 0.01)

    fft_data_noise_removed2 = remove_noise(
        fft_data_clarified2, sampling_rate2, 0, 70, 0.001)
    fft_data_noise_removed2 = remove_noise(
        fft_data_clarified2, sampling_rate2, 5000, max_freq2, 0.01)

    # write wav file:
    write_wav("noiseremoved1cm.wav", sampling_rate1, fft_data_clarified1)
    write_wav("noiseremoved1m.wav", sampling_rate2, fft_data_clarified2)

    # plot freq domain before and after:
    figure_frequency_domain_1 = plt.figure()
    figure_frequency_domain_1 = plot_frequency_domain(np.abs(
        fft_data1), freqs1, legend="original1cm.wav", figure=figure_frequency_domain_1)
    figure_frequency_domain_1 = plot_frequency_domain(np.abs(
        fft_data_noise_removed1), freqs1, legend="noiseremoved1cm.wav", figure=figure_frequency_domain_1)

    figure_frequency_domain_2 = plt.figure()
    figure_frequency_domain_2 = plot_frequency_domain(np.abs(
        fft_data2), freqs2, legend="original1m.wav", figure=figure_frequency_domain_2)
    figure_frequency_domain_2 = plot_frequency_domain(np.abs(
        fft_data_noise_removed2), freqs2, legend="noiseremoved1m.wav", figure=figure_frequency_domain_2)

    # plot time domain before and after:
    figure_time_domain_1 = plt.figure()
    data_noise_removed1 = my_ifft(fft_data_noise_removed1)
    figure_time_domain_1 = plot_time_domain(
        data1, time1, legend="original1cm.wav", figure=figure_time_domain_1)
    figure_time_domain_1 = plot_time_domain(
        data_noise_removed1, time1, legend="noiseremoved1cm.wav", figure=figure_time_domain_1)

    figure_time_domain_2 = plt.figure()
    data_noise_removed2 = my_ifft(fft_data_noise_removed2)
    figure_time_domain_2 = plot_time_domain(
        data2, time2, legend="original1m.wav", figure=figure_time_domain_2)
    figure_time_domain_2 = plot_time_domain(
        data_noise_removed2, time2, legend="noiseremoved1m.wav", figure=figure_time_domain_2)

    figure_time_domain_1.legend()
    figure_time_domain_2.legend()
    figure_frequency_domain_1.legend()
    figure_frequency_domain_2.legend()

    plt.show()


if __name__ == "__main__":
    main()
