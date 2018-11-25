import math
from log import Log 
import curses
import configparser

class Plot:

    def __init__(self, logger, config):
        self.config = config
        logger.add('Plotter initialized')


    def start(self):
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        scr.keypad(True)
        scr.clear()
        return scr

    def draw_border(self,scr,x,y):
        for i in range(1,x-1):
            scr.addstr(0,i,self.config['Chars']['DHorizontal'])
            scr.addstr(y-1,i,self.config['Chars']['DHorizontal'])

        for j in range(1,y-1):
            scr.addstr(j,0,self.config['Chars']['DVertical'])
            scr.addstr(j,x-1,self.config['Chars']['DVertical'])

        scr.addstr(0,0,self.config['Chars']['DUpperLeft'])
        scr.addstr(0,x-1,self.config['Chars']['DUpperRight'])
        scr.addstr(y-1,0,self.config['Chars']['DLowerLeft'])
        # https://stackoverflow.com/questions/36387625/curses-fails-when-calling-addch-on-the-bottom-right-corner
        try:
            scr.addstr(y-1,x-1,self.config['Chars']['DLowerRight'])
        except curses.error as e:
            pass

        
    def end(self,scr):
        curses.nocbreak()
        scr.keypad(False)
        curses.echo()
        curses.endwin()




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
        pass
        #pyxel.circ(x + int(pyxel.width/2) ,y + int(pyxel.height/2),radius,col)

    def draw(self, x, y, str, scr):
        try:
            scr.addstr(y,x*2,str)
        except curses.error as e:
            pass

    def plot_terrain(self, scr, terrain):
        for column in terrain.terrain:
            for point in column:
                #use switch
                if point.search() == "Star":
                    str = "()"
                elif point.search() == "Planet":
                    str = "[]"
                elif point.search() == "Empty":
                    str = "  "
                self.draw(point.x, point.y, str, scr)