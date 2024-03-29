from entities.bodies import *
from entities.ships import *
from random import randint
from config import Config
from utils import dist,get_circle
from log import Log
import copy

class Board:
    """ Holds the state state of the StarChart board.

    Class variables:
        size    -- Width and height of the board, in tiles
        terrain -- Two-dimmensional array which holds the objects on the board
        orbits  -- An array of integers which holds the radius of the orbits around the star
                   Planets are generated along these orbits

    """

    #TODO: board should always be square, so make this an unique size, and adjust code below to match
    size = (100,100)
    terrain = []
    orbits = []
        
    @classmethod
    def start(cls,star_radius):
        cls.terrain = [[Empty() for i in range(cls.size[1])] for j in range(cls.size[0])]
        cls.gen_star(star_radius)
        cls.gen_planets(int(Config.config['Constants']['CantPlanets']))
        cls.spawn_tests()
        Log.add('Board initialized')
 
    @classmethod
    def spawn_tests(cls):
        """Spawn test objects on the board."""

        #TODO: Create spawn(x,y,Object)
        cls.terrain[20][20] = TestShip()
        for i in range(15):
            x,y = randint(0,cls.size[0]-1), randint(0,cls.size[1]-1)
            if not cls.terrain[x][y].search():
                cls.terrain[x][y] = Asteroid(2)


    @classmethod
    def move(cls,x1,y1,x2,y2):
        """Move object in terrain[x1][y1] to terrain[x2][y2]."""
        
        #TODO: Move logic to logic.py
        distance = dist(x1,y1,x2,y2)
        if cls.terrain[x2][y2].search():
            Log.add("Ship movement failed, obstacle detected.")
            pass
        elif distance <= cls.terrain[x1][y1].fuel:
            Log.add("Moving ship from (" + str(x1) + ","+str(y1) +") to ("+ str(x2) + ","+str(y2)+")")
            cls.terrain[x2][y2] = cls.terrain[x1][y1]
            cls.terrain[x1][y1] = Empty()
            cls.terrain[x2][y2].deplete(distance)
        
    @classmethod
    def gen_star(cls,star_radius):
        """Spawns star in the middle of the board."""

        middle = [int(cls.size[0]/2),int(cls.size[1]/2)]
        cls.terrain[middle[0]][middle[1]] = Star(star_radius)

    @classmethod
    def gen_planets(cls, cant):
        """Spawns planets along the generated orbits.
        
        Selects a random point in an orbit and creates a planet there an in its polar oppposite
        """

        middle = [int(cls.size[0]/2),int(cls.size[1]/2)]
        cont = 0
        while len(cls.orbits) < cant:
            cont+=1
            r = randint(6,int(cls.size[0]/2)-1)
            #If all the distances between orbits are greater than 4
            if all([(abs(r-c) > 4) for c in cls.orbits]):
                cls.orbits.append(r)
            if cont > 50:
                raise Exception("Can't place orbits")
        cls.orbits.sort()
        for d in cls.orbits[:-1]:
            orbit_coords = get_circle(d)
            coord = orbit_coords[randint(0,len(orbit_coords) - 1)]
            #TODO: Don't randomize planet sizes
            #Solar distance is orbit_radius/(board_size/2) => 1 for capital planet, 0.5 for planet on the middle
            planet = Planet(randint(1,4),d/middle[0])
            cls.terrain[middle[0] + coord[1]][middle[1] + coord[0]] = copy.deepcopy(planet)
            cls.terrain[middle[0] - coord[1]][middle[1] - coord[0]] = copy.deepcopy(planet)
        
        try:
            planet = CapitalPlanet(4,cls.orbits[-1]/middle[0])
            cls.terrain[middle[0]][middle[1]+cls.orbits[-1]] = copy.deepcopy(planet)
            cls.terrain[middle[0]][middle[1]-cls.orbits[-1]] = copy.deepcopy(planet)
        except:
            raise

    @classmethod
    def orbit(cls):
        """Causes objects around a planet to orbit along the surounding tiles each turn.
        
        Not in use.
        """

        for x in range(len(cls.terrain)):
            for y in range(len(cls.terrain[0])):
                if cls.terrain[x][y].search() == "Planet":
                    aux = cls.terrain[x+1][y]
                    cls.terrain[x+1][y] = cls.terrain[x+1][y-1]
                    cls.terrain[x+1][y-1] = cls.terrain[x][y-1]
                    cls.terrain[x][y-1] = cls.terrain[x-1][y-1]
                    cls.terrain[x-1][y-1] = cls.terrain[x-1][y]
                    cls.terrain[x-1][y] = cls.terrain[x-1][y+1]
                    cls.terrain[x-1][y+1] = cls.terrain[x][y+1]
                    cls.terrain[x][y+1] = cls.terrain[x+1][y+1]
                    cls.terrain[x+1][y+1] = aux