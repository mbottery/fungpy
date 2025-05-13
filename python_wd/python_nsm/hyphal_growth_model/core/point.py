# core/point.py

import numpy as np

class MPoint:
    """3D point class with vector operations used in mycelium growth simulation."""
    
    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initialise with x, y, z as floats."""
        self.coords = np.array([x, y, z], dtype=np.float64)

    def copy(self):
        """Return a new MPoint with the same coordinates."""
        return MPoint(*self.coords)

    def distance_to(self, other) -> float:
        """Euclidean distance to another MPoint."""
        return np.linalg.norm(self.coords - other.coords)

    def normalise(self):
        """Convert this point to a unit vector."""
        norm = np.linalg.norm(self.coords)
        if norm == 0:
            return self
        self.coords /= norm
        return self

    def add(self, other):
        """Vector addition with another MPoint."""
        self.coords += other.coords
        return self

    def subtract(self, other):
        """Vector subtraction with another MPoint."""
        self.coords -= other.coords
        return self

    def scale(self, factor):
        """Multiply vector by scalar."""
        self.coords *= factor
        return self

    def dot(self, other):
        """Dot product with another MPoint."""
        return float(np.dot(self.coords, other.coords))

    def cross(self, other):
        """Cross product with another MPoint (returns a new MPoint)."""
        return MPoint(*np.cross(self.coords, other.coords))

    def rotated_around(self, axis, angle_degrees):
        """Rotate vector around another vector (axis) by given angle (degrees)."""
        angle_rad = np.deg2rad(angle_degrees)
        axis_vec = axis.coords / np.linalg.norm(axis.coords)
        self.coords = (
            self.coords * np.cos(angle_rad)
            + np.cross(axis_vec, self.coords) * np.sin(angle_rad)
            + axis_vec * (np.dot(axis_vec, self.coords)) * (1 - np.cos(angle_rad))
        )
        return self

    def __str__(self):
        """String representation."""
        return f"MPoint({self.coords[0]:.3f}, {self.coords[1]:.3f}, {self.coords[2]:.3f})"

    def to_list(self):
        """Convert to Python list."""
        return self.coords.tolist()

    def as_array(self):
        """Return as NumPy array (for low-level math)."""
        return self.coords

    @staticmethod
    def from_array(arr):
        """Create an MPoint from a raw list or array."""
        return MPoint(*arr[:3])
