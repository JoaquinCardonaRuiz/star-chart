from ships import Ship

class Building():
    def __init__(self):
        pass

#ORBITAL BUILDINGS

class OrbitalBuilding(Ship,Building):
    #Orbit-bound ships and infrastructure.
    #They sit on the 8 tiles surrounding a planet and rotate every turn
    pass

class OrbitalGun(OrbitalBuilding):
    #Orbit-bound ship with very high damage and range, which gets less accurate with distance
    pass

class MagneticCannon(OrbitalBuilding):
    #Orbit-bound building that accelerates ships to relativistic speeds 
    # and allows the transport of goods and people across the solar system
    pass 

class TerraformingSatellite(OrbitalBuilding):
    #Orbit-bound ship that provides tools for terraforming planets
    pass

#LAND BUILDINGS
class LandBuilding(Building):
    pass

