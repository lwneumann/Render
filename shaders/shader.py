from pixel import Pixel


class Shader:
    def __init__(self, def_color=(255, 255, 255)):
        self.color = def_color
        return
    
    def fragment(self, pix, frame=0):
        """
        Given a point return new color
        """
        if pix in [None, False]:
            return pix
        return self.color

    def vertex(self, pix, frame=0):
        """
        Given a point, return new position
        """
        return [pix[0], pix[1]]
    
    def __repr__(self):
        return f"{type(self).__name__}({self.color})"


# Some defaults
DEFAULT_SHADER = Shader()
GRAY = Shader((150, 150, 150))
RED = Shader((255, 100, 100))
GREEN = Shader((100, 255, 100))
BLUE = Shader((100, 100, 255))
