# tropisms/nutrient_field_finder.py

from tropisms.field_finder import FieldFinder
from core.point import MPoint
import numpy as np

class NutrientFieldFinder(FieldFinder):
    def __init__(self, location: MPoint, strength=1.0, decay=1.0, repulsive=False):
        self.location = location
        self.strength = strength
        self.decay = decay
        self.repulsive = repulsive

    def find_field(self, point: MPoint) -> float:
        d = point.distance_to(self.location)
        if self.repulsive:
            return -self.strength / (1 + self.decay * d)
        return self.strength / (1 + self.decay * d)

    def gradient(self, point: MPoint) -> MPoint:
        direction = point.copy().subtract(self.location)
        d = np.linalg.norm(direction.as_array())
        if d == 0:
            return MPoint(0, 0, 0)
        grad_mag = self.strength * self.decay / ((1 + self.decay * d) ** 2)
        grad = direction.scale(-grad_mag if self.repulsive else grad_mag)
        return grad.normalise()

    def get_id(self):
        return id(self)
