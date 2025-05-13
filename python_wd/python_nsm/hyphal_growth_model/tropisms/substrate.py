# tropisms/substrate.py

from core.point import MPoint
from tropisms.field_finder import FieldFinder
import numpy as np

class LinearSubstrate(FieldFinder):
    """
    Represents a linear substrate (e.g., a line of nutrient),
    emitting a scalar field that decays with perpendicular distance.
    """

    def __init__(self, origin: MPoint, direction: MPoint, strength: float = 1.0, decay: float = 1.0):
        self.origin = origin.copy()
        self.direction = direction.copy().normalise()
        self.strength = strength
        self.decay = decay

    def find_field(self, point: MPoint) -> float:
        # Perpendicular distance to line
        delta = point.copy().subtract(self.origin)
        projection = self.direction.copy().scale(delta.dot(self.direction))
        perpendicular = delta.subtract(projection)
        d = np.linalg.norm(perpendicular.as_array())
        return self.strength / (1 + self.decay * d)

    def gradient(self, point: MPoint) -> MPoint:
        # Compute attractive force perpendicular to line
        delta = point.copy().subtract(self.origin)
        projection = self.direction.copy().scale(delta.dot(self.direction))
        perpendicular = delta.subtract(projection)
        d = np.linalg.norm(perpendicular.as_array())

        if d == 0:
            return MPoint(0, 0, 0)

        grad = perpendicular.scale(-self.strength * self.decay / ((1 + self.decay * d) ** 2)).normalise()
        return grad
