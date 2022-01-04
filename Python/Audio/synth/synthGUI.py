#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/

#note: perhaps different sections of the GUI could be formatted into a class, then the overall components could be rearranged, this
#can be addressed in a later version of the synthesizer
import Tkinter as tk
from synthRunner import runner
from time import sleep

#order: first we must have all of our functionality and processing, only then should we move forward with GUI design

#local variables
volume = 1     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
freq = 440.0     # sine frequency, Hz, may be float
duration = 2   # in seconds, may be float

#create the sound player object
run = runner(volume, fs, freq, duration)

#idea is that we would first instantiate any necessary processing objects and then call their specific commands from the button
def testCallBack():
    freq = freqSlider.get()
    run.convertFreq(freq)
    run.generateSamples()
    run.stream()
#need 44100 samples for 1 second of audio


#idea instantiate all the basic tkinter objects and processing objects, execute, idea we could actually have a bunch of buttons for the different frequencies
#maybe ill do separate versions of this project
master = tk.Tk()

#we will use a slider to set the frequency value
freqSlider = tk.Scale(master, from_=400, to=1000, orient=tk.HORIZONTAL)
freqSlider.pack()

toggleButton = tk.Button(master, text='toggle sound', command=testCallBack)
toggleButton.pack()

sineButton = tk.Button(master, text='Sine')
sineButton.pack()
sawButton = tk.Button(master, text='Saw')
sawButton.pack()
triangleButton = tk.Button(master, text='Triangle')
triangleButton.pack()
noiseButton = tk.Button(master, text = 'Noise')
noiseButton.pack()

master.mainloop()