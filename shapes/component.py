from math import ceil
from shapes.shape_util import *
import shaders.shader as shader


class Component:
    def __init__(self, global_position=[0, 0], filled=False, priority=0):
        """
        Points are connected in order.
        """
        self.global_position = global_position
        self.points = []
        self.components = []
        self.shader = shader.DEFAULT_SHADER
        self.filled = filled
        self.priority = priority
        return

    def get_canvas_size(self):
        xmin = None
        xmax = None
        ymin = None
        ymax = None

        # Consider inner components
        for c in self.components:
            c_size, c_dims = c.get_canvas_size
            if xmax is None or c_dims[0] > xmax:
                xmax = c_dims[0]
            if xmin is None or xmin is None or c_dims[1] < xmin:
                xmin = c_dims[1]
            if ymax is None or c_dims[2] > ymax:
                ymax = c_dims[2]
            if ymin is None or c_dims[3] < ymin:
                ymin = c_dims[3]
        
        # Consider own points
        for p in self.points + self.points:
            # X range
            if xmin is None or p[0] < xmin:
                xmin = p[0]
            if xmax is None or p[0] > xmax:
                xmax = p[0]
            # Y range
            if ymin is None or p[1] < ymin:
                ymin = p[1]
            if ymax is None or p[1] > ymax:
                ymax = p[1]

        # Returns canvas size and dimensions
        return [[ceil(xmax - xmin)+1, ceil(ymax - ymin)+1], [xmax, xmin, ymax, ymin]]

    def draw_lines(self):
        line_points = []
        last_p = 0
        last_x = self.points[last_p][0]
        last_y = self.points[last_p][1]

        for p_i in range(1, len(self.points)):
            # Get points of the line
            line_points += make_line(last_x, last_y, self.points[p_i][0], self.points[p_i][1])

            # Prepare for next line
            last_p += 1
            if p_i < len(self.points):
                last_x = self.points[p_i][0]
                last_y = self.points[p_i][1]
        return line_points
    
    def fill(self, points):
        # Detect side to fill on
        active_spots = [[points[0][0], points[0][1]-1]]

        # Fill
        fill_directions = (
            (1, 0), (-1, 0),
            (0, 1), (0, -1)
        )
        while len(active_spots) > 0:
            activ_x = active_spots[0][0]
            activ_y = active_spots[0][1]
            for dir in fill_directions:
                new_pos = [activ_x + dir[0], activ_y + dir[1]]
                if new_pos not in points:
                    points.append(new_pos)
            active_spots.pop(0)
        return points

    def render(self):
        # Get point cords and colors
        render_points = []
        # Get points shaded by the component
        # TODO add internal components too
        if len(self.points) > 1:
            comp_render = []
            # Automatically links to the last point if filling.
            do_fill = self.filled and len(self.points) >= 3
            if do_fill:
                self.points.append(self.points[0])
                print(self.points)
            # Gather points
            for point in self.draw_lines():
                comp_render.append(point)
            # Back to filling
            if do_fill:
                comp_render = self.fill(comp_render)

            # Apply Shader
            for point_i in range(len(comp_render)):
                render_points.append([self.shader.vertex(comp_render[point_i]), self.shader.fragment(comp_render[point_i])])
        return render_points


if __name__ == "__main__":
    c = Component()
    c.points = [[5, 5], [0, 0], [1, 3]]
    print(c.get_canvas_size())
