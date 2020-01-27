import utils
from random import random
import math
from entities.tile import Tile
from random import randint
from log import Log

class Empty:
    def __init__(self):
        self.identity = utils.identify(self)
    
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

    def __init__(self, size, solar_distance, planet_type = None):
        #TODO: make sure opposite planets have the same stats

        Empty.__init__(self)
        self.size = size
        self.type = planet_type
        self.solar_distance = solar_distance
        #Depends on solar_distance
        self.avg_temperature = self.get_avgtemp() 

        self.oxygen_richness = (random()*55 + 5)/100
        self.mineral_richness = self.get_mineral_richness()
        self.water_richness = self.get_water_richness()
        #Habitable if oxygen around 21%, water above 10%, and avg temperature around 283K
        self.characteristics = self.get_chars()
        if self.type == None:
            self.gen_type()
        self.terrain = self.gen_terrain()
        self.panx,self.pany = 0,0
        self.posx,self.posy = 0,0
        Log.add(self.characteristics)


    def get_chars(self):
        #TODO: simplify this mess
        """
        Temperature keys:               Oxygen keys:                    Mineral keys:                   Water keys:
            < 123     -- Frozen             < 8%      -- Poor               < 8%       -- Poor              < 10%       -- Poor
            123 - 213 -- Gelid              8%  - 14% -- Sparce             8%  - 25%  -- Sparce            10%  - 20%  -- Sparce
            213 - 253 -- Cold               14% - 35% -- Moderate           25% - 50%  -- Moderate          20% - 45%   -- Moderate
            253 - 318 -- Temperate          35% - 50% -- Abundant           50% - 75%  -- Abundant          45% - 75%   -- Abundant
            318 - 368 -- Hot                50% - 60% -- Excesive           75% - 100% -- Rich              75% - 90%   -- Excessive
            368 - 433 -- Scorching                                                                          90% - 100%  -- Flooded
            > 433     -- Molten
        """
        chars = []
        hospitability_points = 0

        if self.avg_temperature > 433:
            chars.append("Molten")
        elif self.avg_temperature > 368:
            chars.append("Scorching")
        elif self.avg_temperature > 318:
            chars.append("Hot")
            hospitability_points += 0.75
        elif self.avg_temperature > 253:
            chars.append("Temperate")
            hospitability_points += 1
        elif self.avg_temperature > 213:
            chars.append("Cold")
            hospitability_points += 0.75
        elif self.avg_temperature > 123:
            chars.append("Gelid")
            hospitability_points += 0.25
        else:
            chars.append("Frozen")

        #TODO: revise oxygen livable proportions

        if self.oxygen_richness > 0.45:
            chars.append("Oxygen excess")
            hospitability_points += 0.4
        elif self.oxygen_richness > 0.32:
            chars.append("Oxygen abundant")
            hospitability_points += 0.7
        elif self.oxygen_richness > 0.14:
            chars.append("Oxygen moderate")
            hospitability_points += 1
        elif self.oxygen_richness  > 0.08:
            chars.append("Oxygen sparce")
        else:
            chars.append("Oxygen poor")

        if self.mineral_richness > 0.75:
            chars.append("Mineral richness")
        elif self.mineral_richness > 0.5:
            chars.append("Mineral abundant")
        elif self.mineral_richness > 0.25:
            chars.append("Mineral moderate")
        elif self.mineral_richness  > 0.08:
            chars.append("Mineral sparce")
        else:
            chars.append("Mineral poor")

        if self.water_richness > 0.9:
            chars.append("Flooded")
            hospitability_points += 0.75
        elif self.water_richness > 0.75:
            chars.append("Water excess")
            hospitability_points += 1
        elif self.water_richness > 0.45:
            chars.append("Water abundant")
            hospitability_points += 1
        elif self.water_richness > 0.2:
            chars.append("Water moderate")
            hospitability_points += 1
        elif self.water_richness  > 0.1:
            chars.append("Water sparce")
            hospitability_points += 0.75
        else:
            chars.append("Water poor")


        chars.append("Habitability " + str(hospitability_points) + "/3")
        return chars

    def get_avgtemp(self):
        #TODO: add randomness again
        #TODO: make sure it never goes below 0
        if self.solar_distance<0.2:
            return -100*self.solar_distance+438.651
        elif self.solar_distance>0.75:
            return -100*self.solar_distance+155.621
        else:
            return math.pow(9.1-20*self.solar_distance,3)+286


    def get_mineral_richness(self):
        #TODO: make sure it never goes negative
        return (10/(1+math.pow((math.e),(5-2.8*(1-self.solar_distance))))) + (random()*0.2 - 0.1)

    def get_water_richness(self):
        #TODO: add randomness again
        #TODO: make sure it never goes below 0 or above 1
        if self.solar_distance<0.225:
            return 0.3*self.solar_distance+0.0315
        elif self.solar_distance>0.7:
            return self.solar_distance-0.01
        else:
            return math.pow(2.8*self.solar_distance-1.3,3)+0.4

    def gen_type(self):
        pass
    
    def gen_terrain(self):
        #TODO: calculate jump and alpha based on planet properties
        size = Planet.sizes[str(self.size)]
        jump = randint(4,10)/100
        alpha = 1+ randint(0,100)/100
        heights = utils.gen_height_map(size, jump, alpha)
        #avg mineral content = richness * 500
        #avg height * modifier = richness * 500
        #richness * 500 / avg height = modifier
        #(richness * 500) / (sum(height) / size^2) = modifier
        modifier = (self.mineral_richness * 2500000) / (utils.get_sum_2d_matrix(heights) / math.pow(self.size,2))
        minerals = [[i*modifier for i in j] for j in heights]
        humidities = [[(1/(i+0.01)) for i in j] for j in heights]
        
        #how many layers of abstraction are u on?
        terrain = [[Tile(height=tile[0],minerals=tile[1],humidity=tile[2]) for tile in row] for row in [list(zip(heights[i],minerals[i],humidities[i])) for i in range(len(heights))]]
        return terrain

    def search(self):
        return "Planet"

class CapitalPlanet(Planet):
    def __init__(self, size, solar_distance,planet_type = None):
        Planet.__init__(self,size,solar_distance, planet_type)

    def search(self):
        return "Capital Planet"


class Marker(Empty):
    def __init__(self):
        Empty.__init__(self)
    
    def search(self):
        return "Marker"