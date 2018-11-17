from plot import Plot
class Terrain:
    def __init__(self, size=(40,40), filler= " "):
        self.size = size
        self.filler = filler
        self.terrain = [[self.filler for i in range(size[0])] for j in range(size[1])]
    
    def add_circle(self,plotter,radius,center=(0,0), char='#'):
        coordinates = plotter.get_circle(radius,center)
        for c in coordinates:
            self.terrain[c[0]][c[1]] = char