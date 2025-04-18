import file_maker


def pixel_to_complex(r, c, size, x_min=-2, x_max=2, y_min=-2, y_max=2):
    """
    0, 0       -> x_min, y_min
    size, size -> x_max, y_max
    """
    x = x_min + (c / size) * (x_max - x_min)
    y = y_min + (r / size) * (y_max - y_min)
    return complex(x, y)


def is_stable(c, num_iterations):
    z = 0
    try:
        for _ in range(num_iterations):
            z = z ** 2 + c
            if abs(z) > 2:
                return False
    # Some are big :(
    except OverflowError:
        return False
    return True


def make_brot(n=500, iterations=5):
    brot = [[(0, 0, 0) for c in range(n)] for r in range(n)]

    for r in range(n):
        for c in range(n):
            if is_stable(pixel_to_complex(r, c, n, n), iterations):
                brot[r][c] = (255, 255, 255)
    return brot


if __name__ == "__main__":
    file_maker.array_to_png(make_brot())