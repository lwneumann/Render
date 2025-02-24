import file_maker
from alive_progress import alive_bar
from math import sin, cos, pi


def normalize(i):
    # [-1, 1] -> [0, 255]
    return int(i*127.5 + 127.5)


def trig_img(p, size=500):
    # x3 of:
    #  0 - Outer coef
    #  1 - sin coef
    #  2 - power of c in sin
    #  3 - power of r in sin
    #  4 - cos coef
    #  5 - power of c in cos
    #  6 - power of r in cos
    i = [
            [tuple([normalize(
                p[_][0] * sin( p[_][1] * (c**p[_][2]) * (r**p[_][3]) * (pi/size) ) * cos( p[_][4] * (c**p[_][5]) * (r**p[_][6]) * (pi/size) )
            ) for _ in range(3)] + [255]
                ) for c in range(size)
            ] for r in range(size)
        ]
    return i


def vid_test():
    p = [
        [2, 1, 0, 1, 1, 1, 0] for _ in range(3)
    ]

    print()
    print('-'*20)
    print()
    print('-Rendering')
    frames = 90

    p[2][2] = 1

    with alive_bar(frames) as bar:
        for i in range(frames):
            file_maker.array_to_png(trig_img(p), i)
            # p[0][1] += 0.3
            # p[0][4] += 0.3
            # p[1][1] += 0.3
            # p[1][4] += 0.3
            # p[2][1] += 0.3
            # p[2][4] += 0.3

            # p[0][3] += 1/frames
            # p[0][5] += 1/frames

            p[2][6] += 2/frames

            bar()

    print()
    file_maker.make_mp4()
    print()
    print('-'*20)
    print()
    return


# p = [
    # [2, 1, 0, 1, 1, 1, 0],
    # [2, 1, 0, 1, 1, 1, 2],
    # [2, 1, 1, 1, 1, 1, 0]
# ]

# file_maker.array_to_png(trig_img(p), folder='./')

if __name__ == "__main__":
    vid_test()