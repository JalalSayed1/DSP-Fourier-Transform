from utils import *
from timefreqplot import *


def clarify_sound(fft_data, sampling_rate, low_freq=300, high_freq=3000, damping_factor=0.11, boost_factor=10):
    '''Clarifies the sound by damping all data then boosting the frequency spectrum between low_freq and high_freq.
    damping_factor: the factor to damp all frequencies (linear scale). Default is 0.1.
    boost_factor: the factor to boost the desired frequencies only (linear scale). Default is 10.
    '''

    low_index1, high_index1 = get_low_high_index(
        low_freq, high_freq, sampling_rate, len(fft_data))

    # ' Clarify:
    # damp all frequencies first then only boost the desired frequencies:
    fft_data_new = fft_data * damping_factor  # damp all frequencies
    fft_data_new[low_index1:high_index1] = fft_data_new[low_index1:high_index1] * \
        boost_factor  # boost the desired frequencies only

    return fft_data_new


def main():
    # read wav file:
    sampling_rate1, data1, freqs1, fft_data1, time1 = read_file(
        "original1cm.wav")
    sampling_rate2, data2, freqs2, fft_data2, time2 = read_file(
        "original1m.wav")

    print("sampling_rate1: ", sampling_rate1)
    print("sampling_rate2: ", sampling_rate2)

    fft_data_clarified1 = clarify_sound(
        fft_data1, sampling_rate1, 70, 3000, damping_factor=0.5, boost_factor=30)
    fft_data_clarified2 = clarify_sound(
        fft_data2, sampling_rate2, 70, 3000, damping_factor=0.9, boost_factor=50)

    # write wav file:
    write_wav("improved1cm.wav", sampling_rate1, fft_data_clarified1)
    write_wav("improved1m.wav", sampling_rate2, fft_data_clarified2)

    # plot freq domain before and after:
    figure_frequency_domain_1 = plt.figure()
    figure_frequency_domain_1 = plot_frequency_domain(np.abs(
        fft_data1), freqs1, legend="original1cm.wav", figure=figure_frequency_domain_1)
    figure_frequency_domain_1 = plot_frequency_domain(np.abs(
        fft_data_clarified1), freqs1, legend="improved1cm.wav", figure=figure_frequency_domain_1)

    figure_frequency_domain_2 = plt.figure()
    figure_frequency_domain_2 = plot_frequency_domain(np.abs(
        fft_data2), freqs2, legend="original1m.wav", figure=figure_frequency_domain_2)
    figure_frequency_domain_2 = plot_frequency_domain(np.abs(
        fft_data_clarified2), freqs2, legend="improved1m.wav", figure=figure_frequency_domain_2)

    # plot time domain before and after:
    figure_time_domain_1 = plt.figure()
    data_clarified1 = my_ifft(fft_data_clarified1)
    figure_time_domain_1 = plot_time_domain(
        data1, time1, legend="original1cm.wav", figure=figure_time_domain_1)
    figure_time_domain_1 = plot_time_domain(
        data_clarified1, time1, legend="improved1cm.wav", figure=figure_time_domain_1)

    figure_time_domain_2 = plt.figure()
    data_clarified2 = my_ifft(fft_data_clarified2)
    figure_time_domain_2 = plot_time_domain(
        data2, time2, legend="original1m.wav", figure=figure_time_domain_2)
    figure_time_domain_2 = plot_time_domain(
        data_clarified2, time2, legend="improved1m.wav", figure=figure_time_domain_2)

    figure_time_domain_1.legend()
    figure_time_domain_2.legend()
    figure_frequency_domain_1.legend()
    figure_frequency_domain_2.legend()

    plt.show()


if __name__ == "__main__":
    main()
