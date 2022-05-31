import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = plt.axes(xlim=(-10, 10), ylim=(-10, 10))
ax.grid()
line, = ax.plot([], [], lw=3)
circle = ax.plot([], [])

def init():
    line.set_data([], [])
    circle.set_data([], [])
    return circle
def animate(i):
    x = np.linspace(0, 4, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    circ = plt.Circle((0,0),.5*i)
    plt.Circle((0,0),.5*i)
    return line,

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)


anim.save('test.gif', writer='imagemagick')