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
    #   ( 21 == 10*2 + 1 )
    segment_size = int(sample_rate / 20)

    # apply the STFT to the samples using our segment size
    # f = frequency array, t = time array, zxx = fft data
    f, t, zxx = signal.stft(samples, fs=sample_rate, nperseg=segment_size)

    ################################################################################
    # STEP 3: Use pitch detection to determine the dominant frequencies in the file.
    ################################################################################

    # this is just like the Tuner homework except that a largest bin needs to be found
    # for every segment.
    largest_bins = np.argmax(np.abs(zxx), axis=0)
    # print(len(largest_bins))
    # for i in largest_bins:
    #     print(i)
    for i, lb in enumerate(largest_bins):
        print("{0:.1f}".format(lb * (sample_rate / segment_size)))  # this is the bin-to-frequency equation

    # throw in a graph to see it. very slow, good for 1 second sine.wavs
    plt.pcolormesh(t, f, np.abs(zxx), vmin=0, vmax=20, shading='gouraud')  # how to find vmax?
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

    # largest_bin = np.argmax(np.abs(fft))
    # frequencies = np.fft.rfftfreq(samples.size, d=1./sample_rate)
    # center_frequency = frequencies[largest_bin]
    """

    # Step 4: Shift the detected frequencies in the desired direction.

    # Step 5: Apply the Inverse Fast Fourier Transform to convert the frequencies back into a new array of samples.
    result = np.fft.irfft(samples)

    # Step 6: Apply a filter over the final samples.

    # Step 7: Write the samples to a new WAV file on disk.
    wf.write('pitchified_' + file, sample_rate, result)
    """
