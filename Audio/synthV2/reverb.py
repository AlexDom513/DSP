import numpy as np
from scipy import signal

class verb:

    def __init__(self):
        self.b1, self.a1 = self.allpassCoef(.7, 347)
        self.b2, self.a2 = self.allpassCoef(.7, 113)
        self.b3, self.a3 = self.allpassCoef(.7, 37)
        self.b1C, self.a1C = self.combCoef(.773, 1687)
        self.b2C, self.a2C = self.combCoef(.802, 1601)
        self.b3C, self.a3C = self.combCoef(.753, 2053)
        self.b4C, self.a4C = self.combCoef(.733, 2251)

    def applyReverb(self, inputSignal):
        y = signal.lfilter(self.b1, self.a1, inputSignal)
        y = signal.lfilter(self.b2, self.a2, y)
        y = signal.lfilter(self.b3, self.a3, y)
        y1 = signal.lfilter(self.b1C, self.a1C, y)
        y2 = signal.lfilter(self.b2C, self.a2C, y)
        y3 = signal.lfilter(self.b3C, self.a3C, y)
        y4 = signal.lfilter(self.b4C, self.a4C, y)
        y = y1 + y2 + y3 + y4
        return y

    def combCoef(self, gain, delay):
        b = [1]
        a = np.zeros(delay+1)
        a[0] = 1
        a[-1] = -gain
        return b, a

    def allpassCoef(self, k, delay):
        b = np.zeros(delay+1)
        b[0] = -k
        b[-1] = 1
        a = np.zeros(delay+1)
        a[0] = 1
        a[-1] = -k
        return b, a