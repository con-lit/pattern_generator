import random
from perlin_noise import PerlinNoise
import numpy as np

class Perlin:
    def __init__(self, width:int, hight:int, octaves:int = 3, seed:int=None, data:np.array = None):
        if data is not None:
            self._data = data
        else:
            noise = PerlinNoise(octaves=octaves, seed=seed)
            data = [[noise([i/width, j/hight]) for j in range(hight)] for i in range(width)]
            self._data = np.array(data)

    @property
    def max(self):
        return self._data.max() if self._data.size else -1

    def slice(self, x:int, y:int, size:int):
        sliced = self._data[x:x+size, y:y+size]
        return Perlin(size, size, data=sliced)
    

    def sample_points_in_triangle(self, v1, v2, v3, num_samples=100):
        """Sample points inside a triangle using barycentric coordinates."""
        samples = []
        for _ in range(num_samples):
            u, v = random.random(), random.random()
            if u + v > 1:
                u, v = 1 - u, 1 - v
            # Barycentric interpolation
            x = (1 - u - v) * v1[0] + u * v2[0] + v * v3[0]
            y = (1 - u - v) * v1[1] + u * v2[1] + v * v3[1]
            samples.append((x, y))
        return samples
    
    def get_average(self, vertices:list):
        samples = self.sample_points_in_triangle(vertices[0], vertices[1], vertices[2])
        color_values = [self._data[int(x), int(y)] for x, y in samples]
        return sum(color_values) / len(color_values)