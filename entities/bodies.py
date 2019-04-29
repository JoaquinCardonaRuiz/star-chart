from utils import gen_height_map
from utils import identify
from entities.tile import Tile
from random import randint

class Empty:
    def __init__(self):
        self.identity = identify(self)
    
    def search(self):
        return(False)


class Star(Empty):
    def __init__(self, radius):
        Empty.__init__(self)
        self.radius = radius
        self.energy = radius*10
    
    def search(self):
        return "Star"


class Asteroid(Empty):
    def __init__(self, size):
        Empty.__init__(self)
        self.size = size
    
    def gen_shape():
        pass

    def search(self):
        return "Asteroid"


class Planet(Empty):
    """
    Size keys:
        1 -- Moon-sized, 10x10
        2 -- Small Planet, 25x25
        3 -- Medium Planet, 40x40
        4 -- Large Planet, 65x65
    """
    #TODO: move to config.ini
    sizes = {'1':60,'2':85,'3':100,'4':135}

    def __init__(self, size, planet_type = None):
        Empty.__init__(self)
        self.size = size
        self.type = planet_type
        if self.type == None:
            self.gen_type()
        self.terrain = self.gen_terrain()
        self.panx,self.pany = 0,0
        self.posx,self.posy = 0,0

    def gen_type(self):
        pass
    
    def gen_terrain(self):
        #TODO: calculate jump and alpha based on planet properties
        size = Planet.sizes[str(self.size)]
        jump = randint(4,10)/100
        alpha = 1+ randint(0,100)/100
        t = gen_height_map(size, 0.07, 1.5)
        terrain = [[Tile(height) for height in row] for row in t]
        return terrain

    def search(self):
        return "Planet"

class CapitalPlanet(Planet):
    def __init__(self, size, planet_type = None):
        Planet.__init__(self,size, planet_type)

    def search(self):
        return "Capital Planet"


class Marker(Empty):
    def __init__(self):
        Empty.__init__(self)
    
    def search(self):
        return "Marker"