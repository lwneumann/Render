from shapes.circle import Circle
from shapes.polygon import Polygon
import shapes.shape_util as util
import shaders.shader as shader
from math import pi, cos, sin


class Bone:
    def __init__(self, position, meat_r, angle=0, min_angle=0, render_center=False, render_sides=False):
        self.position = position
        self.meat_r = meat_r
        self.min_angle = min_angle
        self.angle = angle
        self.render_center = render_center
        self.render_sides = render_sides
        
        self.circ = Circle(self.position, self.meat_r, filled=False, circ_shader=shader.BLUE)
        self.center = Circle(self.position, self.meat_r/10, filled=False, circ_shader=shader.RED)
        self.sides = [Circle(pos, meat_r/10, circ_shader=shader.RED) for pos in range(2)]
        self.get_sides()
        return

    def get_sides(self, num_points=2, front=True):
        # Orthagonal points to direction
        dir = 1 if front else -1
        point_angles = [pi/2 + dir*(pi/(num_points-1))*step for step in range(num_points)]
        sides = [ [ self.position[0] + self.meat_r * cos(self.angle + offset),
                   self.position[1] + self.meat_r * sin(self.angle + offset) ]
                  for offset in point_angles ]
        self.sides[0].position = sides[0]
        self.sides[1].position = sides[-1]
        return sides

    def render(self):
        pixels = self.circ.render()
        self.circ.position = self.position

        if self.render_center:
            self.center.position = self.position
            pixels += self.center.render()
        if self.render_sides:
            self.get_sides()
            pixels += self.sides[0].render
            pixels += self.sides[1].render

        return pixels

    def normalize_pos(self, other_bone):
        dist = util.distance(self.position, other_bone.position)
        new_p = other_bone.position, other_bone.angle
        if dist > self.meat_r:
            theta = util.get_angle(self.position, other_bone.position, dist)
            
            new_p = [self.position[0] + cos(theta) * self.meat_r, self.position[1] + sin(theta) * self.meat_r], theta
        return new_p

    def move(self, speed):
        self.position[0] += cos(self.angle) * speed
        self.position[1] += sin(self.angle) * speed
        return

    def __repr__(self):
        return f"Bone({self.position}, {self.meat_r}, {self.angle}, {self.circ})"


class Animal:
    def __init__(self, body_len, body_sizes, starting_pos, default_size=None, default_speed=2, show_bones=False, head_resolution=5, fill_shader=shader.GRAY, edge_shader=shader.DEFAULT_SHADER):
        self.default_speed = default_speed
        self.body_len = body_len
        self.body_sizes = body_sizes        
        self.show_bones = show_bones
        self.head_resolution = head_resolution
        self.fill_shader = fill_shader
        self.edge_shader = edge_shader

        self.default_size = self.body_sizes[-1] if default_size is None else default_size
        
        self.bones = []
        self.make_bones(starting_pos)
        return
    
    def render(self):
        pixels = []
        
        # Get Polygon outline
        points = []
        left_side = []
        right_side = []
        for bone_i, bone in enumerate(self.bones):
            # Adds resolution for number of sides to get, 2 is just left and right to define body
            full_sides = bone_i in (0, len(self.bones)-1)
            num_sides = self.head_resolution if full_sides else 2
            # Get sides
            bone_sides = bone.get_sides(num_points=num_sides, front=bone_i not in (0, len(self.bones)-1))
            if full_sides:
                # Add all other points to the left side - this is for when you want contours around face, back, \dots
                left_side += bone_sides
            else:
                # Otherwise split left and right.
                left_side += bone_sides[:-1]
                # Retype the right side into a list of the point so it can append the point
                # Not the coords to points
                right_side += [bone_sides[-1]]

        # Arrange and render Polygon
        points = left_side + right_side[::-1]

        skeleton = Polygon(points, thickness=0, poly_shader=self.fill_shader, line_shader=self.edge_shader)
        pixels += skeleton.render()
        
        # Gets bones of the animal if desired
        if self.show_bones:
            for bone in self.bones:
                pixels += bone.render()

        return pixels

    def get_size(self, b_i):
        if b_i >= len(self.body_sizes):
            return self.default_size
        else:
            return self.body_sizes[b_i]

    def make_bones(self, starting_pos):
        for b in range(self.body_len):
            self.bones.append(Bone(starting_pos.copy(), self.get_size(b)))
        return

    def move_spine(self):
        # Move down spine and ensure connectivity
        # This is front to back
        for bone_i in range(1, len(self.bones)):
            new_p, new_a = self.bones[bone_i-1].normalize_pos(self.bones[bone_i])
            self.bones[bone_i].position = new_p
            self.bones[bone_i].angle = new_a
        return

    def move_and_turn(self, new_pos):
        self.bones[0].angle = util.get_angle(self.bones[0].position, new_pos)
        self.bones[0].position = new_pos
        self.move_spine()
        return
