import file_maker
from math import cos, sin, pi, exp


size = 800, 1200
FPS = 50
SECONDS = 5
TOTAL_FRAMES = FPS * SECONDS


def map_color(val, r, c, ind, i):
    # return int(abs((255-val) * cos(val / (ind+1))))
    return max(min(int(
            val - 5*(
                ((3-ind)) * cos(((c+1)/size[1])*((size[0] - r)/size[0]))
                )
        ), 255), 0)


def get_wave(i, p=None):
    if p is None:
        p = [ [(0, 0, 0) for c in range(size[1])] for r in range(size[0]) ]
    amp = size[0]*0.9 / 2
    period = size[1]
    hshift = i * (size[1] / ( 8 * (TOTAL_FRAMES-1)))
    vshift = size[0]/2

    y = lambda s: amp * sin(((2*pi*(( (exp(s/600) + 1)* s)-hshift))/period)) + vshift

    for r in range(size[0]):
        for c in range(size[1]):
            if sum(p[r][c]) > 0:
                new_color = tuple([map_color(p[r][c][c_val], r, c, c_val, i) for c_val in range(3)])
                p[r][c] = new_color

    for x in range(size[1]):
        y_pos = int(y(x))
        # p[min(max(y_pos-1, 0), size[0]-1)][x] = (255, 255, 255)
        p[min(max(y_pos, 0), size[0]-1)][x] = (255, 255, 255)
        p[min(max(y_pos+1, 0), size[0]-1)][x] = (255, 255, 255)
    
    return p


def step(p, i):
    return get_wave(i, p)


if __name__ == "__main__":
    # file_maker.array_to_png(get_wave(0), folder='', filename='sintest2-thickness', mode="RGB")
    file_maker.render_video(step, fps=FPS, frames=TOTAL_FRAMES)
