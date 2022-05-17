# CS410 Computers Sound & Music
#
# Filtering Functions
#
# All of our filtering functions are located below.
#
import scipy.signal as signal


# references: https://github.com/pdx-cs-sound/hw-resample, assignment #2
def low_pass(samples, cutoff = 0.95):
    # this generates the filter window parameters
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.kaiserord.html
    #
    # Parameters:
    #   ripple: -40 = upper bound for deviation between Desired and Actual frequency response
    #   width: 0.05 = width of transition band, expressed as a fraction of nyquist frequency
    #
    # Return values:
    #   numtaps = length of window, number of samples
    #   beta = number which determines window shape
    #       (often expressed as "alpha", where beta = pi * alpha)
    numtaps, beta = signal.kaiserord(-40, 0.05)

    # this accepts the window parameters and generates the array of coefficients
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html
    #
    # cutoff: 0.45 = the cutoff frequency, fraction of total frequency (1)
    #   total frequencies remaining = cutoff + transition band length
    #
    # scale: True = ??? Still don't understand the scale argument yet. What is "unity"?
    subband = signal.firwin(numtaps, cutoff, window=('kaiser', beta), scale=True)

    # Convolve the original samples with the subband
    # (written by hand for assignment 2 but much faster with np.convolve or signal.convolve)
    samples = signal.convolve(samples, subband)
    samples = samples.astype("int16")  # (lost our int16s)
    # samples = samples[0::2]

    return samples
