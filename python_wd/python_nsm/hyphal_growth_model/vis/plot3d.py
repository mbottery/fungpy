# vis/plot3d.py

import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D projection
from core.mycel import Mycel

def plot_mycel_3d(mycel: Mycel, title="Hyphal Growth in 3D", save_path=None):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    all_x, all_y, all_z = [], [], []

    for section in mycel.get_all_segments():
        for start, end in section.get_subsegments():
            x0, y0, z0 = start.coords
            x1, y1, z1 = end.coords

            ax.plot([x0, x1], [y0, y1], [z0, z1], colour="green", linewidth=1.2)
            all_x.extend([x0, x1])
            all_y.extend([y0, y1])
            all_z.extend([z0, z1])

        if section.is_tip and not section.is_dead:
            x_tip, y_tip, z_tip = section.end.coords
            ax.scatter(x_tip, y_tip, z_tip, colour="red", s=10)

    if all_x and all_y and all_z:
        ax.set_xlim(min(all_x), max(all_x))
        ax.set_ylim(min(all_y), max(all_y))
        ax.set_zlim(min(all_z), max(all_z))

    plt.tight_layout()

    if not save_path:
        os.makedirs("outputs", exist_ok=True)
        save_path = "outputs/mycelium_3d.png"

    plt.savefig(save_path)
    plt.close()
