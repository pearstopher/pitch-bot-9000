# CS410 Computers, Sound, & Music
# Spring 2022
# Term Project: Pitch Bot 9000
#
# Members:
#   Christopher Juncker - juncker@pdx.edu
#   Clara Stickney - cstick2@pdx.edu
#

import scipy.io.wavfile as wf
import scipy.signal as signal
import numpy as np
import sys
import matplotlib.pyplot as plt


# default behavior with no arguments:
#   print instructions on how to run the program correctly
if len(sys.argv) != 3:
    print("Usage: pitchbot.py <'file.wav'> <'up'|'down'>\n")
    # print("Usage: pitchbot.py <'file.wav'> <'up'|'down'> <num_steps>\n")  # future


else:

    ##########################################
    # STEP 1: Preprocess commandline arguments
    ##########################################

    # read in the input WAV file
    file = sys.argv[1]
    sample_rate, samples = wf.read(file)

    # read in user specification of pitch direction
    shift = 1 if sys.argv[2] == 'up' else -1
    # shift *= sys.argv[3]  # multiply by num_steps (future)

    ####################################################################
    # STEP 2: Apply the Short Time Fourier Transform to the sample data.
    ####################################################################

    # the fast fourier transform will only tell us the single dominant frequency over
    # the whole file. Since we will be inputting files with multiple frequencies, we
    # need to discover the dominant frequencies at each location of the file. The
    # STFT will accomplish this for us by essentially just chopping the file up into
    # a bunch of segments and calculating the FFT  of each of them.

    # we can play around with segment size to see how it affects the results
    # current segment size:
    #   sample_rate/10 = each window is one tenth of a second long
    #   because the windows overlap, there will be 21 overlapping 0.1 second windows
    #   for a 1-second wav ( 21 == 10*2 + 1 )
    segment_size = int(sample_rate / 10)

    # apply the STFT to the samples using our segment size
    # f = frequency array, t = time array, zxx = fft data
    f, t, zxx = signal.stft(samples, fs=sample_rate, nperseg=segment_size)

    ################################################################################
    # STEP 3: Use pitch detection to determine the dominant frequencies in the file.
    ################################################################################

    # this is just like the Tuner homework except that a largest bin needs to be found
    # for every segment.
    largest_bins = np.argmax(np.abs(zxx), axis=0)

    # print the bins (temporarily) to confirm that we're getting the right frequencies
    for i, lb in enumerate(largest_bins):
        print("{0:.1f}".format(lb * (sample_rate / segment_size)))  # this is the bin-to-frequency equation

    # visualize the frequencies in the file (very slow, good for 1 second sine.wavs)
    plt.pcolormesh(t, f, np.abs(zxx), vmin=0, vmax=20, shading='gouraud')  # how to find vmax?
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

    # largest_bin = np.argmax(np.abs(fft))
    # frequencies = np.fft.rfftfreq(samples.size, d=1./sample_rate)
    # center_frequency = frequencies[largest_bin]

    #################################################################
    # STEP 4: Shift the detected frequencies in the desired direction
    #################################################################

    # the equation for shifting FFT bins is the same as the equation for shifting frequencies
    #   F_new = F * 2^(num_steps/12)
    #   B_new = B * 2^(num_steps/12)
    #
    # I built the whole unsimplified Bin shifting equation in Desmos
    #   https://www.desmos.com/calculator/2o3dkcudeh
    #
    # To shift the frequencies by n steps, we just need to shift all of the bins according to
    # the bin shifting equation above. Additionally, note that:
    #   1. the output of the equation will need to be rounded to the nearest integer because
    #      there is no such thing as a fraction of a bin.
    #   2. when shifting up, values that exceed the maximum frequency can simply be discarded
    #

    # make a new array with the same size as the old one (I love this function)
    new_zxx = np.empty_like(zxx)

    length = len(zxx)
    for i in range(length):
        index = int(i * (2**(shift/12)))
        if index < length:
            new_zxx[index] = zxx[i]

    largest_bins = np.argmax(np.abs(new_zxx), axis=0)

    # print the bins (temporarily) to confirm that we're getting the right frequencies
    for i, lb in enumerate(largest_bins):
        print("{0:.1f}".format(lb * (sample_rate / segment_size)))  # this is the bin-to-frequency equation


    """


    # Step 5: Apply the Inverse Fast Fourier Transform to convert the frequencies back into a new array of samples.
    result = np.fft.irfft(samples)

    # Step 6: Apply a filter over the final samples.

    # Step 7: Write the samples to a new WAV file on disk.
    wf.write('pitchified_' + file, sample_rate, result)
    """
