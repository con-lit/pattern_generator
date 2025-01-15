class ConnectorNew:
    def __init__(self):
        self.connections = {}

    def register_connection(self, id:str):
        if id not in self.connections:
            self.connections[id] = ['connection1']
            print(f"Connection created {id}")
        else:
            self.connections[id].append('connection2')
            print(f"Connection extended {id}")
    