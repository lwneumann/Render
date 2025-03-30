from math import ceil


class Gradient:
    def __init__(self, c_scale, gradient_size=100, out_of_range=(0, 0, 0)):
        self.c_range = []
        self.gradient_size = gradient_size
        self.make_range(c_scale)
        self.out_of_range = out_of_range
        return
    
    def make_range(self, c_scale):
        step_count = len(c_scale)-1
        step_size = ceil(self.gradient_size / step_count)

        for step in range(step_count):
            change = [ (c_scale[step+1][clr] - c_scale[step][clr]) / step_size for clr in range(3) ]
            for s in range(step_size):
                self.c_range.append( [c_scale[step][clr] + s*change[clr] for clr in range(3)] )
        return

    def __getitem__(self, index):
        if 0 <= index < len(self.c_range):
            return tuple([ int(self.c_range[index][c]) for c in range(3) ])
        else:
            return self.out_of_range
