import math
from log import Log 
import curses
import configparser
import utils

class Plot:

    def __init__(self, logger, config):
        self.config = config
        self.panx = 0
        self.pany = 0
        logger.add('Plotter initialized')


    def pan_camera(self, direction):
        if direction == 's':
            self.pany += 1
        elif direction == 'w':
            self.pany -= 1
        elif direction == 'd':
            self.panx += 1
        elif direction == 'a':
            self.panx -= 1
        elif direction == 'o':
            self.zoom -= 0.05
        elif direction == 'p':
            self.zoom += 0.05

    def start(self):
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
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


    def draw_circ(self,x,y,radius,col):
        pass
        #pyxel.circ(x + int(pyxel.width/2) ,y + int(pyxel.height/2),radius,col)

    def draw(self, x, y, str, color, scr):
        try:
            scr.addstr(-self.pany + y, -self.panx + x*2,str,color)
        except curses.error as e:
            pass

    def draw_orbits(self,scr,terrain):
        middle = [int(terrain.size[0]/2),int(terrain.size[1]/2)]
        for r in terrain.orbits:
            to_add = utils.get_circle(r)
            for coord in to_add:
                x,y = middle[0]+coord[0],middle[1]+coord[1]
                self.draw(x, y, '.',233,scr)

    def plot_terrain(self, scr, terrain):
        #colors from 233 to 254
        for column in terrain.terrain:
            for point in column:
                color = 254
                #TODO use switch
                if point.search() == "Star":
                    str = "✹"
                elif point.search() == "Planet":
                    str = "⨁"
                elif point.search() == "Empty":
                    str = ""
                self.draw(point.x, point.y, str, color, scr)
        self.draw_orbits(scr,terrain)