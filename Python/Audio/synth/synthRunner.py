#goal: develop a program(simulator) where we can test different waveforms and implement different types of filtering/algorithms
#refer to prototyping file for explanantion of how the samples are generated

#useful links/resources:
#https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python (notice 2nd response: include .tobytes())

import pyaudio
import numpy as np

class runner:
    def __init__(self, fs, freq, duration):
        self.fs = fs
        self.freq = freq
        self.duration = duration
        self.disp = []
        self.numSamples = None
        self.samples = None
        self.repeat = None
        self.player = pyaudio.PyAudio()

    def convertFreq(self, freq):
        self.freq = freq
        self.numSamples = np.round(self.fs / self.freq)
        self.repeat = np.ceil((1 + self.fs / self.numSamples) * self.duration)

    def sine(self):
        num = self.numSamples
        n = np.linspace(0,num,num = num)
        x = np.sin(2*np.pi*n)
        x = x[:-1]
        samples = np.tile(x,self.repeat)
        self.disp = samples
        self.samples = samples.astype(np.float32).tobytes()

    def saw(self):
        num = self.numSamples
        n = np.linspace(0,num,num = num)
        n = n[:-1]
        samples = np.tile(n,self.repeat)
        self.disp = samples
        self.samples = samples.astype(np.float32).tobytes()

    def triangle(self):
        num = self.numSamples
        numHalf = round(num/2)
        n1 = np.linspace(0,numHalf,num = numHalf)
        n2 = np.linspace(numHalf,2*numHalf,num = numHalf)
        n2 = n2[::-1]
        n2 = n2-numHalf
        n = np.concatenate((n1, n2), axis=0)
        n = n[:-1]
        samples = np.tile(n,self.repeat)
        self.disp = samples
        self.samples = samples.astype(np.float32).tobytes()

    def noise(self):
        num = self.numSamples
        x = np.random.randn(num)
        x = x[:-1]
        samples = np.tile(x,self.repeat)
        self.disp = samples
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