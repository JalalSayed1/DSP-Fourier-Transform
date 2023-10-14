# Digital Signal Processing Fourier

# Transform – Assignment 1

Report written by:
Team2014: Tamim Abdul Maleque(2523948a) and Jalal Sayed(2571964s)

GitHub repo: github.com/JalalSayed1/DSP-Fourier-Transform/tree/master

## Introduction

This assignment involves signal processing on two audio files, 'sound1.wav' and 'sound2.wav',
recorded at different distances. The sounds were transformed from the time domain to the
frequency domain using a Fast Fourier Transform (FFT). In the frequency domain, the sounds were
enhanced by dampening all frequencies and then boosting specific frequency ranges to improve
clarity. Noise in certain frequency bands was suppressed. Following these modifications, an Inverse
Fast Fourier Transform (IFFT) was applied to convert the signals back to the time domain. The
processed audio was then written to new WAV files.

## Description

### Fundamental Frequencies of Vowels and Frequency Range of Consonants

**Fundamental Frequency** : This is the primary or lowest frequency of a periodic waveform. It
determines the basic pitch or tone of the signal. The identified fundamental vowel frequencies were
the frequency peak seen in the 70 Hz to 400Hz.

**Harmonics** : These are integer multiples of the fundamental frequency. The amplitude of harmonics
decreases as their frequency increases due to energy distribution. The energy gets distributed over a
wider range of frequencies as frequency increases and hence a lower amplitude in the harmonic
frequencies.

![Frequency domain for sound1 and 2](https://github.com/JalalSayed1/DSP-Fourier-Transform/assets/92950538/f61bf1c1-0288-4dc3-b052-8180d6ec3382)

**Figure 1:** The plots show the annotated Frequency Domain of the Audio Signal identifying the peak vowels,
consonants, and noise for **(a) Left:** sound recorded approximately 1 m away and **(b) Right:** sound recorded
approximately 1 cm away.


### Speech Audio Improvement

To clarify the voice recording, all range of the sound was damped first then a certain range of
frequency boosted. The methodology was implemented to damp all signals first to soften the audio
and boosted in the frequency range of 70 Hz to 3000Hz so that the human speech would be audible.

**Table 1:** The chosen factors for speech audio improvement.

| Sound Name  | Damping Factor | Boosting Factor | Clarified Frequency (70Hz to 3000Hz) <br/> Audio Overall Boosting |
|------------|----------------|-----------------|---------------------------------------------------------------|
| original1cm.wav | x 0.5           | x 30         | x 15                                                          |
| original1m.wav | x 0.9           | x 50         | x 45                                                          |

Table 1 above shows the chosen factors in the sound clarification section of our laboratory. The
damping factor of sound1.wav has a higher dampening effect than sound2.wav. This is due to the
original sound2.wav being recorded further away hence being softer already.

The boosting factor for the specified frequency for sound1.wav has a lower boosting effect than
sound2.wav. This is due to sound1.wav original audio being clearer than sound2.wav. The boosting
factor is a multiple so that our desired frequency range would be within the amplitude peaks of the
fundamental vowel frequency amplitudes.

The choosing of the clarified frequency range was selected to boost the range of frequency that
contained the vowels and the consonants allowing better clarity in the processed audio signal. This
frequency is also noted to be around the voice range frequency of an human speaking voice.

### Audio Noise Removal

We damped the frequencies between 0 and 70 Hz by 0. 001 for both sound files. This is because
when we used a bigger value (less damping), there was a hissing noise in the audio. We kept
decreasing this value until this noise disappeared and the voice quality improved. We needed to
damp this region by so much because the noise power was relatively high compared to the voice.
One of the reasons we had this high noise in our audio file was because of the microphone quality to
capture the audio. We also damped all frequencies greater than 10 KHz as it was mainly noise as
well.

As a result, the voice clarity and richness of boosted. Background noise minimized and the overall
quality improved.


## Conclusion

In conclusion this assignment successfully demonstrated the use of Scipy and Numpy Python libraries
to do audio signal processing on two sound waves.

In Figure 2 below, for the frequency spectrum of both sound the frequency amplitudes have shifted
for different audio processing. In noise removal (sound damping) the amplitude in dB becomes more
negative, whereas for boosting (sound enhancement) the amplitude is higher value.

![Time domain of sound2 wav before and after noise removal](https://github.com/JalalSayed1/DSP-Fourier-Transform/assets/92950538/f9cc72a6-86ba-418d-b421-956e573a417b)
![Time domain of sound1 wav before and after noise removal](https://github.com/JalalSayed1/DSP-Fourier-Transform/assets/92950538/6f5399cd-0361-417c-bce0-1fb35e472605)

**Figure 2 :** The time -domain plot of the audio signal **(a) Above:** plot shows the sound recorded approximately
1 m away **(b) Below:** plot shows the sound recorded approximately 1 cm away. _Blue graph is noise removed
audio and orange graph is original non-processed audio._

![Frequency domain of original1mwav before and after noise removal](https://github.com/JalalSayed1/DSP-Fourier-Transform/assets/92950538/394676a6-f657-4062-89b3-d04071dedf4e)
![Frequency domain of original1cm wav before and after noise removal](https://github.com/JalalSayed1/DSP-Fourier-Transform/assets/92950538/3659f29f-13f1-46a6-81cc-e67a64ff5527)

**Figure 3 :** The frequency - domain plot of the audio signal showing the three stages of audio processing on
different frequencies. **_(a) Above_** : plot shows the sound recorded approximately 1 m away **_(b) Below_** : plot shows
the sound recorded approximately 1 cm away. _Blue graph is original non-processed audio, orange graph is
improved speech audio and green graph is noise removed audio._

In Figure 3 above, we present the time-domain representations of both the original and processed
audio signals. While the processed data exhibits increased amplitudes to enhance volume, noise
filtering has attenuated certain peaks. Despite these modifications, the overall duration and pattern
remain consistent, indicating no evidence of audio signal clipping.

## References

https://www.physicsclassroom.com/class/sound/Lesson-4/Fundamental-Frequency-and-Harmonics.

(Accessed 13/10/2023)
