class ConnectorNew:
    def __init__(self):
        self.connections = {}

    def register_connection(self, id:str):
        if id not in self.connections:
            self.connections[id] = ['connection1']
        else:
            self.connections[id].append('connection2')
    