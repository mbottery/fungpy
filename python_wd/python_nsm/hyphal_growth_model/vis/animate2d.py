# vis/animate2d.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from core.mycel import Mycel
from core.options import Options
from tropisms.orientator import Orientator
import numpy as np

def animate_growth(mycel: Mycel, orientator: Orientator, steps=100, interval=200):
    """Animates the simulation frame-by-frame using matplotlib."""
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title("Hyphal Growth Animation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis("equal")
    ax.grid(True)

    lines = []

    def init():
        return lines

    def update(frame):
        ax.clear()
        ax.set_title(f"Time = {mycel.time:.1f}")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.axis("equal")
        ax.grid(True)

        for tip in mycel.get_tips():
            new_orientation = orientator.compute(tip)
            tip.orientation = new_orientation

        mycel.step()

        for section in mycel.get_all_segments():
            x0, y0 = section.start.coords[:2]
            x1, y1 = section.end.coords[:2]
            ax.plot([x0, x1], [y0, y1], colour="green", linewidth=1.2)
            if section.is_tip and not section.is_dead:
                ax.plot(x1, y1, "ro", markersize=3)

        return lines

    ani = animation.FuncAnimation(fig, update, frames=steps, init_func=init, blit=False, interval=interval)
    plt.show()
