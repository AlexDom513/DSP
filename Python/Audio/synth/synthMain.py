from synthRunner import runner
import numpy as np

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
freq = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*freq/fs)).astype(np.float32)

run = runner(volume, fs, duration, freq, samples)
run.stream()