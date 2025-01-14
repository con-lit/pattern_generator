class TriTree:
    children = []
    
    def __init__(self, vertices:list, depth:int, reflected:bool):
        self.vertices = vertices
        self.depth = depth
        self.reflected = reflected
        pass

    def midpoint(self, p1, p2):
        return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    
    def _divide_surface(self):
        if depth == 0:
            # Base case: Draw the triangle
            x = [vertices[0][0], vertices[1][0], vertices[2][0], vertices[0][0]]
            y = [vertices[0][1], vertices[1][1], vertices[2][1], vertices[0][1]]
            color = "red" if reflected else "blue"

        else:
            # Get the midpoints of each side
            mid1 = self.midpoint(vertices[0], vertices[1])
            mid2 = self.midpoint(vertices[1], vertices[2])
            mid3 = self.midpoint(vertices[2], vertices[0])
            
            # Recursively subdivide each of the 4 smaller triangles
            self.children = [

            ]
            self.subdivide_triangle([vertices[0], mid1, mid3], depth - 1, reflected)
            self.subdivide_triangle([mid1, vertices[1], mid2], depth - 1, reflected)
            self.subdivide_triangle([mid3, mid2, vertices[2]], depth - 1, reflected)
            self.subdivide_triangle([mid1, mid2, mid3], depth - 1, not reflected)