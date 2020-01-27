class Tile():

    #TODO: measure temp in Kelvin, add option to display units as C/F
    def __init__(self,height,minerals,humidity):
        self.char = ''
        self.height = height
        self.minerals = minerals
        self.humidity = humidity
    
    def search(self):
        return(False)

class Plain(Tile):
    def __init__(self):
        self.char = ''
        self.height = 0
        self.temperature = 0
    
    def search(self):
        return("Plain")

class Mountain(Tile):
    def __init__(self):
        self.char = ''
        self.height = 0
        self.temperature = 0
    
    def search(self):
        return("Mountain")