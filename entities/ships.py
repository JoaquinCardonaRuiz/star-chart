from utils import identify

class Ship:
    def __init__(self, health, fuel):
        self.fuel = fuel
        self.health = health
        self.identity = identify(self)

    def search(self):
        return "Ship"

    
    def deplete(self,dist):
        self.fuel -= dist

class Fleet():
    def __init__(self, ships):
        self.ships = ships


class CapitalShip(Ship):
    #Main ship in fleet. Self-sustaining, capable of ship and colony production, heavily armoured
    pass

class Dreadnought(Ship):
    #Fast, moderately armoured and heavily armed
    pass

class Galley(Ship):
    #Transport vehicles for boarding and invading
    pass

class Bireme(Galley):
    #Galley with 120 capacity
    pass

class Trireme(Galley):
    #Galley with 180/200 capacity
    pass

class Quinquireme(Galley):
    #Galley with 420/450/500 capacity
    pass

class Galleas(Galley):
    #Galley with 800/1000 capacity
    pass

class Corvette(Ship):
    #A light and fast assault ship
    pass

class Cruiser(Ship):
    #Light and very fast exploration vessel
    pass

class Frigate(Ship):
    #Largest warship, slow, heavyly armed
    pass

class Destroyer(Ship):
    #Medium Size ship with high attack and low defence. Fast, but hp starts to drop if not escorting a Frigate
    pass

class Protector(Ship):
    #Very high defence, moderate attack, and very slow
    pass 

class SupplyShip(Ship):
    pass

class TestShip(Ship):
    #A cheap, customizable ship to test weapons on
    #░
    def __init__(self):
        Ship.__init__(self, 100, 50)
    