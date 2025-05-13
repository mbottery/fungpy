# io_utils/grid_export.py

import numpy as np
import matplotlib.pyplot as plt
from vis.density_map import DensityGrid
import os

def export_grid_to_csv(grid: DensityGrid, filename: str):
    np.savetxt(filename, grid.grid, delimiter=",", fmt="%.4f")
    print(f"✅ Density grid saved to CSV: {filename}")

def export_grid_to_png(grid: DensityGrid, filename: str, cmap="hot"):
    plt.imsave(filename, grid.grid, cmap=cmap, origin='lower')
    print(f"🖼️ Density heatmap saved as image: {filename}")
