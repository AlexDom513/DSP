#goal: develop a program(simulator) where we can test different waveforms and implement different types of filtering/algorithms

#useful links/resources
#https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python (notice 2nd response: include .tobytes())

import pyaudio
import numpy as np

class runner:
    def __init__(self, volume, fs, freq, duration):
        self.volume = volume
        self.fs = fs
        self.freq = freq
        self.numSamples = None
        self.samples = None
        self.duration = duration
        self.player = pyaudio.PyAudio()

    def convertFreq(self, freq):
        self.freq = freq
        self.numSamples = np.round(self.fs / self.freq)

    def generateSamples(self):
        num = self.numSamples
        n = np.linspace(0,num,num = num)
        x = np.sin(2*np.pi*n)
        x = x[:-1]
        repeat = np.ceil((1 + self.fs / num) * self.duration)
        samples = np.tile(x,repeat)


        print(len(samples))
        print(1.0* len(samples) / (self.fs))

        self.samples = samples.astype(np.float32).tobytes()

    def stream(self):

        stream = self.player.open(format=pyaudio.paFloat32,
                channels=1,
                rate=self.fs,
                output=True)

        # play. May repeat with different volume values (if done interactively) 
        stream.write(self.samples)
        stream.start_stream()

        # stop stream (6) maybe also place this somewhere else, an end event
        stream.stop_stream()
        stream.close()

        # close PyAudio (7), we will need to actually re-add this in somehow
        #self.player.terminate()