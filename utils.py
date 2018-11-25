from random import *
import math

def populate(freq):
    #Gets a value freq between 1 and 0, and returns True or False with probability = freq
    return(random() < freq)

def dist(x1,y1,x2,y2):
    #Gets two coordinates and returns the distance between them
    return math.sqrt(pow((x2-x1),2)+pow((y2-y1),2))