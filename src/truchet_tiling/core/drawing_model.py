from sklearn.cluster import DBSCAN
from svgpathtools import Path
import numpy as np

from truchet_tiling.core.svg_utils import is_smooth, merge_paths
from truchet_tiling.core.utils import random_uuid, select_two

class DrawingModel:
    def __init__(self):
        self.points = []
        self.connections = {}
        self.lines = {}
        self.path_2_line = {}

    def register_connection(self, id:str):
        if id not in self.connections:
            self.connections[id] = ['connection1']
        else:
            self.connections[id].append('connection2')

    def register_path(self, path_id:str, path: Path):
        line_id = random_uuid()
        self.path_2_line[path_id] = line_id
        self.lines[line_id] = path
        start = path.start
        end = path.end
        self.points.append([path_id, (start.real, start.imag)])
        self.points.append([path_id, (end.real, end.imag)])

    def connect_lines(self, radius:float = 0.2):
        tolerance = 2*radius
        coords = np.array([p[1] for p in self.points])
        dbscan = DBSCAN(eps=radius, min_samples=2).fit(coords)
        clusters = {}
        for label, point in zip(dbscan.labels_, self.points):
            if label == -1:  # noise/outlier
                continue
            clusters.setdefault(label, []).append(point)

        for cluster in clusters.values():
            lines = {}
            for point in cluster:
                path_id = point[0]
                line_id = self.path_2_line[path_id]
                line = self.lines[line_id]
                lines[line_id] = line

            selected = select_two(lines, is_smooth, tolerance)
            for pair in selected:
                line_1_id, line_2_id = [k for k in pair.keys()]
                line_1, line_2 = [v for v in pair.values()]
                merged_line = merge_paths(line_1, line_2, tolerance)
                merged_line_id = random_uuid()
                self.path_2_line = {k: merged_line_id if v == line_1_id or v == line_2_id else v for k, v in self.path_2_line.items()}
                self.lines[merged_line_id] = merged_line
                del self.lines[line_1_id]
                del self.lines[line_2_id]