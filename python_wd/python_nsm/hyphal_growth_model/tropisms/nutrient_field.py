from core.point import MPoint

class NutrientField:
    def __init__(self, attractors=None, decay=0.05):
        self.sources = attractors or []
        self.decay = decay

    def compute(self, point: MPoint) -> MPoint:
        total = MPoint(0, 0, 0)
        for (x, y), strength in self.sources:
            vec = MPoint(x - point.x, y - point.y, 0)
            dist = vec.magnitude()
            if dist > 1e-3:
                influence = strength * np.exp(-self.decay * dist)
                total.add(vec.normalise().scale(influence))
        return total
