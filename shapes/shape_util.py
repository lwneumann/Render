from math import pi, acos, asin


# Return set of points that create a line between them
def make_line(x1, y1, x2, y2):
    line = []
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    # Equivelent points
    if x1 == x2 and y1== y2:
        return [[x1, y1]]

    # Straight Lines
    if x1 == x2:
        if y1 > y2:
            y1, y2 = y2, y1

        for y in range(y1, y2+1):
            line.append([x1, y])
    elif y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1

        for x in range(x1, x2+1):
            line.append([x, y1])
    # Actual Lines
    else:
        dx = x1 - x2
        dy = y1 - y2
        dirx = -1 if x1 > x2 else 1
        diry = -1 if y1 > y2 else 1

        # Line in terms of x
        if abs(dx) > abs(dy):
            m = abs(dy / dx)
            for x_i in range(abs(dx)):
                px = x1 + x_i * dirx
                py = y1 + x_i * diry * m
                line.append([int(px), int(py)])
        # Line in terms of y
        else:
            m = abs(dx / dy)
            for y_i in range(abs(dy)):
                px = x1 + y_i * dirx * m
                py = y1 + y_i * diry
                line.append([int(px), int(py)])
    return line


# Euclid Distance using smallest dimension of the points
def distance(p1, p2):
    return sum([(p1[i] - p2[i])**2 for i in range(min(len(p1), len(p2)))])**0.5


# Gets angle between two points.
# Namely:
#             p2
#            /  |
#           /   |
#          /    |
#         /     |
#        /      |
#       /       |
#      /theta   |
#     p1--------O
#
# Often you may need distance for something else as well as theta
# If this is the case you can save a little time passing it in.
def get_angle(p1, p2, dist=None):
    if dist is None:
        dist = distance(p1, p2)

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    if dx != 0:
        theta = acos(dx/dist)
    else:
        theta = asin(dy/dist)
    # Offset angle ignoring half the circle
    if dy < 0:
        theta = 2*pi - theta
    return theta
