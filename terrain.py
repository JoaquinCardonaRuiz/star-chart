from plot import Plot
from entities.bodies import *
from entities.ships import *
from random import randint
import configparser
from utils import dist,get_circle

class Terrain:
    """ Holds the state state of the StarChart board.

    Class variables:
        size    -- Width and height of the board, in tiles
        terrain -- Two-dimmensional array which holds the objects on the board
        config  -- Config file reader
        orbits  -- An array of integers which holds the radius of the orbits around the star
                   Planets are generated along these orbits

    """
    def __init__(self, star_radius,logger,config):
        self.size = (100,100)
        self.terrain = [[Empty() for i in range(self.size[1])] for j in range(self.size[0])]
        self.gen_star(star_radius)
        self.config = config
        self.orbits = []
        self.gen_planets(int(self.config['Constants']['CantPlanets']))
        self.spawn_tests()
        

    def spawn_tests(self):
        """Spawn test objects on the board."""

        #TODO: Create spawn(x,y,Object)
        self.terrain[60][40] = TestShip()
        self.terrain[0][0] = Marker()
        self.terrain[0][0] = Marker()
        self.terrain[0][0] = Marker()
        self.terrain[0][0] = Marker()


    def move(self,x1,y1,x2,y2):
        """Move object in terrain[x1][y1] to terrain[x2][y2]."""

        #TODO: Move logic to logic.py
        distance = dist(x1,y1,x2,y2)
        if self.terrain[x2][y2].search():
            pass
        elif self.terrain[x1][y1].search() and distance <= self.terrain[x1][y1].fuel:
            self.terrain[x2][y2] = self.terrain[x1][y1]
            self.terrain[x1][y1] = Empty()
            self.terrain[x2][y2].deplete(distance)
        

    def gen_star(self,star_radius):
        """Spawns star in the middle of the board."""

        middle = [int(self.size[0]/2),int(self.size[1]/2)]
        self.terrain[middle[0]][middle[1]] = Star(star_radius)


    def gen_planets(self, cant):
        """Spawns planets along the generated orbits.
        
        Selects a random point in an orbit and creates a planet there an in its polar oppposite
        """

        middle = [int(self.size[0]/2),int(self.size[1]/2)]
        while len(self.orbits) < cant:
            r = randint(6,int(self.size[0]/2))
            #If all the distances between orbits are greater than 4
            if all([(abs(r-c) > 4) for c in self.orbits]):
                self.orbits.append(r)
        self.orbits.sort()
        for d in self.orbits[:-1]:
            orbit_coords = get_circle(d)
            coord = orbit_coords[randint(0,len(orbit_coords) - 1)]
            self.terrain[middle[0] + coord[1]][middle[1] + coord[0]] = Planet(4)
            self.terrain[middle[0] - coord[1]][middle[1] - coord[0]] = Planet(4)
        
        self.terrain[middle[0]][middle[1]+self.orbits[-1]] = CapitalPlanet(4)
        self.terrain[middle[0]][middle[1]-self.orbits[-1]] = CapitalPlanet(4)


    def orbit(self):
        """Causes objects around a planet to orbit along the surounding tiles each turn.
        
        Not in use.
        """

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


