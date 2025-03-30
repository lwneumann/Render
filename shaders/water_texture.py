"""
Although it does work its pretty slow.
"""
from perlin_noise import PerlinNoise
import shaders.shader as shader


class WaterTexture(shader.Shader):
    def __init__(self, size, def_color=(50, 50, 255), water_intensity=0.5, noise_depth=3, base_octave=3):
        super().__init__(def_color)
        self.intensity = water_intensity
        self.size = size
        self.noise = []
        self.noise_weight = []
        self.make_noise(noise_depth, base_octave)
        return
    
    def make_noise(self, noise_depth, base_octave):
        for n in range(noise_depth):
            self.noise.append(PerlinNoise(octaves=base_octave * (n+1)))
            self.noise_weight.append(1/(n+1))
        return
 
    def fragment(self, pix, color=(255, 255, 255), frame=0):
        """
        Given a point return new color
        """
        if pix in [None, False]:
            return pix
        
        val = 0
        for n in range(len(self.noise)):
            val += self.noise_weight[n] * self.noise[n]([pix[0]/self.size[0], pix[1]/self.size[1]])
        
        val = (val/2)+0.5

        new_col = tuple([int(
            (1-self.intensity)*color[i] + self.intensity * self.color[i] * val
            ) for i in range(3) ])

        return new_col

    def vertex(self, pix, color=(255, 255, 255), frame=0):
        """
        Given a point, return new position
        """
        return [pix[0], pix[1]]