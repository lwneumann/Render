from random import random
import FileAnimate
from math import cos, sin, pi

import FileAnimate.file_maker


class Body:
    def __init__(self, pos, radius, size, orb_r, color=(100, 100, 255), moves=True, dir=1, theta=None):
        self.pos = pos
        self.radius = radius
        self.size = size
        self.orbit_r = orb_r
        self.color = color
        self.moves = moves
        self.dir = dir

        self.theta = theta
        return

    def move(self, angle, theta):
        # Rotation Speed
        angle = angle / (4 * pi)
        # Axis Rotation Speed
        if self.theta is None:
            theta = self.dir * theta / (16 * pi)
        else:
            theta = self.theta
        self.pos = [
            self.orbit_r * cos(angle)               + self.size[0]/2,
            self.orbit_r * sin(angle) * cos(theta)  + self.size[1]/2,
            self.orbit_r * sin(angle) * sin(theta)  + self.size[2]/2
        ]
        return

    def __repr__(self):
        return self.pos

    def dist(self, other_pos):
        return sum([ (self.pos[dimension] - other_pos[dimension])**2 for dimension in range(len(other_pos))]) ** 0.5


class BodSystem:
    def __init__(self, size):
        self.size = size
        size.append(size[0])
        self.bodies = [
            Body([size[0]/2, size[1]/2, size[2]/2], 40, size, 0, color=(255, 100, 100), moves=False),
            Body([0, 0, 0], 20, size, 100, theta=0.5*pi),
            Body([0, 0, 0], 10, size, 200, color=(100, 255, 100), dir=-1, theta=3/2*pi)
        ]
        return

    def step(self, prior_frame=None, frame_count=None):
        # frame = prior_frame
        frame = None
        if frame is None:
            frame = [[ (0, 0, 0) for c in range(self.size[0])] for r in range(self.size[1])]

        for bod in self.bodies:
            if bod.moves:
                bod.move(frame_count, frame_count)

        self.bodies.sort(key=lambda bod: bod.pos[2])

        for bod in self.bodies:
            for x in range(int(bod.pos[0]) - bod.radius, int(bod.pos[0]) + bod.radius+1):
                for y in range(int(bod.pos[1]) - bod.radius, int(bod.pos[1]) + bod.radius+1):
                    if bod.dist((x, y)) < bod.radius:
                        frame[y][x] = bod.color

        return frame


if __name__ == "__main__":
    s = BodSystem([500, 500])
    FPS = 30
    SECONDS = 10
    FRAMES = FPS * SECONDS

    FileAnimate.file_maker.render_video(s.step, frames=FRAMES, fps=FPS, video_folder="TestOutputs")
