class Pixel:
    def __init__(self, color=(0, 0, 0), unset=False):
        self.color = color
        self.unset = unset
        return

    def __eq__(self, value):
        return isinstance(value, Pixel) and self.color == value.color and self.unset == value.unset

    def __repr__(self):
        return str(self.color)
    
    def __str__(self):
        return str(self.color)