from shapes.circle import Circle
from shapes.line import Line
from shapes.polygon import Polygon
from animal import Animal
import shapes.shape_util as util
import shaders.shader as shader
from shaders.water_texture import WaterTexture
import file_maker, window, shapes.component as component

import animal

from math import pi, cos, sin, acos, asin
from random import randint


class LineTest:
    def __init__(self, size, frames):
        self.angle_step = 4 * pi / frames
        self.size = size
        self.r = min(size) * 0.3
        self.frames = frames

        self.wind = window.Window(size, size)
        self.wind.components.append(component.Component(position=[int(size[0]/2),int(size[1]/2)]))
        return

    def step(self, frame_count=0, last_frame=None):
        if frame_count > self.frames/2:
            self.wind.loop_screen = True

        p1x = self.r * cos(frame_count * self.angle_step)
        p1y = self.r * sin(frame_count * self.angle_step)

        self.wind.components[0].points = [[p1x, p1y], [0, 0]]

        return self.wind.render()

def makeLineTest():
    FPS = 60
    SECONDS = 6
    FRAMES = FPS * SECONDS
    file_maker.render_video(LineTest([400, 400], FRAMES).step, FRAMES, FPS, video_name='vTest')
    return


def componentTest():
    size = [30, 30]
    w = window.Window(size, size)
    c = component.Component(filled=True)
    c.points = [[28, 5], [5, 8], [16, 27]]
    w.add_components(c)
    file_maker.array_to_png(w.render(), filename='fillTest', folder='.')
    return


def circleTest():
    size = [200, 200]
    w = window.Window(size, size)
    c1 = Circle([100, 100], 50)
    c2 = Circle([50, 50], 25, filled=False, thickness=1, circ_shader=shader.Shader((100, 100, 255)))
    c3 = Circle([75, 80], 25, filled=False, circ_shader=shader.Shader((255, 100, 100)))
    w.add_components(c1, c2, c3)
    file_maker.array_to_png(w.render(), filename='cTest', folder='.')
    return


def lineClassTest():
    size = [200, 200]
    w = window.Window(size, size)
    lines = [Line([randint(0, size[0]-1), randint(0, size[1]-1)], [randint(0, size[0]-1), randint(0, size[1]-1)]) for l in range(5)]
    w.add_components(lines)
    file_maker.array_to_png(w.render(), filename='lines', folder='.')
    return


def boneTest():
    size = [200, 200]
    w = window.Window(size, size)
    
    b = animal.Bone([100, 100], 20)
    c1, c2 = b.get_sides()
    c1 = Circle(c1, 2, circ_shader=shader.RED)
    c2 = Circle(c2, 2, circ_shader=shader.RED)

    w.add_components(b, c1, c2)

    file_maker.array_to_png(w.render(), filename='boneTest', folder='.')
    return


class NormalizeTest:
    def __init__(self, size, frames):
        self.angle_step = 4 * pi / frames
        self.size = size
        self.r = min(size) * 0.3
        self.frames = frames
        self.pos = [size[0]/2, size[1]/2]
        self.other_pos = [size[0]/2+self.r, size[1]/2]

        self.wind = window.Window(size, size)
        self.c1 = Circle(self.pos, 4, circ_shader=shader.BLUE)
        self.c2 = Circle(self.other_pos, 4, circ_shader=shader.RED)
        self.l = Line(self.pos, self.other_pos)

        self.wind.add_components(self.l, self.c2, self.c1)
        return

    def step(self, frame_count=0, last_frame=None):
        self.other_pos = [self.pos[0] + (20 + self.r) * cos(frame_count * self.angle_step), self.pos[1] + (20 + self.r) * sin(frame_count * self.angle_step)]
        self.l.p2 = self.normalize_pos(self.other_pos)
        self.c2.position = self.other_pos
        return self.wind.render()

    def normalize_pos(self, p):
        dist = util.distance(self.pos, p)
        if dist > self.r:
            dx = p[0] - self.pos[0]
            dy = p[1] - self.pos[1]

            if dx != 0:
                theta = acos(dx/dist)
            else:
                theta = asin(dy/dist)
            if dy < 0:
                theta = 2*pi - theta

        return [self.pos[0] + cos(theta) * self.r, self.pos[1] + sin(theta) * self.r]

def normalizePosTest():
    FPS = 60
    SECONDS = 6
    FRAMES = FPS * SECONDS
    file_maker.render_video(NormalizeTest([400, 400], FRAMES).step, FRAMES, FPS, video_name='normalizePoints')
    return


class SpineTest:
    def __init__(self, size, frames):
        self.size = size
        self.r = 0
        self.max_r = min(size) * 0.3
        self.r_step = 0.5
        self.frames = frames
        self.pos = [size[0]/2, size[1]/2]
        self.angle = 0
        self.turn_rate = 0.02

        self.spine = Animal(8, [15, 18, 15, 14, 10], self.pos, show_bones=True)
        
        # wat = WaterTexture(size=size)
        self.wind = window.Window(size, size)
        self.wind.add_components(self.spine)
        return

    def step(self, frame_count=0, last_frame=None):
        if self.r != self.max_r:
            self.r = min(self.r + self.r_step, self.max_r)
        self.angle += self.turn_rate
        if self.angle >= 2*pi:
            self.angle -= 2*pi

        new_p = [self.pos[0] + self.r * cos(self.angle), self.pos[1] + self.r * sin(self.angle)]
        self.spine.move_and_turn(new_p)

        return self.wind.render()

def doSpineTest():
    FPS = 60
    SECONDS = 8
    FRAMES = FPS * SECONDS
    file_maker.render_video(SpineTest([400, 400], FRAMES).step, FRAMES, FPS, video_name='spine')
    return


def waterTest():
    size = [200, 200]
    wat = WaterTexture(size=size)
    w = window.Window(size, size, win_shader=wat)

    c1 = Circle([100, 100], 50)
    c2 = Circle([50, 50], 25, filled=False, thickness=1, circ_shader=shader.RED)
    c3 = Circle([75, 80], 25, filled=False, circ_shader=shader.GREEN)
    w.add_components(c1, c2, c3)

    file_maker.array_to_png(w.render(), filename='waterTexture', folder='.')
    return


def polygonTest():
    size = [300, 300]
    wat = WaterTexture(size=size, water_intensity=0.9)
    w = window.Window(size, size, "polygonFilled2")

    points = [
        (40, 40),
        (150, 200),
        (100, 280),
        (280, 175),
        (10, 40)
    ]
    p = Polygon(points, thickness=0, poly_shader=wat)
    w.add_components(p)

    w.render_frame()
    return


def boneSpreadTest():
    size = [600, 600]
    w = window.Window(size, size, "boneSpread")
    
    for r in range(6):
        if r in (0, 3):
            num = 1
        for c in range(6):
            num += 1
            x = 50 + 100*c
            y = 50 + 100*r
            direction = r <= 3
            b = animal.Bone([x, y], 20)
            w.add_components(b)
            b_sides = b.get_sides(num_points=num, front=direction)
            for i, c in enumerate(b_sides):
                shad = shader.RED if i in [0, len(b_sides)-1] else shader.BLUE
                c = Circle(c, 2, circ_shader=shad)
                w.add_components(c)
    w.render_frame()
    return


if __name__ == "__main__":
    doSpineTest()
