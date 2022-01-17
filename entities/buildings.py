from entities.ships import Ship


class Building():
    name = 'Generic Building'
    snippet = 'Building for testing'
    symbol = '▣'
    mineral_cost = 0

    def __init__(self):
        pass

    @classmethod
    def item_repr(cls):
        '''ᐁ∇▾♦⟠⧫ᚖṀṁṂṃ₩₦'''
        return [cls.symbol + ' ' + cls.name,
                cls.snippet,
                '⟠ '+str(cls.mineral_cost)]

#ORBITAL BUILDINGS

class OrbitalBuilding(Ship,Building):
    # Orbit-bound ships and infrastructure.
    # They sit on the 8 tiles surrounding a planet and rotate every turn
    pass

class OrbitalGun(OrbitalBuilding):
    # Orbit-bound ship with very high damage and range, which gets less accurate with distance
    name = 'Orbital Gun'
    snippet = 'Building for testing'
    symbol = '◬'
    mineral_cost = 1800

class MagneticCannon(OrbitalBuilding):
    # Orbit-bound building that accelerates ships to relativistic speeds 
    # and allows the transport of goods and people across the solar system
    name = 'Magnetic Cannon'
    snippet = 'Building for testing'
    symbol = '▣'
    mineral_cost = 2200

class TerraformingSatellite(OrbitalBuilding):
    # Orbit-bound ship that provides tools for terraforming planets
    name = 'Terraforming Satellite'
    snippet = 'Building for testing'
    symbol = '▣'
    mineral_cost = 3800

#LAND BUILDINGS
class LandBuilding(Building):
    pass

class Rail(LandBuilding):
    #╩╦╩╦╩╦╩╦╩╦╩╦╩╦╩╦╩╦╩╦╩
    name = 'Rail Line'
    snippet = 'Building for testing'
    symbol = '╩╦'
    mineral_cost = 10

class Dome(LandBuilding):
    name = 'Dome'
    snippet = 'Building for testing'
    symbol = '◚'
    mineral_cost = 200

class LaunchPad(LandBuilding):
    name = 'Launch Pad'
    snippet = 'Building for testing'
    symbol = '◎'
    mineral_cost = 150

buildings = [OrbitalGun, MagneticCannon, TerraformingSatellite, Rail, Dome, LaunchPad]