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