#https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
#https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/
import numpy as np
import Tkinter as tk
from synthRunner import runner

#here we construct our layout of all the different widgets
class GUI(tk.Tk):
#In our case, we're inheriting everything from the tk.Tk class. Think of it kind of like how you import modules to use them.
#That's basically what's happening when you inherit, only at the local class level.

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs) #initialize the inherited class

        # define container, which will be filled with a bunch of frames to be accessed later on
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
freq = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*freq/fs)).astype(np.float32)
#https://www.kite.com/python/answers/how-to-modify-a-global-variable-inside-a-class-method-in-python

#here we can start constructing individual widgets and their methods      
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10,padx=10)


        #volume = 0.5     # range [0.0, 1.0]
        #fs = 44100       # sampling rate, Hz, must be integer
        #duration = 1.0   # in seconds, may be float
        #freq = 440.0        # sine frequency, Hz, may be float

        # generate samples, note conversion to float32 array
        #samples = (np.sin(2*np.pi*np.arange(fs*duration)*freq/fs)).astype(np.float32)

        def print_value(val):
            print(val)
            global freq
            freq = val

        slider = tk.Scale(self, from_ = 100, to = 1000, orient = tk.HORIZONTAL, command = print_value)
        slider.pack()

        #need to actually update the runner because the instantiation is has already been done once with the 440 Hz
        #there is no actual way to change the parameter for frequency!!!!!
        run = runner(volume, fs, duration, freq, samples)

        #so this is actually pretty smart, we have our runner carry a stream method, then whenever we press the button we can actually play the sound!
        #button could actually be an enable/disable feature
        button = tk.Button(self, text="Visit Page 1", command=lambda: run.stream())
        button.pack() 

app = GUI()
app.mainloop()