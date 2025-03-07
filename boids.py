from random import randint, random
from math import pi, cos, sin


BOID_DETECTION_R = 5
BOID_SIZE = 5
BOID_SPEED = 2

SEPERATION_FACTOR = 1
ALIGNMENT_FACTOR = 0.5
COHESION_FACTOR = 0.5


def dist(x1, y1, x2, y2, size):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    
    if dx > size[0] / 2:
        dx = size[0] - dx
    if dy > size[1] / 2:
        dy = size[1] - dy

    return (dx**2 + dy**2)**0.5


class Boid:
    def __init__(self, size, angle=None, x=None, y=None):
        self.color = randint(46, 219), randint(46, 199), 219
        if angle is None:
            self.angle = random() * 2 * pi
        else:
            self.angle = angle

        if x is None:
            self.x = randint(0, size[0])
        else:
            self.x = x

        if y is None:
            self.y = randint(0, size[1])
        else:
            self.y = y
        return
    
    def __str__(self):
        return "(" + self.x + ", " + self.y + ")"

    def __repr__(self):
        return "(" + self.x + ", " + self.y + ")"


class Flock:
    def __init__(self, b_count, size):
        self.boids = [Boid(size) for b in range(b_count)]
        self.size = size
        return
    
    def get_avg_boid(self, ind):
        x = self.boids[ind].x
        y = self.boids[ind].y

        n_count = 0
        av_dist = [0, 0]
        av_angle = self.boids[ind].angle
        av_pos = [0, 0]

        for bc, b in enumerate(self.boids):
            if bc != ind:
                if dist(b.x, b.y, x, y, self.size) <= BOID_DETECTION_R:
                    n_count += 1
                    
                    av_dist[0] += abs(b.x - x)
                    av_dist[1] += abs(b.y - y)
                    
                    av_angle += b.angle

        if n_count != 0:
            av_dist = [SEPERATION_FACTOR * av_dist[1] / n_count, SEPERATION_FACTOR * av_dist[0] / n_count]
            av_angle = ALIGNMENT_FACTOR * av_angle / n_count
            av_pos = [COHESION_FACTOR * av_pos[0] / n_count, COHESION_FACTOR * av_pos[1] / n_count]
        return av_dist, av_angle, av_pos, n_count

    def __getitem__(self, i):
        return self.boids[i]

    def run(self):
        new_boids = []
        for bc, b in enumerate(self.boids):
            av_dist, av_angle, av_pos, n_count = self.get_avg_boid(bc)
            n_x = (av_dist[0] + av_pos[0] + cos(b.angle) * BOID_SPEED) % self.size[0] - 1
            n_y = (av_dist[1] + av_pos[1] + sin(b.angle) * BOID_SPEED) % self.size[1] - 1
            
            new_boids.append(Boid(self.size, angle=av_angle, x=n_x, y=n_y))
        
        self.boids = new_boids
        return

    def step(self, frame_count=0, last_frame=None):
        frame = None
        if frame is None:
            frame = [ [(0, 0, 0) for r in range(self.size[0])] for c in range(self.size[1]) ]

        self.run()

        for b in self.boids:
            for x in range(int(b.x) - BOID_SIZE, int(b.x) + BOID_SIZE+1):
                for y in range(int(b.y) - BOID_SIZE, int(b.y) + BOID_SIZE+1):
                    if dist(x, y, b.x, b.y, self.size) < BOID_SIZE:
                        frame[y%self.size[1]][x%self.size[0]] = b.color

        return frame


def get_step(size):
    return Flock(20, size).step