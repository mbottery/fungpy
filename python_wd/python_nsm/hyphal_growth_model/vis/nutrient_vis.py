# vis/nutrient_vis.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from core.options import Options

def plot_nutrient_field_2d(opts: Options, ax=None, save_path=None):
    """Plots nutrient sources and sinks on a 2D plane."""
    if ax is None:
        fig, ax = plt.subplots()

    ax.set_title("Nutrient Field (2D)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Plot attractors
    for pos, strength in opts.nutrient_attractors:
        x, y = pos[0], pos[1]
        ax.plot(x, y, "g^", label="Attractor" if strength > 0 else "Repellent")
        ax.annotate(f"{strength:+.1f}", (x, y), textcoords="offset points", xytext=(0, 5), ha="centre")

    # Plot repellents
    for pos, strength in opts.nutrient_repellents:
        x, y = pos[0], pos[1]
        ax.plot(x, y, "rv")
        ax.annotate(f"{strength:+.1f}", (x, y), textcoords="offset points", xytext=(0, -10), ha="centre")

    ax.legend(["Attractor", "Repellent"])
    ax.grid(True)
    ax.axis("equal")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def plot_nutrient_field_3d(opts: Options, ax=None, save_path=None):
    """Plots nutrient sources in 3D (optional height/position awareness)."""
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

    ax.set_title("Nutrient Field (3D)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    for pos, strength in opts.nutrient_attractors:
        ax.scatter(*pos, color="green", marker="^", s=40)
        ax.text(*pos, f"{strength:+.1f}", color="green", size=8)

    for pos, strength in opts.nutrient_repellents:
        ax.scatter(*pos, color="red", marker="v", s=40)
        ax.text(*pos, f"{strength:+.1f}", color="red", size=8)

    ax.view_init(elev=20, azim=135)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
