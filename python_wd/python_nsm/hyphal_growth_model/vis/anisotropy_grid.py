# vis/anisotropy_grid.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from core.point import MPoint

class AnisotropyGrid:
    """Spatial grid assigning directional bias (anisotropy vector) at each location."""

    def __init__(self, width=100, height=100, depth=100, resolution=10.0):
        self.width = width
        self.height = height
        self.depth = depth
        self.resolution = resolution

        self.field = np.zeros((int(width / resolution),
                               int(height / resolution),
                               int(depth / resolution), 3))
        self.field[..., 0] = 1.0  # Default: bias along +X

    def set_uniform_direction(self, direction: MPoint):
        vec = direction.normalise().as_array()
        self.field[:, :, :, :] = vec

    def get_direction_at(self, point: MPoint) -> MPoint:
        i = int((point.coords[0] + self.width / 2) / self.resolution)
        j = int((point.coords[1] + self.height / 2) / self.resolution)
        k = int((point.coords[2] + self.depth / 2) / self.resolution)

        if 0 <= i < self.field.shape[0] and 0 <= j < self.field.shape[1] and 0 <= k < self.field.shape[2]:
            vec = self.field[i, j, k]
            return MPoint(*vec).normalise()
        else:
            return MPoint(0, 0, 0)

# Visualisation helpers
def plot_anisotropy_2d(grid: AnisotropyGrid, title="Anisotropy Vectors (XY Slice)", save_path=None):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    step = 1
    for i in range(0, grid.field.shape[0], step):
        for j in range(0, grid.field.shape[1], step):
            vec = grid.field[i, j, 0]
            x = (i * grid.resolution) - grid.width / 2
            y = (j * grid.resolution) - grid.height / 2
            ax.quiver(x, y, vec[0], vec[1], angles='xy', scale_units='xy', scale=1.0, colour='blue', width=0.002)

    ax.axis("equal")
    ax.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def plot_anisotropy_3d(grid: AnisotropyGrid, save_path=None):
    """Plot anisotropy vectors in 3D."""
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("Anisotropy Field (3D Sample)")

    step = 2
    for i in range(0, grid.field.shape[0], step):
        for j in range(0, grid.field.shape[1], step):
            for k in range(0, grid.field.shape[2], step):
                vec = grid.field[i, j, k]
                if np.linalg.norm(vec) < 1e-3:
                    continue
                x = (i * grid.resolution) - grid.width / 2
                y = (j * grid.resolution) - grid.height / 2
                z = (k * grid.resolution) - grid.depth / 2
                ax.quiver(x, y, z, vec[0], vec[1], vec[2], length=3.0, normalize=True, colour="blue")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
