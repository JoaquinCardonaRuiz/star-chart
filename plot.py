import math
from log import Log 
import curses
import configparser
import utils
import time
from random import randint
class Plot:

    def __init__(self, logger, config, terrain):
        self.middle = [int(terrain.size[0]/2),int(terrain.size[1]/2)]
        self.terrain = terrain
        self.config = config
        self.panx = terrain.size[0] - 75
        self.posx = self.middle[0]
        self.posy = self.middle[1]
        self.pany = 18 + int(0.5 * ((terrain.size[1] - 75))) 
        logger.add('Plotter initialized')


    def pan_camera(self, direction):
        if direction == 's' and self.posy < self.terrain.size[1]-1:
            self.posy += 1
            self.pany += 0.8
        elif direction == 'w' and self.posy > 0:
            self.posy -= 1
            self.pany -= 0.8
        elif direction == 'd' and self.posx < self.terrain.size[0] - 1:
            self.posx += 1
            self.panx += 1.6
        elif direction == 'a' and self.posx > 0:
            self.posx -= 1
            self.panx -= 1.6

    def start(self):
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        scr.keypad(True)
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_BLUE, -1)
        curses.init_pair(3, curses.COLOR_GREEN, -1)
        curses.init_pair(4, curses.COLOR_WHITE, -1)
        curses.init_pair(5, curses.COLOR_WHITE, -1)
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
            scr.addstr(-int(self.pany) + y, -int(self.panx) + x*2,str,curses.color_pair(color))
        except curses.error as e:
            pass

    def draw_ui(self, x, y, str, color, scr):
        try:
            scr.addstr(y+1, x*2 + 1,str,curses.color_pair(color))
        except curses.error as e:
            pass

    def draw_orbits(self,scr):
        for r in self.terrain.orbits:
            to_add = utils.get_circle(r)
            for coord in to_add:
                x,y = self.middle[0]+coord[0],self.middle[1]+coord[1]
                self.draw(x, y, '.',4,scr)
                
    def draw_radius(self, ship, scr):
        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = ship.x + coord[0], ship.y + coord[1]
            #self.draw(x, y, '░',233,scr)
            self.draw(x, y, '.',2,scr)
    
    def draw_pointer(self,scr):
        self.draw(self.posx,self.posy, str(self.posx)+','+str(self.posy) ,5, scr)
        

    def plot_terrain(self, scr):
        #colors from 233 to 254
        self.draw_orbits(scr)
        current = self.terrain.terrain[self.posx][self.posy]
        if current.search() == "Ship":
            self.draw_radius(current,scr)
        for column in self.terrain.terrain:
            for point in column:
                if point.search():
                    color = 5
                    string = point.char
                    self.draw(point.x, point.y, string, color, scr)
        self.draw_pointer(scr)
        self.draw_ui(0,0, str(int(self.panx))+','+str(int(self.pany)) ,5, scr)
