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
import includes.helpers
import includes.shift

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
    includes.helpers.graph(t, f, zxx)

    # largest_bin = np.argmax(np.abs(fft))
    # frequencies = np.fft.rfftfreq(samples.size, d=1./sample_rate)
    # center_frequency = frequencies[largest_bin]

    #################################################################
    # STEP 4: Shift the detected frequencies in the desired direction
    #################################################################

    # the pitch shifting algorithm is one of the most important parts of our program.
    # we have tried multiple algorithms (all discussed in README.md) and all of our
    # code for these algorithms is contained in 'includes/shift.py'.
    #
    # Each function in 'shift.py' accepts STFT data as it's first argument and
    # returns another STFT array which has been modified with the goal of shifting
    # the pitch by the specified amount.

    # Shift 1: Linear Shift
    # new_zxx = includes.shift.shift_linear(zxx, shift, largest_bins, sample_rate, segment_size)

    # Shift 2: Log Scaled Shift
    new_zxx = includes.shift.shift_log(zxx, shift)

    # Shift 3: TBD

    # find the largest bins again for a sanity check (same code as earlier)
    largest_bins = np.argmax(np.abs(new_zxx), axis=0)

    # print the bins (temporarily) to confirm that we're getting the right frequencies
    for i, lb in enumerate(largest_bins):
        print("{0:.1f}".format(lb * (sample_rate / segment_size)))  # this is the bin-to-frequency equation

    #############################################################################
    # STEP 5: Apply the Inverse FFT to convert the frequencies back into samples.
    #############################################################################

    # call the inverse short time fourier transform on our new shifted FFT data
    _, new_samples = signal.istft(new_zxx, fs=sample_rate)

    # play the original and the shifted sound, one after the other
    includes.helpers.play(samples, sample_rate)
    includes.helpers.play(new_samples, sample_rate)

    # do the fft again on our new samples to print a new spectrogram and see what the damage is
    f, t, zxx = signal.stft(new_samples, fs=sample_rate, nperseg=segment_size)
    includes.helpers.graph(t, f, zxx)

    ###############################################
    # STEP 6: Apply a filter over the final samples
    ###############################################

    # Whenever we are modifying the FFT bins, the resulting audio needs to be filtered with
    # a low-pass filter to make sure that no high frequencies were added during the audio
    # reconstruction process. This is especially important when changing the sample rate of
    # the audio, but it is a good practice regardless.


    """


    # Step 6: Apply a filter over the final samples.

    # Step 7: Write the samples to a new WAV file on disk.
    wf.write('pitchified_' + file, sample_rate, result)
    """
