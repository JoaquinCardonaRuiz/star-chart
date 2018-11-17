import math
from log import Log 
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
            while (x >= y):
                # for every coordinate, we displace by radius to adjust to the (0,0) point being in the top left
                pixels.append((center[0] + x - int(radius), center[1] + y + int(radius)))
                pixels.append((center[0] + y - int(radius), center[1] + x + int(radius)))
                pixels.append((center[0] - y - int(radius), center[1] + x + int(radius)))
                pixels.append((center[0] - x - int(radius), center[1] + y + int(radius)))
                pixels.append((center[0] - x - int(radius), center[1] - y + int(radius)))
                pixels.append((center[0] - y - int(radius), center[1] - x + int(radius)))
                pixels.append((center[0] + y - int(radius), center[1] - x + int(radius)))
                pixels.append((center[0] + x - int(radius), center[1] - y + int(radius)))
            
                if (err <= 0):
                    y += 1
                    err += dy
                    dy += 2

                if (err > 0):
                    x -= 1
                    dx += 2
                    err += dx - (radius << 1)
            return pixels

    def plot_terrain(self,terrain):
        for y in terrain.terrain:
            for x in y:
                print(x+"   ",end='')
            print("\n")
        #print(terrain.terrain)
