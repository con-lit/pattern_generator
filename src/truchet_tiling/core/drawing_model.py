from sklearn.cluster import DBSCAN
from svgpathtools import Path
import numpy as np

from truchet_tiling.core.utils import random_uuid

class DrawingModel:
    def __init__(self):
        self.pathes = {}
        self.points = []
        self.connections = {}
        self.lines = {}
        self.path_line = {}

    def register_connection(self, id:str):
        if id not in self.connections:
            self.connections[id] = ['connection1']
        else:
            self.connections[id].append('connection2')

    def register_path(self, path_id:str, path: Path, start:tuple, end:tuple):
        line_id = random_uuid()
        self.path_line[path_id] = {path_id: line_id}
        self.lines[line_id] = path

        self.points.append([line_id, start])
        self.points.append([line_id, end])

    def connect_lines(self, radius:float = 0.1):
        # Extract (x, y) coordinates from [id, (x, y)]
        coords = np.array([p[1] for p in self.points])
        
        # Apply DBSCAN with eps=radius, minimum of 2 points
        dbscan = DBSCAN(eps=radius, min_samples=2).fit(coords)
        
        # Organize points by cluster label
        clusters = {}
        for label, point in zip(dbscan.labels_, self.points):
            if label == -1:  # noise/outlier
                continue
            clusters.setdefault(label, []).append(point)

        for cluster in clusters.values():
            for i in range(len(cluster) - 1):
                pair = (cluster[i][0], cluster[i + 1][0])
                print(pair)
                