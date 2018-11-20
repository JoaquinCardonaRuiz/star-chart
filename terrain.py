from plot import Plot
from entities.bodies import *
class Terrain:
    def __init__(self, star_radius):
        self.size = (pyxel.width,pyxel.height)
        self.terrain = [[Empty() for i in range(self.size[0])] for j in range(self.size[1])]
        self.terrain[int(len(terrain)/2)][int(len(terrain[0])/2)] = Star(star_radius)
    
    def add_circle(self,plotter,radius,center=(0,0), char='#'):
        coordinates = plotter.get_circle(radius,center)
        for c in coordinates:
            self.terrain[c[0]][c[1]] = char

class Empty:
    def __init__(self):
        pass
    
    def search(self):
        return("Empty")