from random import *
import math

def populate(freq):
    #Gets a value freq between 1 and 0, and returns True or False with probability = freq
    return(random() < freq)

def dist(x1,y1,x2,y2):
    #Gets two coordinates and returns the distance between them
    return math.sqrt(pow((x2-x1),2)+pow((y2-y1),2))

def get_circle(radius,center=(0,0)):
        # Applies Midpoint circle algorithm
        if radius < 6:
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
            pixels.append((x, y))
            pixels.append((y, x))
            pixels.append((-y, x))
            pixels.append((-x, y))
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
