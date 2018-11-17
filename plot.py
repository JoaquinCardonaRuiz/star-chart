import math
from log import Log 
import pyxel
class Plot:

    def __init__(self, logger):
        self.logger = logger

    def get_circle(self,radius,center=(0,0)):
            # Applies Midpoint circle algorithm
            if radius < 6:
                self.logger.add("Plot error: Radius can't be smaller than 6")
                return []

            pixels = []
            x = radius-1
            y = 0
            dx = 1
            dy = 1
            err = dx - (radius<<1) # https://www.geeksforgeeks.org/left-shift-right-shift-operators-c-cpp/
            center = list(center)
            center[0] -= radius
            center[1] += radius
            while (x >= y):
                pixels.append((center[0] + x, center[1] + y))
                pixels.append((center[0] + y, center[1] + x))
                pixels.append((center[0] - y, center[1] + x))
                pixels.append((center[0] - x, center[1] + y))
                pixels.append((center[0] - x, center[1] - y))
                pixels.append((center[0] - y, center[1] - x))
                pixels.append((center[0] + y, center[1] - x))
                pixels.append((center[0] + x, center[1] - y))
            
                if (err <= 0):
                    y += 1
                    err += dy
                    dy += 2

                if (err > 0):
                    x -= 1
                    dx += 2
                    err += dx - (radius << 1)
            return pixels

    def draw_circ(self,x,y,radius,col):
        pyxel.circ(x + int(pyxel.width/2) ,y + int(pyxel.height/2),radius,col)

    def plot_terrain(self, terrain):
        for row in terrain.terrain:
            for point in row:
                if point.search() == "Star":
                    self.draw_circ(0,0,point.radius,1)