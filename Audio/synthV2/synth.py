#https://www.wizard-notes.com/entry/dev/pyqt5-pyaudio-simple-synthesizer
#https://github.com/Kurene/simple-synthesizer-with-pyqt5-pyaudio/blob/master/main.py
#file responsible for processing inputs and returning an actual sound output

import pyaudio
import numpy as np
import threading
from synth_modules import Oscillator

class Synthesizer:
    waveform = ["sin", "saw"]
    
    def __init__(self, rate=44100, n_chunk=1024):
        self.rate = rate
        self.n_chunk = n_chunk
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=1, frames_per_buffer=n_chunk)
        print('Stream Active!')
        self.oscillators = []
        self.type = Synthesizer.waveform[0]
        t = threading.Thread(target=self.render)
        t.start()
     
    #find and return the oscillator for a specific frequency
    def __seek_osc(self, freq):
        osc = None
        for o in self.oscillators:  #check if freq matches an established oscillator
            if freq == o.freq:
                osc = o
        if osc is None:             #if there is no active oscillator, create one
            osc = Oscillator(self.rate, self.n_chunk, freq, self.type)
            self.oscillators.append(osc)
        return osc
    
    #render the chunks as sound
    def render(self):
        while self.stream.is_active():
            chunk = np.zeros(self.n_chunk)                          #by default, create zero chunk
            for osc in self.oscillators:                            #loop through list of created oscillators
                if osc.is_run():                                    #check if oscillator is active
                    chunk += osc.out()                              #add output of active oscillator into chunk
            self.stream.write(chunk.astype(np.float32).tobytes())   #write chunk to stream (play sound)
    
    #enable/disable oscillator playback
    def request(self, freq):
        osc = self.__seek_osc(freq)
        if not osc.is_run():
            osc.start()
            return True
        else:
            osc.stop()
            return False

    #terminate synthesizer operation
    def terminate(self):
        for osc in self.oscillators:
            osc.stop()
        self.stream.close()
        self.p.terminate()
        print('Stream Terminated!')