from random import randint


class Cellular:
    def __init__(self, screen_size, grid_size):
        self.size = grid_size
        self.screen_size = screen_size
        self.rules = [
            [
                [randint(0, 1) for col in range(3)]
                for row in range(3)
            ],
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ]
        ]
        return
    
    def step(self):
        print('headsdas')
        return 


def get_step(size):
    Cellular(size).step()
    return