import json
from pathlib import Path

class Store:
    def __init__(self, path='store.json'):
        self.path = Path(path)
    def put(self, key, value):
        data = json.loads(self.path.read_text()) if self.path.exists() else {}
        data[key] = value
        self.path.write_text(json.dumps(data))
    def get(self, key):
        data = json.loads(self.path.read_text())
        return data.get(key)
