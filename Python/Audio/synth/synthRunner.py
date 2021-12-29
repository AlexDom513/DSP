#https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python

import pyaudio
import numpy as np

class runner:
    def __init__(self, volume, fs, duration, freq, samples):
        self.volume = volume
        self.fs = fs
        self.duration = duration
        self.freq = freq
        self.samples = samples
        self.player = pyaudio.PyAudio()

    def stream(self):
        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = self.player.open(format=pyaudio.paFloat32,
                channels=1,
                rate=self.fs,
                output=True)
        # play. May repeat with different volume values (if done interactively) 
        stream.write(self.volume*self.samples)

        # stop stream (6)
        stream.stop_stream()
        stream.close()

        # close PyAudio (7)
        #self.player.terminate()