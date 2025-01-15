import importlib.resources as ilr
import random
from typing import Literal
from PIL import Image
import numpy as np
import truchet_tiling.static.gradients as tt

class Gradient:
    files = {
         'linear': 'gradient_linear.png',
         'radial': 'gradient_round.png',
    }
    def __init__(self, type: Literal["linear", "radial"], width: int, height: int):
        with ilr.path(tt, self.files[type]) as fspath:
            image = Image.open(fspath).convert('L')
            image_resized = image.resize((width, height))
            self._data = np.array(image_resized).swapaxes(0, 1)
            self._data = self._data / 255
        
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
        values = [self._data[int(x), int(y)] for x, y in samples]
        return values
    
    def get_average(self, vertices:list):
        color_values = self.sample_points_in_triangle(vertices[0], vertices[1], vertices[2])
        return sum(color_values) / len(color_values)
    
    def get_max(self, vertices:list):
        color_values = self.sample_points_in_triangle(vertices[0], vertices[1], vertices[2])
        return max(color_values)