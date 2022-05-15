#useful links/resources:
#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/

import Tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from synthRunner import runner

fs = 44100       # sampling rate, Hz, must be integer, need 44100 samples for 1 second of audio
freq = 440.0     # sine frequency, Hz, may be float
duration = 1   # in seconds, may be float

state = 0

#create the sound player object
run = runner(fs, freq, duration)

def case0():
    global state
    state = 0

def case1():
    global state
    state = 1

def case2():
    global state
    state = 2

def case3():
    global state
    state = 3

def plot():
    global a
    global canvas
    a.clear()
    a.plot(run.disp[:300])
    canvas.draw()

    global b
    global canvas2
    b.clear()
    b.plot(run.axisFFT, run.samplesFFT)
    canvas2.draw()

#idea is that we would first instantiate any necessary processing objects and then call their specific commands from the button
def testCallBack():
    freq = freqSlider.get()
    run.convertFreq(freq)

    global state
    if state == 0:
        run.sine()
    if state == 1:
        run.saw()
    if state == 2:
        run.triangle()
    if state == 3:
        run.noise()

    plot()
    run.stream()

#tkinter setup
master = tk.Tk()
master.title('PySynth v1')
master.iconbitmap('icon (1).ico')
actionFrame = tk.Canvas(master)
buttonFrame = tk.Canvas(master)
graphFrame = tk.Canvas(master)

#canvas (group similar widgets together)
actionFrame.pack(side='left', expand=True)
graphFrame.pack(expand=False)
buttonFrame.pack(side='right',expand=True)

#graphFrame
f = Figure(figsize=(3,2), dpi=100)
a = f.add_subplot(111)
a.plot([])
canvas = FigureCanvasTkAgg(f, master=graphFrame)
canvas.draw()
canvas.get_tk_widget().pack()

f2 = Figure(figsize=(3,2), dpi=100)
b = f2.add_subplot(111)
b.plot([])
canvas2 = FigureCanvasTkAgg(f2, master=graphFrame)
canvas2.draw()
canvas2.get_tk_widget().pack()

#actionFrame
freqSlider = tk.Scale(actionFrame, from_=100, to=1000, orient=tk.HORIZONTAL)
freqSlider.grid(column=0,row=0)
toggleButton = tk.Button(actionFrame, text='Play!', command=testCallBack)
toggleButton.grid(column=0, row=1)

#buttonFrame
padX = 0
padY = 0
buttonWidth = 7

sineButton = tk.Button(buttonFrame, text='Sine', width=buttonWidth, command=case0)
sineButton.grid(column=0, row=2, padx=padX, pady=padY)

sawButton = tk.Button(buttonFrame, text='Saw', width=buttonWidth, command=case1)
sawButton.grid(column=1, row=2, padx=padX, pady=padY)

triangleButton = tk.Button(buttonFrame, text='Triangle', width=buttonWidth, command=case2)
triangleButton.grid(column=0, row=3, padx=padX, pady=padY)

noiseButton = tk.Button(buttonFrame, text = 'Noise', width=buttonWidth, command=case3)
noiseButton.grid(column=1, row=3, padx=padX, pady=padY)

master.mainloop()