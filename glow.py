import FileAnimate
from math import exp, ceil, pi, cos, sin
from random import randint, random

import FileAnimate.file_maker


def bump(x, y, amp, hshift, vshift, period):
    r = ((x-hshift)**2 + (y-vshift)**2) ** 0.5
    if -period < r < period:
        v = amp * exp( 1/( ((r)/period)**2 - 1) +1 )
    else:
        v = 0
    return v


class Gradient:
    def __init__(self, c_scale, gradient_size=100):
        self.c_range = []
        self.gradient_size = gradient_size
        self.make_range(c_scale)
        return
    
    def make_range(self, c_scale):
        step_count = len(c_scale)-1
        step_size = ceil(self.gradient_size / step_count)

        for step in range(step_count):
            change = [ (c_scale[step+1][clr] - c_scale[step][clr]) / step_size for clr in range(3) ]
            for s in range(step_size):
                self.c_range.append( [c_scale[step][clr] + s*change[clr] for clr in range(3)] )
        return

    def __getitem__(self, index):
        if 0 <= index < len(self.c_range):
            return tuple([ int(self.c_range[index][c]) for c in range(3) ])
        else:
            return (0, 0, 0)


class Flame:
    def __init__(self, spawn_buffer, size):
        self.pos = [randint(spawn_buffer, size[0]-spawn_buffer), randint(spawn_buffer, size[1]-spawn_buffer)]
        angle = random()*2*pi
        self.dir = [cos(angle), sin(angle)]
        self.speed = randint(1, 5)
        self.borders = size
        self.edge_buffer = spawn_buffer
        return

    def __getitem__(self, index):
        return int(self.pos[index])

    def move(self):
        for dimen in range(len(self.dir)):
            self.pos[dimen] = min(max(self.pos[dimen] + self.dir[dimen] * self.speed, self.edge_buffer), self.borders[dimen]-self.edge_buffer-1)
        return


class Torch:
    # Because it holds flames? idk
    def __init__(self):
        self.flames = []
        self.gradient = Gradient(
            [(255, 255, 255), (255, 247, 93), (255, 153, 31), (254, 101, 13), (243, 60, 4), (218, 31, 5), (161, 1, 0), (80, 0, 0), (20, 0, 0), (0, 0, 0)][::-1]
        )
        self.size = [500, 500]
        self.flame_count = 9
        self.flame_r = 30
        self.spawn_buffer = self.flame_r + 10
        
        for f in range(self.flame_count):
            self.flames.append(Flame(self.spawn_buffer, self.size))
        return

    def step(self, prior_frame=None, frame_count=0):
        frame = prior_frame
        if frame is None:
            frame = [ [(0, 0, 0) for c in range(self.size[1])] for r in range(self.size[0]) ]

        for f in range(self.flame_count):
            # Move
            self.flames[f].move()

            # Render
            f_x = self.flames[f][0]
            f_y = self.flames[f][1]
            for row in range(self.flame_r - f_y, self.flame_r + f_y):
                for col in range(self.flame_r - f_x, self.flame_r + f_x):
                    color = self.gradient[int(bump(col, row, 100, f_x, f_y, self.flame_r))]
                    if sum(color) > sum(frame[row][col]):
                        frame[row][col] = color
                    # frame[row][col] = tuple( [ max(color[i], p[row][col][i]) for i in range(3) ] )
        return frame


if __name__ == "__main__":
    t = Torch()

    FPS = 20
    SECONDS = 3
    FRAME_COUNT = SECONDS * FPS

    FileAnimate.file_maker.render_video(t.step, frames=FRAME_COUNT, fps=FPS, mode="RGB")
