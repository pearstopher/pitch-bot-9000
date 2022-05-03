# Christopher Juncker - juncker@pdx.edu
# Clara Stickney - cstick2@pdx.edu 
# CS 410P - Spring 2022
# Term Project: Pitch Bot 9000

import scipy.io.wavfile as wf
import scipy.fft
from scipy import signal
import numpy as np
import sys


if (len(sys.argv) == 3):
    # Step 1: Preprocess commandline arguments
    #   - Read in the input WAV file
    #   - Read in user specification of pitch direction
    filename = sys.argv[1]
    s, samples = wf.read(filename)
    direction = sys.argv[2]

    # Step 2: Apply the Fast Fourier Transform to the sample data.
    fft = scipy.fft.rfft(samples)

    # Step 3: Use pitch detection to determine the dominant frequencies in the file.
    #   - Apply window? Other junk? Yee?
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
    wf.write('pitchified_' + filename, s, result)