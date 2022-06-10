import numpy as np
from scipy import signal
from reverb import verb


#purpose of Oscillator class is to generate waveforms, generated waveforms can then be rendered by the synthesizer
#each oscillator created will represent a different pitch, timbre, etc.
class Oscillator:
    
    def __init__(self, rate, n_chunk, freq, type, gain=0.1):
        self.rate = rate                            #sampling rate (typically 44100 Hz)
        self.n_chunk = n_chunk                      #chunk size (typically 1024 samples), process audio signals as chunks
        self.freq = freq                            #signal frequency
        self.gain = gain                            #signal gain
        self.state = False                          #oscillator active
        self.pi2_t0 = 2 * np.pi / (rate / freq)     #angular frequency
        self.offset = 0                             #offset between chunks
        self.period = n_chunk * rate                #signal period
        self.change_waveform(type)                  #specify if waveform is sine/saw
        self.reverbModifier = verb()                #declare reverb object that we will use to modify our chunk

    def out(self):
        x =  np.arange(self.offset, self.offset + self.n_chunk)     #generate timesteps (offset, offset+chunk)
        chunk = self.gain * self.generator(self.pi2_t0 * x)         #generate the signal for the actual chunk
        self.offset += self.n_chunk                                 #update offset param
        if self.offset == self.period:
            self.offset = 0
        chunk = self.reverbModifier.applyReverb(chunk)
        return chunk
    
    def is_run(self):
        return self.state
        
    def start(self):
        self.state = True
        
    def stop(self):
        self.state = False
        self.offset = 0
        
    def change_waveform(self, type):
        self.type = type
        if self.type == "sin":
            self.generator = np.sin
        elif self.type == "saw":
            self.generator = signal.sawtooth