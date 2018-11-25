from plot import Plot
from entities.bodies import *
from random import randint
import configparser

class Terrain:
    def __init__(self, star_radius,logger,config):
        self.size = (75,75)
        self.terrain = [[Empty(j,i) for i in range(self.size[1])] for j in range(self.size[0])]
        self.gen_star(star_radius)
        self.config = config
        self.orbits = []
        self.gen_planets(int(self.config['Constants']['CantPlanets']))
        
    def gen_star(self,star_radius):
        middle = [int(self.size[0]/2),int(self.size[1]/2)]
        self.terrain[middle[0]][middle[1]] = Star(star_radius,middle[0],middle[1])


    def gen_planets(self, cant):
        while len(self.orbits) < cant:
            r = randint(6,int(self.size[0]/2))
            if all([(abs(r-c) > 2) for c in self.orbits]):
                self.orbits.append(r)
        
        
        '''# for i in half the ammount of planets, we create a planet on each side of the screen
        for i in range(int(cant/2)):
            x,y = randint(1,int(self.size[0]/2))-1, randint(0,self.size[1]-1)
            self.terrain[x][y] = Planet(2, x, y)
            x,y = randint(int(self.size[0]/2),self.size[0])-1, randint(0,self.size[1]-1)
            self.terrain[x][y] = Planet(2, x, y)'''

    
    def add_circle(self,plotter,radius,center=(0,0), char='#'):
        coordinates = plotter.get_circle(radius,center)
        for c in coordinates:
            self.terrain[c[0]][c[1]] = char

    def orbit(self):
        for x in range(len(self.terrain)):
            for y in range(len(self.terrain[0])):
                if self.terrain[x][y].search() == "Planet":
                    aux = self.terrain[x+1][y]
                    self.terrain[x+1][y] = self.terrain[x+1][y-1]
                    self.terrain[x+1][y-1] = self.terrain[x][y-1]
                    self.terrain[x][y-1] = self.terrain[x-1][y-1]
                    self.terrain[x-1][y-1] = self.terrain[x-1][y]
                    self.terrain[x-1][y] = self.terrain[x-1][y+1]
                    self.terrain[x-1][y+1] = self.terrain[x][y+1]
                    self.terrain[x][y+1] = self.terrain[x+1][y+1]
                    self.terrain[x+1][y+1] = aux


