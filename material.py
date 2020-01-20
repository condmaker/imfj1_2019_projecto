from color import *

class Material:
    def __init__(self, color, name = "UnknownMaterial", fill = 5):
        self.color = color
        self.name = name
        self.line_width = fill

