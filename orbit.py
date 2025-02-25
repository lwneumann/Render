from random import random
import FileAnimate, MinecraftAnimate
from math import cos, sin, pi

import FileAnimate.file_maker
import MinecraftAnimate.main


class Body:
    """
    Fake Orbits!
    Just follows transform matricies to rotate
    """
    def __init__(self, pos, radius, size, orb_r, color=(100, 100, 255), moves=True, dir=1, theta=None, phi=None):
        # Body Position
        self.pos = pos
        # Body Radius
        self.radius = radius
        # Size is window size used to give a centered output pos
        self.size = size
        # Orbit Radius
        self.orbit_r = orb_r
        self.color = color
        # Does it move
        self.moves = moves
        # Direction of movement clockwise or !
        self.dir = dir
        # -- These can be left alone and they will rotate if defined, it locks that axis tilt
        # x tilt
        self.theta = theta
        # y tile
        self.phi = phi
        return

    def move(self, angle, theta=None, phi=None):
        if theta is None:
            theta = angle
        if phi is None:
            phi = angle
        # Rotation Speed
        angle = angle / (4 * pi)
        # Gets tilts unless fixed
        # theta
        if self.theta is None:
            theta = self.dir * theta / (24 * pi)
        else:
            theta = self.theta
        # phi
        if self.phi is None:
            phi = self.dir * phi / (16 * pi)
        else:
            phi = self.phi

        # Rotate the bod
        self.pos = [
            self.size[0]/2 + self.orbit_r * ( cos(angle) * cos(phi) + sin(angle) * sin(theta) * sin(phi)),
            self.size[1]/2 + self.orbit_r * sin(angle) * cos(theta),
            self.size[2]/2 + self.orbit_r * ( sin(angle) * sin(theta) * cos(phi) - cos(angle) * sin(phi) )
        ]
        return

    def __repr__(self):
        return self.pos

    def dist(self, other_pos):
        # eulic dist
        return sum([ (self.pos[dimension] - other_pos[dimension])**2 for dimension in range(len(other_pos))]) ** 0.5


class BodSystem:
    def __init__(self, size):
        # Window size
        self.size = size
        # Cubes off to three dimentions if you are giving just the picture size
        if len(size) == 2:
            size.append(size[0])

        # Probably generalize later but for now explicitly constructing system.
        self.bodies = [
            # Center body
            Body([size[0]/2, size[1]/2, size[2]/2], 40, size, 0, color=(253, 184, 19), moves=False),
            # Orbiter
            Body([0, 0, 0], 20, size, 100, phi=0),
            # Smaller orbiter
            Body([0, 0, 0], 10, size, 200, color=(100, 255, 100), dir=-1, theta=3/2*pi, phi=0)
        ]
        return

    def step(self, prior_frame=None, frame_count=None):
        # frame = prior_frame
        frame = None
        if frame is None:
            frame = [[ (0, 0, 0) for c in range(self.size[0])] for r in range(self.size[1])]

        for bod in self.bodies:
            if bod.moves:
                # Defaults theta and phi to be angles
                bod.move(frame_count)

        self.bodies.sort(key=lambda bod: bod.pos[2])

        for bod in self.bodies:
            for x in range(int(bod.pos[0]) - bod.radius, int(bod.pos[0]) + bod.radius+1):
                for y in range(int(bod.pos[1]) - bod.radius, int(bod.pos[1]) + bod.radius+1):
                    if bod.dist((x, y)) < bod.radius:
                        frame[y][x] = bod.color

        return frame


if __name__ == "__main__":
    size = [500, 500]
    s = BodSystem(size)
    FPS = 30
    SECONDS = 10
    FRAMES = FPS * SECONDS
    # FileAnimate.file_maker.render_video(s.step, frames=FRAMES, fps=FPS, video_folder="TestOutputs")
    MinecraftAnimate.main.render_datapack(s.step, pack_name="OrbitPack", fps=FPS, seconds=SECONDS, uses_blockname=False, size=size)
