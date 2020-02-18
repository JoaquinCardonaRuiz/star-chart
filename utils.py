from random import *
import math
from noise import pnoise2
from noise import snoise2


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


def gen_height_map(size,jump,alpha):
    #jump shoud vary btw 0.04 and 0.8
    #alpha between 1 and 2
    #h = seed
    h = randint(0,100)+(randint(0,1000)/1000)
    t = []
    for i in range(size):
        r=[]
        for j in range(size):
            r.append(abs(pnoise2(h+i*jump,h+j*jump)) * alpha)
        t.append(r)
    return t


def get_sum_2d_matrix(matrix):
    s = 0
    for row in matrix:
        for item in row:
            s+=item
    return s


def identify(obj):
    #creates an identity array for an object, which contains its class,
    #superclass, and respective super-super-classes
    identity = []
    identity.append(obj.__class__)
    while True:
        try:
            identity.append(identity[-1].__bases__[0])
        except:
            return [i.__name__ for i in identity[:-1]]


def max2d(arr):
    return max(map(max,arr))

class Meta(type):
    #Metaclass that allows use of __repr__ for classes, instead of instances
    def __repr__(cls):
        return(cls.string_repr)