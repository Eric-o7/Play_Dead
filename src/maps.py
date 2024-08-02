from graphics import *

class Maps():
    def __init__(self, name, height, width, neighbors, coordinates=None):
        self.name = name
        self.height = height
        self.width = width
        self.neighbors = neighbors
        self.coordinates = coordinates
        
        