# CS410 Computers Sound & Music
#
# Pitch Shifting Functions
#
# All of the pitch shifting functions we have tried are located below.
#
import numpy as np


##############################
# SHIFT 1 - Basic Linear Shift
##############################

def shift_linear(zxx, shift, fundamental):
    # this one is pretty simple:
    #   1. calculate the new frequency from the fundamental frequency
    #   2. calculate how far we need to shift the bins
    #   3. move all of the bins over by that amount
    #   4. clean up any frequencies that fall off the top or bottom
    return

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


###############
# SHIFT 3 - ...
###############

# ...
