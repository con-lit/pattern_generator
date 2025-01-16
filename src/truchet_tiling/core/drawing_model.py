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
        self.path_line[path_id] = line_id
        self.lines[line_id] = path

        self.points.append([path_id, start])
        self.points.append([path_id, end])

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
                path_1_id, path_2_id = cluster[i][0], cluster[i+1][0]
                line_1_id, line_2_id = self.path_line[path_1_id], self.path_line[path_2_id]
                if line_1_id == line_2_id:
                    continue
                merged_line = Path(*self.lines[line_1_id], *self.lines[line_2_id])
                merged_line_id = 'merged-' + random_uuid()
                self.path_line = {k: merged_line_id if v == line_1_id or v == line_2_id else v for k, v in self.path_line.items()}
                self.lines[merged_line_id] = merged_line
                del self.lines[line_1_id]
                del self.lines[line_2_id]
                