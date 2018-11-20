class Star:
    def __init__(self, radius):
        self.radius = radius
        self.energy = radius*10
    
    def search(self):
        return "Star"

class Asteroid:
    def __init__(self, size):
        self size = size
    
    def gen_shape:
        pass

    def search(self):
        return "Asteroid"

class Planet:
    def __init__(self, size,  planet_type = None):
        self.size = size
        self.type = planet_type
        if self.type = None:
            self.gen_type

    def gen_type(self):
        pass
    
    def search(self):
        return "Planet"