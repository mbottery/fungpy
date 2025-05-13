# tropisms/field_finder.py

from abc import ABC, abstractmethod
from core.point import MPoint
import numpy as np

class FieldFinder(ABC):
    """Base class for any object that contributes a scalar field."""

    @abstractmethod
    def find_field(self, point: MPoint) -> float:
        """Returns field strength at a given point."""
        pass

    def gradient(self, point: MPoint) -> MPoint:
        """Returns direction of field change at a given point (optional)."""
        return MPoint(0, 0, 0)

    def get_id(self) -> int:
        """Optional: return ID for source exclusion logic."""
        return -1


class PointFieldFinder(FieldFinder):
    """A simple field emitter from a fixed point (e.g., substrate or tip)."""

    def __init__(self, source: MPoint, strength: float = 1.0, decay: float = 1.0):
        self.source = source.copy()
        self.strength = strength
        self.decay = decay  # Field ~ strength / (1 + d * decay)

    def find_field(self, point: MPoint) -> float:
        d = self.source.distance_to(point)
        return self.strength / (1.0 + self.decay * d)

    def gradient(self, point: MPoint) -> MPoint:
        """Returns a vector pointing from source → point, scaled by gradient."""
        direction = point.copy().subtract(self.source)
        d = np.linalg.norm(direction.as_array())
        if d == 0:
            return MPoint(0, 0, 0)
        return direction.scale(self.strength * self.decay / ((1 + self.decay * d) ** 2)).normalise()
