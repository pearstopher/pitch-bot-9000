# CS410 Computers Sound & Music
#
# Helper Functions
#
# This is just a place to keep some extra little functions out of the way
#
import numpy as np
import pyaudio
import scipy.io.wavfile as wf


def play(samples, sample_rate):
    # this should only be used when bytes are set to 16
    # don't convert the original samples, they will be reused
    s = samples.astype(np.int16)  # np.Float32, etc

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,  # paFloat32, etc
                    channels=1,
                    rate=sample_rate,
                    output=True)
    stream.write(s.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()


# write the samples to disk
def write(samples, sample_rate, file="default.wav"):
    s = samples.astype(np.int16)
    wf.write(file, sample_rate, s)
