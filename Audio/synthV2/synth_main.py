from synth import Synthesizer
import threading
import keyboard
import time
import sys

noteDict = {
  'z': 220,
  'x': 247,
  'c': 262,
  'v': 294,
  'b': 330,
  'n': 349,
  'm': 392,
  ',': 440}

#synth runner class puts sound rendering on seperate thread to avoid clipping
class synthRunner:
    def __init__(self, synth):
        self.synth = synth
        self.note = None
        self.activate = False

    def playNote(self):
        if self.activate:
            self.synth.request(self.note)
            self.activate = False

synth1 = Synthesizer()
runner = synthRunner(synth1)

while True:
    for note in noteDict:
        if keyboard.is_pressed(note):
            runner.note = noteDict[note]
            runner.activate = True
            t = threading.Thread(target=runner.playNote)
            t.start()
    if keyboard.is_pressed('q'):
        synth1.terminate()
        sys.exit()
    time.sleep(.1)

#Sample for testing chord
#synth.request(262)
#synth.request(330)
#synth.request(392)
