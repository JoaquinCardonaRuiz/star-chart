class Empty:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.char = ''
    
    def search(self):
        return(False)

class Star(Empty):
    def __init__(self, radius,x,y):
        Empty.__init__(self,x,y)
        self.radius = radius
        self.energy = radius*10
        self.char = '✹'
    
    def search(self):
        return "Star"

class Asteroid(Empty):
    def __init__(self, size):
        self.size = size
    
    def gen_shape():
        pass

    def search(self):
        return "Asteroid"

class Planet(Empty):
    def __init__(self, size, x, y, planet_type = None):
        Empty.__init__(self,x,y)
        self.size = size
        self.type = planet_type
        self.char = '⨁'
        if self.type == None:
            self.gen_type()

    def gen_type(self):
        pass
    
    def search(self):
        return "Planet"

class Marker(Empty):
    def __init__(self, x, y):
        Empty.__init__(self,x,y)
        self.char = "AA"
    
    def search(self):
        return "Marker"