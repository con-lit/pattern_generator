from sklearn.cluster import DBSCAN
from svgpathtools import Path, CubicBezier
import numpy as np

from truchet_tiling.core.svg_utils import connect_pathes
from truchet_tiling.core.utils import random_uuid

class DrawingModel:
    def __init__(self):
        self.points = []
        self.connections = {}
        self.lines = {}
        self.path_line = {}

    def register_connection(self, id:str):
        if id not in self.connections:
            self.connections[id] = ['connection1']
        else:
            self.connections[id].append('connection2')

    def register_path(self, path_id:str, path: Path):
        line_id = random_uuid()
        self.path_line[path_id] = line_id
        self.lines[line_id] = path
        start = path.start
        end = path.end
        self.points.append([path_id, (start.real, start.imag)])
        self.points.append([path_id, (end.real, end.imag)])

    def connect_lines(self, radius:float = 0.2):
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

        print(f'Found {len(clusters)} nodes to connect')

        for cluster in clusters.values():
            i = 0
            while i < len(cluster) - 1:
                path_1_id, path_2_id = cluster[i][0], cluster[i+1][0]
                line_1_id, line_2_id = self.path_line[path_1_id], self.path_line[path_2_id]
                if line_1_id != line_2_id:
                    merged_line = connect_pathes(
                        self.lines[line_1_id], 
                        self.lines[line_2_id], 
                        tolerance=radius,
                    )
                    merged_line_id = random_uuid()
                    self.path_line = {k: merged_line_id if v == line_1_id or v == line_2_id else v for k, v in self.path_line.items()}
                    self.lines[merged_line_id] = merged_line
                    del self.lines[line_1_id]
                    del self.lines[line_2_id]
                i += 2