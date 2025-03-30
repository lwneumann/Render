import file_maker
from math import cos, sin, pi


size = 800, 800
FPS = 50
SECONDS = 4
TOTAL_FRAMES = FPS * SECONDS


def sub_list(start, end, subdivisions):
    grain = (end - start) / subdivisions
    return [round(start + i * grain, 10) for i in range(subdivisions + 1)]


def get_c(t, x, y):
    return (
        255,
        255,
        255
    )
    # return (
        # int( (255/2)*(cos(t) + 1)*(sin(t) + 1) ),
        # int( (255/2)*(cos(t) + 1) ),
        # int( (255/2)*(cos(t**2) + 1)*(sin(t) + 1) ))


def spiral(p, i):
    theta = lambda a: ( a )/( pi )
    spiral_len = lambda a: 3*a
    theta_0 = theta(i)
    theta_1 = theta(i+1)
    subdivs = 10 * (i+1)

    for t in sub_list(theta_0, theta_1, subdivs):
        sp_len = t/32

        x1 = int( (size[1]/2) + spiral_len(t) * sp_len * cos(t) )
        y1 = int( (size[0]/2) + spiral_len(t) * sp_len * sin(t) )
        if 0 <= x1 < size[1] and 0 <= y1 < size[0]:
            p[y1][x1] = get_c(t, x1, y1)
        
        # x2 = int( (size[1]/2) + 0.8 * spiral_len(t) * sp_len * cos(-t) )
        # y2 = int( (size[0]/2) + 0.8 * spiral_len(t) * sp_len * sin(-t) )
        # if 0 <= x2 < size[1] and 0 <= y2 < size[0]:
        #     p[y2][x2] = get_c(t, x2, y2)

    return p


def blur(p):
    for r in range(size[0]):
        for c in range(size[1]):
            if sum(p[r][c]) > 0:
                p[r][c] = (
                    max(p[r][c][0] - 15, 0),
                    max(p[r][c][1] - 12, 0),
                    max(p[r][c][2] - 5, 0)
                )
    return p


def step(p, i):
    if p is None:
        p = [ [(0, 0, 0) for c in range(size[1])] for r in range(size[0]) ]

    # Disortion
    p = blur(p)

    # Spiral
    p = spiral(p, i)
    return p


if __name__ == "__main__":
    file_maker.render_video(step, TOTAL_FRAMES, FPS, mode="RGB")
