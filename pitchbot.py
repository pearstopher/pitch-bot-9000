# CS410 Computers, Sound, & Music
# Spring 2022
# Term Project: Pitch Bot 9000
#
# Members:
#   Christopher Juncker - juncker@pdx.edu
#   Clara Stickney - cstick2@pdx.edu
#

import scipy.io.wavfile as wf
import scipy.fft
from scipy import signal
import numpy as np
import sys


# default behavior with no arguments:
#   print instructions on how to run the program correctly
if len(sys.argv) != 3:
    print("Usage: pitchbot.py <'file.wav'> <'up'|'down'>\n")
    # print("Usage: pitchbot.py <'file.wav'> <'up'|'down'> <num_steps>\n")  # future


else:

    # STEP 1: Preprocess commandline arguments

    # read in the input WAV file
    file = sys.argv[1]
    sample_rate, samples = wf.read(file)

    # read in user specification of pitch direction
    shift = 1 if sys.argv[2] == 'up' else -1
    # shift *= sys.argv[3]  # multiply by num_steps (future)

    # STEP 2: Apply the Fast Fourier Transform to the sample data.
    fft = scipy.fft.rfft(samples)

    # Step 3: Use pitch detection to determine the dominant frequencies in the file.
    #   - Apply window? Other junk? Yee?
    #
    """
    magnitude = np.abs(fft)
    largest_bin = np.argmax(magnitude)
    center_freq = largest_bin * (s / length)
    """

    # Step 4: Shift the detected frequencies in the desired direction.

    # Step 5: Apply the Inverse Fast Fourier Transform to convert the frequencies back into a new array of samples.
    result = np.fft.irfft(samples)

    # Step 6: Apply a filter over the final samples.

    # Step 7: Write the samples to a new WAV file on disk.
    wf.write('pitchified_' + file, sample_rate, result)
