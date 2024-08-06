from graphics import *

class Maps():
    def __init__(self, name: str, height: int, width: int, neighbors: list):
        self.name = name
        self.height = height
        self.width = width
        self.neighbors = neighbors

tutorial = Maps("Tutorial Room", 10, 10, None)