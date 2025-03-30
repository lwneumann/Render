import shapes.shape_util as util
import shaders.shader as shader

# TODO add thickness

class Line:
    def __init__(self, p1, p2, lshader=shader.DEFAULT_SHADER):
        self.p1 = p1
        self.p2 = p2
        self.lshader = lshader
        return

    def render(self):
        return [ [self.lshader.vertex(p), self.lshader.fragment(p)] for p in util.make_line(self.p1[0], self.p1[1], self.p2[0], self.p2[1])]
