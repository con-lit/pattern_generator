
import numpy as np

class Grey:
    def __init__(self, width:int, hight:int, octaves:int = 3, seed:int=None, data:np.array = None):
        if data is not None:
            self._data = data
        else:
            
            data = [[0.5 for j in range(hight)] for i in range(width)]
            self._data = np.array(data)

    @property
    def max(self):
        return self._data.max() if self._data.size else -1

    def slice(self, x:int, y:int, size:int):
        sliced = self._data[x:x+size, y:y+size]
        return Grey(size, size, data=sliced)