from truchet_tiling.core.drawing_model import DrawingModel
from truchet_tiling.core.fills.gradient import Gradient
from truchet_tiling.core.utils import random_uuid


class TriTree:
    children = []
    
    def __init__(self, vertices:list, depth:int, reflected:bool, matrix:Gradient, model:DrawingModel):
        self.uuid = None
        self.vertices = vertices
        self.depth = depth
        self.reflected = reflected
        self.matrix = matrix
        self.model = model
        if self.can_be_divided:
            self.divide_surface()
        else: 
            self.create_tile()

    def _midpoint(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    
    @property
    def can_be_divided(self):
        value = self.matrix.get_max(self.vertices)
        return value > 0 and self.depth > 0
    
    @property
    def position(self):
        x = min(self.vertices, key=lambda p: p[0])[0]
        y = min(self.vertices, key=lambda p: p[1])[1]
        return (x, y)
    
    def divide_surface(self):
        mid1 = self._midpoint(self.vertices[0], self.vertices[1])
        mid2 = self._midpoint(self.vertices[1], self.vertices[2])
        mid3 = self._midpoint(self.vertices[2], self.vertices[0])
        next_depth = self.depth - 1

        self.children = [
            TriTree([self.vertices[0], mid1, mid3], next_depth, self.reflected, self.matrix, self.model),
            TriTree([mid1, self.vertices[1], mid2], next_depth, self.reflected, self.matrix, self.model),
            TriTree([mid3, mid2, self.vertices[2]], next_depth, self.reflected, self.matrix, self.model),
            TriTree([mid1, mid2, mid3], next_depth, not self.reflected, self.matrix, self.model),
        ]

    def register_connection(self, point1:tuple, point2:tuple, level:int):
        if level > 1:
            mid = self._midpoint(point1, point2)
            p1 = (point1, mid)
            p2 = (mid, point2)
            self.register_connection(*p1, level = level - 1)
            self.register_connection(*p2, level = level - 1)
        else:
            x1, y1 = map(int, point1)
            x2, y2 = map(int, point2)
            if x1 != x2:
                id = f"{x1}-{y1}-{x2}-{y2}" if x1 < x2 else f"{x2}-{y2}-{x1}-{y1}"
            else:
                id = f"{x1}-{y1}-{x2}-{y2}" if y1 < y2 else f"{x2}-{y2}-{x1}-{y1}"
            self.model.register_connection(id)
            

    def create_tile(self):
        interfaces = 2 ** self.depth
        self.uuid = random_uuid()
        for i, v in enumerate(self.vertices):
            side = (v, self.vertices[(i + 1) % len(self.vertices)])
            self.register_connection(*side, level = interfaces)
        

    def draw_tile(self, callback):
        if self.children:
            for child in self.children:
                child.draw_tile(callback)
        else:
            callback(
                self.position,
                self.reflected,
                self.depth,
                self.uuid,
                self.model,
            )