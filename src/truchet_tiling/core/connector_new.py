from sklearn.cluster import DBSCAN
import numpy as np

class ConnectorNew:
    def __init__(self):
        self.connections = {}
        self.points = []

    def register_connection(self, id:str):
        if id not in self.connections:
            self.connections[id] = ['connection1']
        else:
            self.connections[id].append('connection2')

    def register_path(self, start:tuple, end:tuple, path_id:str):
        self.points.append([path_id, start])
        self.points.append([path_id, end])

    def cluster_points(self, radius:float = 0.1):
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

        return list(clusters.values())