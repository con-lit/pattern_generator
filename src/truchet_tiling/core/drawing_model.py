from sklearn.cluster import DBSCAN
from svgpathtools import Path
import numpy as np

from truchet_tiling.core.svg_utils import merge_paths
from truchet_tiling.core.utils import close, random_uuid

from itertools import combinations
        
def is_smooth(p1: Path, p2:Path, tolerance=0.1):
    s1, e1 = p1.start, p1.end
    s2, e2 = p2.start, p2.end

    if close(e1, s2, tolerance):
        p2.start = e1
        first, second = p1, p2
    elif close(e2, s1, tolerance):
        p1.start = e2
        first, second = p2, p1
    elif close(s1, s2, tolerance):
        p1.start = s2
        first, second = p1.reversed(), p2
    elif close(e1, e2, tolerance): 
        p1.end = e2
        first, second = p1, p2.reversed()
    else:
        print('no match')
        print(s1, e1)
        print(s2, e2)
        print('--------')
        first, second = p1, p2
    
    d1 = first[-1].unit_tangent(1.0)
    d2 = second[0].unit_tangent(0.0)
    return close(d1, d2, 1)
    
def select_two(obj, test_func):
    responce = []
    stored_keys = []
    for a, b in combinations(obj.keys(), 2):
        va, vb = obj[a], obj[b]
        if test_func(va, vb) and a not in stored_keys and b not in stored_keys:
            stored_keys.extend([a, b])
            responce.append({a: va, b: vb})
    return responce

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
        coords = np.array([p[1] for p in self.points])
        dbscan = DBSCAN(eps=radius, min_samples=2).fit(coords)
        clusters = {}
        for label, point in zip(dbscan.labels_, self.points):
            if label == -1:  # noise/outlier
                continue
            clusters.setdefault(label, []).append(point)

        for cluster in clusters.values():
            # points = [point[1] for point in cluster]
            # mid_x = sum(x for x, _ in points) / len(points)
            # mid_y = sum(y for _, y in points) / len(points)
            # middle_point = (mid_x, mid_y)

            lines = {}

            for point in cluster:
                path_id = point[0]
                line_id = self.path_2_line[path_id]
                line = self.lines[line_id]
                lines[line_id] = line

            selected = select_two(lines, is_smooth)
            print(f'Found {len(selected)} pairs to merge')
            for pair in selected:
                line_1_id, line_2_id = [k for k in pair.keys()]
                line_1, line_2 = [v for v in pair.values()]
                merged_line = merge_paths(
                    line_1, 
                    line_2, 
                    tolerance=radius,
                )
                merged_line_id = random_uuid()
                self.path_2_line = {k: merged_line_id if v == line_1_id or v == line_2_id else v for k, v in self.path_2_line.items()}
                self.lines[merged_line_id] = merged_line
                del self.lines[line_1_id]
                del self.lines[line_2_id]