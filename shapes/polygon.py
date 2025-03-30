from shapes.line import Line
import shaders.shader as shader
from math import floor, ceil


class Polygon:
    def __init__(self, points, thickness=1, poly_shader=shader.DEFAULT_SHADER, line_shader=None):
        """
        Thickness:
            = 0 : filled
            > 0 : that thickness of lines

        Links first to last point
        """

        self.points = points
        self.filled = thickness == 0
        self.thickness = thickness
        self.p_shader = poly_shader
        self.l_shader = line_shader

        self.lines = []
        return
    
    def make_lines(self):
        for p_i in range(1, len(self.points)+1):
            if self.l_shader is None:
                self.lines.append(Line(self.points[p_i%len(self.points)], self.points[p_i-1]))
            else:
                self.lines.append(Line(self.points[p_i%len(self.points)], self.points[p_i-1], lshader=self.l_shader))
        return
    
    def get_footprint(self):
        x, y = zip(*self.points)
        return floor(min(x)), ceil(max(x)), floor(min(y)), ceil(max(y))

    def render(self):
        self.make_lines()

        pixels = []
        if self.thickness == 0:
            min_x, max_x, min_y, max_y = self.get_footprint()
            for y in range(min_y, max_y+1):
                for x in range(min_x, max_x):
                    count = 0
                    for p_i in range(len(self.points)):
                        x1, y1 = self.points[p_i-1]
                        # x2, y2 = self.points[(p_i+1)%len(self.points)]
                        x2, y2 = self.points[p_i]
                        if (y < y1) != (y < y2) and x < x1 + ((y-y1)/(y2-y1)) * (x2-x1):
                            count += 1
                    if count%2 == 1:
                        pixels.append([self.p_shader.vertex([x, y]), self.p_shader.fragment([x, y])])
        # Render lines afterwards so they're on top
        if self.thickness != 0 or self.l_shader is not None:
            for line in self.lines:
                pixels += line.render()
        return pixels
