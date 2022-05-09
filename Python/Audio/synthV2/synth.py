#https://github.com/Kurene/simple-synthesizer-with-pyqt5-pyaudio/blob/master/main.py

import pyaudio
import numpy as np
import threading
from scipy import signal
import time
import curses

class Oscillator():
    #actually creates the sine wave, which is then rendered by the synthesizer
    def __init__(self, rate, n_chunk, freq, type, gain=0.1):
        #sampling rate
        self.rate = rate
        #chunk size (typically 1024)
        #chunk is like a buffer, each buffer would contain 1024 samples
        #this is done because of processing power constraints
        self.n_chunk = n_chunk
        #frequency
        self.freq = freq
        #gain
        self.gain = gain
        
        #(on or off?)
        self.state = False
        #angular frequency (2*pi/T, T is the period, T = rate/frequency)
        self.pi2_t0 = 2 * np.pi / (rate / freq)
        self.offset = 0
        self.period = n_chunk * rate
        
        self.change_waveform(type)

    def out(self):
        #generate the actual chunk
        x =  np.arange(self.offset, self.offset + self.n_chunk)
        chunk = self.gain * self.generator(self.pi2_t0 * x)
        #offset is used to link the chunks together and avoid clipping?
        self.offset += self.n_chunk
        if self.offset == self.period:
            self.offset = 0
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

class Synthesizer():
    waveform = ["sin", "saw"]
    def __init__(self, rate=44100, n_chunk=1024):
        self.rate = rate
        self.n_chunk = n_chunk
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=1,
                                  frames_per_buffer=n_chunk)
        print('stream active')
        self.oscillators = []
        self.type = Synthesizer.waveform[0]

        #threading used to run sound output in parallel with any gui operation
        t = threading.Thread(target=self.render)
        t.start()
     
    #finds the active oscillators
    def __seek_osc(self, freq):
        osc = None
        #if the function input (frequency) matches a current oscillator, osc = that oscillator
        for o in self.oscillators:
            if freq == o.freq:
                osc = o
        #if there is no active oscillator, create one
        if osc is None:
            osc = Oscillator(self.rate, self.n_chunk, freq, self.type)
            self.oscillators.append(osc)
        #returns the active oscillator
        return osc
    
    #used to actaully create sound
    def render(self):
        while self.stream.is_active():
            
            #by default have a chunk of zeros in case there are no active oscillators
            chunk = np.zeros(self.n_chunk)
            #run through all the current oscillators
            for osc in self.oscillators:

                #adding up the chunks from all the oscillators that are currently running
                if osc.is_run():
                    chunk += osc.out() #add the output of the current oscillator into the chunk
            #write the stream (play the sound of the chunk)
            self.stream.write(chunk.astype(np.float32).tobytes())
            
    def request(self, freq):
        osc = self.__seek_osc(freq)
        #gets the oscillator
        if not osc.is_run():
            osc.start()
            return True
        else:
            osc.stop()
            return False

    #stop oscillators from playing
    def terminate(self):
        for osc in self.oscillators:
            osc.stop()
        self.stream.close()
        self.p.terminate()

import keyboard  # using module keyboard
synth = Synthesizer()
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('z'):  # if key 'q' is pressed
            synth.request(400)
            synth.request(500)
            time.sleep(2)
            synth.request(400)
            synth.request(500)
            #break  # finishing the loop
        if keyboard.is_pressed('x'):  # if key 'q' is pressed
            synth.request(500)
            time.sleep(2)
            synth.request(500)
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            break
    except:
        break  # if user pressed a key other than the given key the loop will break
'''
synth = Synthesizer()
synth.request(400)
time.sleep(5)
synth.request(400)
synth.request(256)
time.sleep(2)
synth.terminate()
'''

