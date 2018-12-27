from random import *
import math

def populate(freq):
    #Gets a value freq between 1 and 0, and returns True or False with probability of True equal to freq
    return(random() < freq)

def dist(x1,y1,x2,y2):
    #Gets two coordinates and returns the (truncated) distance between them
    return int(math.sqrt(pow((x2-x1),2)+pow((y2-y1),2)))

def get_circle(radius,fill = False,center=(0,0)):
        # Applies Midpoint circle algorithm
        radius += 1
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
            if fill:
                for i in range(-x,x):
                    for j in range(-y,y):
                        pixels.append((i,j))
                        pixels.append((j,i))
            else:
                pixels.append((x, y))
                pixels.append((-x, y))
                pixels.append((y, x))
                pixels.append((-y, x))
                pixels.append((-x, -y))
                pixels.append((-y, -x))
                pixels.append((+y, -x))
                pixels.append((x, -y))
        
            if (err <= 0):
                y += 1
                err += dy
                dy += 2

            if (err > 0):
                x -= 1
                dx += 2
                err += dx - (radius << 1)
        return pixels
