from truchet_tiling.core.fills.gradient import Gradient


class TriTree:
    children = []
    
    def __init__(self, vertices:list, depth:int, reflected:bool, matrix:Gradient):
        self.vertices = vertices
        self.depth = depth
        self.reflected = reflected
        self.matrix = matrix
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
            TriTree([self.vertices[0], mid1, mid3], next_depth, self.reflected, self.matrix),
            TriTree([mid1, self.vertices[1], mid2], next_depth, self.reflected, self.matrix),
            TriTree([mid3, mid2, self.vertices[2]], next_depth, self.reflected, self.matrix),
            TriTree([mid1, mid2, mid3], next_depth, not self.reflected, self.matrix),
        ]

    def create_tile(self):
        x = [self.vertices[0][0], self.vertices[1][0], self.vertices[2][0]]
        y = [self.vertices[0][1], self.vertices[1][1], self.vertices[2][1]]

    def draw_tile(self, callback, drawing):
        if self.children:
            for child in self.children:
                child.draw_tile(callback, drawing)
        else:
            callback(drawing, self.position, self.reflected, self.depth)