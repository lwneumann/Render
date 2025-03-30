from shapes import shape_util
import shaders.shader as shader
from math import floor, ceil


class Circle:
    def __init__(self, position, radius=1, filled=True, thickness=0.5, circ_shader=shader.DEFAULT_SHADER):
        self.position = position
        self.radius = max(1, radius)
        self.filled = filled
        self.thickness = thickness
        self.circ_shader = circ_shader
        return
    
    def render(self):
        # Single Point
        if self.radius == 1:
            return [[self.position, 0]]
        # Circle
        else:
            pixels = []
            for x in range(floor(self.position[0]-self.radius), ceil(self.position[0]+self.radius+1)):
                for y in range(floor(self.position[1]-self.radius), ceil(self.position[1]+self.radius+1)):
                    dist = shape_util.distance(self.position, [x, y])
                    # Filled or not
                    if (self.filled and dist <= self.radius) or (self.radius and self.radius - self.thickness <= dist <= self.radius + self.thickness):
                        pixels.append([self.circ_shader.vertex([x,y]), self.circ_shader.fragment([x, y])])
        return pixels
    
    def __repr__(self):
        return f"Circle({self.position}, {self.radius}, {self.filled}, {self.thickness}, {self.circ_shader})"