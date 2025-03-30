import file_maker
from shapes.component import Component
import shaders.shader as shader


class Window:
    def __init__(self, screen_size, simulation_size, frame_name='testFrame', loop_screen=False, unset_color=(0, 0, 0), default_color=(255, 255, 255), win_shader=None, fps=60, seconds=4):
        self.screen_size = screen_size
        self.sim_size = simulation_size
        self.loop_screen = loop_screen
        self.components = []
        self.default_color = default_color
        self.unset_color = unset_color
        self.win_shader = win_shader
        self.fps = fps
        self.seconds = seconds
        self.frames = fps * seconds        
        self.frame_name = frame_name
        return
    
    def add_components(self, *comps):
        for comp in comps:
            if isinstance(comp, list) or isinstance(comp, tuple):
                for c in comp:
                    self.add_components(c)
            else:
                self.components.append(comp)
        return

    def render(self):
        frame = [ [self.unset_color for c in range(self.screen_size[0])] for r in range(self.screen_size[1]) ]

        # Include each components frame
        for comp in self.components:
            comp_pixels = comp.render()

            # Compile colors
            for pixel_info in comp_pixels:
                pix_pos, pix_col = pixel_info
                # Set colors
                if pix_col is None:
                    pix_col = self.unset_color
                elif pix_col is False:
                    pix_col = self.default_color
                
                pix_x = int(pix_pos[0])
                pix_y = int(pix_pos[1])
                # Offset for components internal position and loop screen
                if isinstance(comp, Component):
                    pix_x += comp.global_position[0]
                    pix_y += comp.global_position[1]
                # If looping screen, mod coords
                if self.loop_screen:
                    pix_x = pix_x % self.sim_size[0]
                    pix_y = pix_y % self.sim_size[1]
                    frame[pix_y][pix_x] = pix_col
                # Otherwise only plot when in bound
                elif 0 <= pix_x < self.sim_size[0] and 0 <= pix_y < self.sim_size[1]:
                    frame[pix_y][pix_x] = pix_col

        # Apply Global Shader
        if self.win_shader is not None:
            new_frame = [ [self.unset_color for c in range(self.screen_size[0])] for r in range(self.screen_size[1]) ]
            for row in range(len(frame)):
                for col in range(len(frame[0])):
                    new_p = self.win_shader.vertex([col, row], frame[row][col])
                    new_c = self.win_shader.fragment([col, row], frame[row][col])
                    new_frame[new_p[1]][new_p[0]] = new_c
            frame = new_frame

        return frame

    def render_frame(self):
        file_maker.array_to_png(self.render(), filename=self.frame_name, folder='.')
        return
