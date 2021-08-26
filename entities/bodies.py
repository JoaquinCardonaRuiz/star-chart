import utils
from random import random, randint, normalvariate
import math
from entities.tile import Tile
from log import Log
from config import Config


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

    # Read sizes from config.ini
    sizes = {}
    for key in Config.config['Sizes']:
        sizes[key] = int(Config.config['Sizes'][key])

    def __init__(self, size, solar_distance, planet_type = None):
        Empty.__init__(self)
        self.size = size
        self.type = planet_type
        self.solar_distance = solar_distance
        #Depends on solar_distance
        self.avg_temperature = self.get_avgtemp() 

        self.oxygen_richness = round((random()*55 + 5)/100,2)
        self.mineral_richness = self.get_mineral_richness()
        self.water_richness = self.get_water_richness()
        self.characteristics = self.get_chars()
        if self.type == None:
            self.gen_type()
        self.terrain = self.gen_terrain()
        self.panx,self.pany = 0,0
        self.posx,self.posy = 0,0


    def get_chars(self):
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
        chars = {"Size":                {"value": self.size,                "key": ''},
                 "Type":                {"value": self.type,                "key": ''},
                 "Solar Distance":      {"value": self.solar_distance,      "key": ''},
                 "Average Temperature": {"value": self.avg_temperature,     "key": ''},
                 "Oxygen Richness":     {"value": self.oxygen_richness,     "key": ''},
                 "Mineral Richness":    {"value": self.mineral_richness,    "key": ''},
                 "Water Richness":      {"value": self.water_richness,      "key": ''},
                 "Oxygen Richness":     {"value": self.oxygen_richness,     "key": ''},
                 "Hospitability":       {"value": 0,              "key": 'Out of 3.0'}}

        chars['Hospitability']['value'] = 0

        if self.avg_temperature > 433:
            chars['Average Temperature']['key'] = "Molten"
        elif self.avg_temperature > 368:
            chars['Average Temperature']['key'] = "Scorching"
        elif self.avg_temperature > 318:
            chars['Average Temperature']['key'] = "Hot"
            chars['Hospitability']['value'] += 0.75
        elif self.avg_temperature > 253:
            chars['Average Temperature']['key'] = "Temperate"
            chars['Hospitability']['value'] += 1
        elif self.avg_temperature > 213:
            chars['Average Temperature']['key'] = "Cold"
            chars['Hospitability']['value'] += 0.75
        elif self.avg_temperature > 123:
            chars['Average Temperature']['key'] = "Gelid"
            chars['Hospitability']['value'] += 0.25
        else:
            chars['Average Temperature']['key'] = "Frozen"

        #TODO: revise oxygen livable proportions

        if self.oxygen_richness > 0.45:
            chars['Oxygen Richness']['key'] = "Oxygen excess"
            chars['Hospitability']['value'] += 0.4
        elif self.oxygen_richness > 0.32:
            chars['Oxygen Richness']['key'] = "Oxygen abundant"
            chars['Hospitability']['value'] += 0.7
        elif self.oxygen_richness > 0.14:
            chars['Oxygen Richness']['key'] = "Oxygen moderate"
            chars['Hospitability']['value'] += 1
        elif self.oxygen_richness  > 0.08:
            chars['Oxygen Richness']['key'] = "Oxygen sparce"
        else:
            chars['Oxygen Richness']['key'] = "Oxygen poor"

        if self.mineral_richness > 0.75:
            chars['Mineral Richness']['key'] = "Mineral richness"
        elif self.mineral_richness > 0.5:
            chars['Mineral Richness']['key'] = "Mineral abundant"
        elif self.mineral_richness > 0.25:
            chars['Mineral Richness']['key'] = "Mineral moderate"
        elif self.mineral_richness  > 0.08:
            chars['Mineral Richness']['key'] = "Mineral sparce"
        else:
            chars['Mineral Richness']['key'] = "Mineral poor"

        if self.water_richness > 0.9:
            chars['Water Richness']['key'] = "Flooded"
            chars['Hospitability']['value'] += 0.75
        elif self.water_richness > 0.75:
            chars['Water Richness']['key'] = "Water excess"
            chars['Hospitability']['value'] += 1
        elif self.water_richness > 0.45:
            chars['Water Richness']['key'] = "Water abundant"
            chars['Hospitability']['value'] += 1
        elif self.water_richness > 0.2:
            chars['Water Richness']['key'] = "Water moderate"
            chars['Hospitability']['value'] += 1
        elif self.water_richness  > 0.1:
            chars['Water Richness']['key'] = "Water sparce"
            chars['Hospitability']['value'] += 0.75
        else:
            chars['Water Richness']['key'] = "Water poor"

        return chars


    def get_avgtemp(self):
        #TODO: add randomness again
        #TODO: make sure it never goes below 0
        if self.solar_distance<0.2:
            return round(-100*self.solar_distance+438.651,2)
        elif self.solar_distance>0.75:
            return round(-100*self.solar_distance+155.621,2)
        else:
            return round(math.pow(9.1-20*self.solar_distance,3)+286,2)


    def get_mineral_richness(self):
        #TODO: make sure it never goes negative
        return round((10/(1+math.pow((math.e),(5-2.8*(1-self.solar_distance))))) + (random()*0.2 - 0.1),2)


    def get_water_richness(self):
        #TODO: add randomness again
        #TODO: make sure it never goes below 0 or above 1
        if self.solar_distance<0.225:
            return round(0.3*self.solar_distance+0.0315, 2)
        elif self.solar_distance>0.7:
            return round(self.solar_distance-0.01, 2)
        else:
            return round(math.pow(2.8*self.solar_distance-1.3,3)+0.4, 2)


    def gen_type(self):
        pass
    

    def gen_terrain(self):
        #TODO: calculate jump and alpha based on planet properties
        size = Planet.sizes[str(self.size)]

        # Jump determines how closely the perlin noise is sampled,
        # and therefore, how small or large mountains and valleys are.
        # It's a normal distribution whose mean varies according to
        # solar distance. The farther from the sun the planet is,
        # the larger mountains and valleys, so the easier it is for
        # starting players.
        jump = normalvariate(0.07-((self.solar_distance * 2 - 1) * 0.02),0.014)
        heights = utils.gen_height_map(size, jump)
        minerals = self.get_minerals(heights)
        humidities = [[round((1 - i)*self.water_richness,2) for i in j] for j in heights]
        
        #how many layers of abstraction are u on?
        terrain = [[Tile(height=tile[0],minerals=tile[1],humidity=tile[2]) for tile in row] for row in [list(zip(heights[i],minerals[i],humidities[i])) for i in range(len(heights))]]
        return terrain
    

    def get_minerals(self,heights):
        """Determines mineral content in tiles"""
        #The algorithm searches for points with a height near the maximum. If there are enough, it puts the mineral centers there
        #If not, it widens the heights its willing to consider and checks again

        # Distance from the maximum in which to deposit mineral centers. Mineral centers will only be deposited
        # In points which are between height max_val and max_val - min_dif
        min_dif = 0.02

        # Maximum height in the whole map
        max_val = utils.max2d(heights)

        # We gather every point between max val and max_val - min_dif
        max_coords = [(ix,iy) for ix, row in enumerate(heights) for iy, i in enumerate(row) if abs(i-max_val)<min_dif]

        # We remove repeated points or points too close to each other
        for cx in max_coords:
            for cy in max_coords:
                if cx != cy and utils.dist(cx[0],cx[1],cy[0],cy[1]) < 10:
                    max_coords.remove(cy)

        # If there are 10 or more adequate points, we place the centers.
        # Otherwise, we add 0.01 to min_dif to widen the search, and repeat.
        while len(max_coords) < 10:
            # TODO: encapsulate this sequence in a sub-method
            min_dif += 0.01
            max_coords = [(ix,iy) for ix, row in enumerate(heights) for iy, i in enumerate(row) if abs(i-max_val)<min_dif]
            for cx in max_coords:
                for cy in max_coords:
                    if cx != cy and utils.dist(cx[0],cx[1],cy[0],cy[1]) < 10:
                        max_coords.remove(cy)


        minerals = [[0 for i in j] for j in heights]
        for c in max_coords:
            #for i in range(1,6)[::-1]:
            for i in range(6,7):
                coords = utils.get_circle(i,True)
                for j in coords:
                    # We just ignore out of index errors if a circle
                    # extends beyond the map of the planet
                    try:
                        minerals[j[0]+c[0]][j[1]+c[1]] += 800
                    except:
                        pass
        return minerals

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