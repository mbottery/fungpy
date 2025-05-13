# vis/density_map.py

import numpy as np
import matplotlib.pyplot as plt
from core.point import MPoint
from core.mycel import Mycel

class DensityGrid:
    def __init__(self, width=100, height=100, resolution=1.0):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.grid = np.zeros((int(height / resolution), int(width / resolution)))

    def add_point(self, point: MPoint):
        x, y = point.coords[0], point.coords[1]
        i = int((y + self.height / 2) / self.resolution)
        j = int((x + self.width / 2) / self.resolution)
        if 0 <= i < self.grid.shape[0] and 0 <= j < self.grid.shape[1]:
            self.grid[i, j] += 1

    def get_density_at(self, point: MPoint) -> float:
        x, y = point.coords[0], point.coords[1]
        i = int((y + self.height / 2) / self.resolution)
        j = int((x + self.width / 2) / self.resolution)
        if 0 <= i < self.grid.shape[0] and 0 <= j < self.grid.shape[1]:
            return self.grid[i, j]
        return 0.0

    def get_gradient_at(self, point: MPoint) -> MPoint:
        x, y = point.coords[0], point.coords[1]
        i = int((y + self.height / 2) / self.resolution)
        j = int((x + self.width / 2) / self.resolution)

        if 1 <= i < self.grid.shape[0] - 1 and 1 <= j < self.grid.shape[1] - 1:
            d_dx = (self.grid[i, j + 1] - self.grid[i, j - 1]) / (2 * self.resolution)
            d_dy = (self.grid[i + 1, j] - self.grid[i - 1, j]) / (2 * self.resolution)
            return MPoint(d_dx, d_dy, 0).normalise()

        return MPoint(0, 0, 0)

    def update_from_mycel(self, mycel: Mycel):
        opts = mycel.options
        count = 0

        for section in mycel.get_all_segments():
            include = False
            
            print(f" Section @ {section.end}, tip={section.is_tip}, dead={section.is_dead}, children={len(section.children)}")
            
            include = True

            if include:
                self.add_point(section.end)
                count += 1

        print(f"🧮 DensityGrid updated with {count} contributing points.")

def plot_density(grid: DensityGrid, title="Hyphal Density Map", save_path=None):
    fig, ax = plt.subplots(figsize=(6, 6))

    # 📏 Auto-zoom to nonzero region
    nonzero_indices = np.argwhere(grid.grid > 0)
    if nonzero_indices.size > 0:
        i_min, j_min = nonzero_indices.min(axis=0)
        i_max, j_max = nonzero_indices.max(axis=0)

        margin = 5
        i_min = max(i_min - margin, 0)
        i_max = min(i_max + margin, grid.grid.shape[0])
        j_min = max(j_min - margin, 0)
        j_max = min(j_max + margin, grid.grid.shape[1])

        grid_region = grid.grid[i_min:i_max, j_min:j_max]

        extent = [
            (j_min * grid.resolution) - grid.width / 2,
            (j_max * grid.resolution) - grid.width / 2,
            (i_min * grid.resolution) - grid.height / 2,
            (i_max * grid.resolution) - grid.height / 2
        ]
    else:
        grid_region = grid.grid
        extent = [
            -grid.width / 2, grid.width / 2,
            -grid.height / 2, grid.height / 2
        ]

    # Heatmap with colourbar for hyphal density
    cax = ax.imshow(grid_region, origin='lower', cmap='hot', extent=extent, aspect='equal')
    fig.colourbar(cax, ax=ax, label="Density")

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(False)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
