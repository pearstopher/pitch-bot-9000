# CS410 Computers Sound & Music
#
# Pitch Shifting Functions
#
# All of the pitch shifting functions we have tried are located below.
#
import numpy as np
import scipy.signal as signal
# import includes.helpers


##############################
# SHIFT 1 - Basic Linear Shift
##############################

def shift_linear(zxx, shift, largest_bins, sample_rate, segment_size):
    # this one is pretty simple:

    #   1. calculate the frequencies of each of the largest bins
    fundamentals = largest_bins * (sample_rate / segment_size)

    #   2. calculate the new frequencies from the fundamental frequencies
    new_fundamentals = fundamentals * (2 ** (shift / 12))

    #   3. calculate how far we need to shift the bins
    new_bins = new_fundamentals / (sample_rate / segment_size)

    bin_shifts = (new_bins - largest_bins).astype(int)  # round back to ints

    #   3. move each of the bins over by the correct amount
    new_zxx = np.roll(zxx, bin_shifts)

    #   4. clean up any frequencies that fall off the top or bottom
    for i, b in enumerate(bin_shifts):
        if b > 0:
            new_zxx[i, :b] = 0
        else:
            new_zxx[i, b:] = 0

    return new_zxx


#############################
# SHIFT 2 - Logarithmic Shift
#############################


def shift_log(zxx, shift):

    # the equation for shifting FFT bins is the same as the equation for shifting frequencies:
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

    # loop through the bins, copying them into their shifted location in the new array
    zxx_len = len(zxx)
    for i in range(zxx_len):
        new_index = int(i * (2**(shift/12)))
        if new_index < zxx_len:
            new_zxx[new_index] = zxx[i]

    return new_zxx


################################
# SHIFT 3 - Shift Peaks Together
################################

def shift_peaks(zxx, shift):
    # This function shifts the frequencies on the correct scale just like before.
    # The main difference is that it finds the locations of the peaks in the FFT
    #  and then moves the entire peaks instead of the individual bins.
    # This is helpful because it keeps the peaks from separating into individual
    #  frequencies like before.

    count = len(zxx[0])
    peaks = [[] for _ in range(count)]

    for i in range(count):
        # lots of parameters to play around with here:
        #   height, threshold, width, prominence
        #   https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
        peaks[i], _ = signal.find_peaks(np.reshape(np.absolute(zxx[:, i]), -1),
                                        height=3, prominence=10)

    # graph some random slices of the frequency domain to see if we have found the peaks
    # includes.helpers.graph_peaks(np.absolute(zxx[:, 10]), peaks[10])
    # includes.helpers.graph_peaks(np.absolute(zxx[:, 20]), peaks[20])

    # make a new empty STFT array to fill again like just like before
    new_zxx = np.zeros_like(zxx)

    # loop through the STFT data, one slice at a time
    for i in range(count):

        # for each slice, loop through the array of peak locations
        num_peaks = len(peaks[i])
        for j in range(num_peaks):

            # ascertain the relevant peak locations:

            # 1. find the start of the peak
            #    (halfway between current peak center and previous peak center)
            start = 0
            if j > 0:
                start = peaks[i][j] - int((peaks[i][j] - peaks[i][j-1]) / 2)
            # else:
            #    start = peaks[i][j] - 50

            # 2. find the center of the peak
            #    (that's just the peak)
            center = peaks[i][j]

            # 3. find the end of the peak
            #    (halfway between the current peak center and the next peak center)
            end = len(new_zxx) - 1
            if j < num_peaks - 1:
                end = peaks[i][j] + int((peaks[i][j+1] - peaks[i][j]) / 2)
            # else:
            #    end = peaks[i][j] + 50

            # now, calculate the new bin center location and offset
            new_center = int(center * (2 ** (shift / 12)))
            offset = new_center - center

            # and copy the entire old peak to the new array
            if start+offset >= 0 and end+offset < len(new_zxx):
                new_zxx[start+offset:end+offset, i] = zxx[start:end, i]
            # todo: add explicit case for when start/end exceeds array bounds

    # and return the new array at the end of course
    return new_zxx
