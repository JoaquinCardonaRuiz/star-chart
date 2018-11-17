class Star:
    def __init__(self, radius):
        self.radius = radius
        self.energy = radius*10
    
    def search(self):
        return "Star"