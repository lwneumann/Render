from FileAnimate import file_maker
from random import randint
from perlin_noise import PerlinNoise


def noise_to_color(n):
    # Greyscale color from noise
    return tuple([ int((1 + n) * 255/2) for _ in range(3) ])


def make_noise(width, height, octaves_mul=1, to_color=True, fixed_seed=None):
    if fixed_seed is not None:
        noise1 = PerlinNoise(octaves=3*octaves_mul, seed=fixed_seed)
        noise2 = PerlinNoise(octaves=6*octaves_mul, seed=fixed_seed)
        noise3 = PerlinNoise(octaves=12*octaves_mul, seed=fixed_seed)
        noise4 = PerlinNoise(octaves=24*octaves_mul, seed=fixed_seed)
    else:
        noise1 = PerlinNoise(octaves=3*octaves_mul)
        noise2 = PerlinNoise(octaves=6*octaves_mul)
        noise3 = PerlinNoise(octaves=12*octaves_mul)
        noise4 = PerlinNoise(octaves=24*octaves_mul)

    pic = []
    for j in range(height):
        row = []
        for i in range(width):
            noise_val = noise1([i/width, j/height])
            noise_val += 0.5 * noise2([i/width, j/height])
            noise_val += 0.25 * noise3([i/width, j/width])
            noise_val += 0.125 * noise4([i/width, j/height])

            if to_color:
                noise_val = noise_to_color(noise_val)

            row.append(noise_val)
        pic.append(row)
    return pic


def lined_noise(width, height, om=1, line_count = 20, fixed_seed=None):
    line_grain = 2 / line_count
    line_width = line_grain / 20

    noise_p = make_noise(width, height, octaves_mul=om, to_color=False, fixed_seed=fixed_seed)

    for x in range(width):
        for y in range(height):
            val = noise_p[y][x]
            if abs(val - round(val / line_grain) * line_grain) <= line_width:
                noise_p[y][x] = (200, 200, 255) #noise_to_color(val)
            else:
                noise_p[y][x] = (0, 0, 0)

    return noise_p


class Line:
    def __init__(self, size, frames):
        self.width, self.height = size
        self.frames = frames
        self.seed = randint(1, 999999)
        return
    
    def step(self, frame_count=0, last_frame=None):
        return lined_noise(self.width, self.height, line_count=1+frame_count, fixed_seed=self.seed)


def get_step(size, frames):
    return Line(size, frames).step


if __name__ == "__main__":
    file_maker.array_to_png(lined_noise(500, 500, 4), "Perlin7", "./TestOutputs")
