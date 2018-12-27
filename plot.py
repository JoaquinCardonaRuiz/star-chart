import math
from log import Log 
import curses
import configparser
import utils
import time
from ui import UI
from random import randint

class Plot:

    def __init__(self, logger, config, terrain):
        self.x ,self.y, self.panx, self.pany, self.posx, self.posy = 0,0,0,0,0,0
        self.middle = [int(terrain.size[0]/2),int(terrain.size[1]/2)]
        self.terrain = terrain
        self.config = config
        self.uis = []
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
        elif direction == 'e' and self.posy > 0 and self.posx < self.terrain.size[0] - 1:
            self.posx += 1
            self.panx += 1.6
            self.posy -= 1
            self.pany -= 0.8

    def start(self,logger):
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
        curses.init_pair(5, curses.COLOR_BLACK, 7)
        scr.clear()
        self.y, self.x = scr.getmaxyx()
        self.y -= 1
        self.panx = self.terrain.size[0] - int(self.x /2)
        logger.add(str(self.x))
        self.posx = self.middle[0]
        self.posy = self.middle[1]
        self.pany = 18 + int(0.5 * ((self.terrain.size[1] - int(self.y *2)))) 
        return scr

    def draw_border(self,scr):
        for i in range(1,self.x-1):
            scr.addstr(0,i,self.config['Chars']['DHorizontal'])
            scr.addstr(self.y,i,self.config['Chars']['DHorizontal'])

        for j in range(1,self.y):
            scr.addstr(j,0,self.config['Chars']['DVertical'])
            scr.addstr(j,self.x-1,self.config['Chars']['DVertical'])

        scr.addstr(0,0,self.config['Chars']['DUpperLeft'])
        scr.addstr(0,self.x-1,self.config['Chars']['DUpperRight'])
        scr.addstr(self.y,0,self.config['Chars']['DLowerLeft'])

        #TODO: use draw method
        # https://stackoverflow.com/questions/36387625/curses-fails-when-calling-addch-on-the-bottom-right-corner
        try:
            scr.addstr(self.y,self.x-1,self.config['Chars']['DLowerRight'])
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

    def draw_orbits(self,scr):
        for r in self.terrain.orbits:
            to_add = utils.get_circle(r)
            for coord in to_add:
                x,y = self.middle[0]+coord[0],self.middle[1]+coord[1]
                self.draw(x, y, '.',4,scr)
                
    def draw_radius(self, ship, scr):
        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = self.posx + coord[0], self.posy + coord[1]
            #self.draw(x, y, '░',233,scr)
            self.draw(x, y, '.',2,scr)

    def draw_lock(self, ship, scr,cx,cy):

        #TODO: merge with draw_radius

        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = cx + coord[0], cy + coord[1]
            #self.draw(x, y, '░',233,scr)
            self.draw(x, y, '.',3,scr)
    
    def draw_pointer(self,scr):
        #self.draw(self.posx,self.posy, str(self.posx)+','+str(self.posy) ,5, scr)
        self.draw(self.posx,self.posy, '░',4, scr)

    
    def draw_UI(self,scr):
        test_ui = UI(["Ships", "Production","Resources"],"Left")
        test_ui_right = UI(["Colonies","Research","Pause"],"Right")
        test_ui_top = UI(["Map", "Info","Ship","Battle","Tech"],"Top")
        test_ui_bottom = UI(["Next Turn"],"Bottom")
        test_ui.draw(scr,self.x,self.y)
        test_ui_right.draw(scr,self.x,self.y)
        test_ui_top.draw(scr,self.x,self.y)
        test_ui_bottom.draw(scr,self.x,self.y)

    def plot_terrain(self, scr):
        #colors from 233 to 254
        self.draw_orbits(scr)
        self.draw_pointer(scr)
        current = self.terrain.terrain[self.posx][self.posy]
        if current.search() == "Ship":
            self.draw_radius(current,scr)
        for column in range(len(self.terrain.terrain)):
            for row in range(len(self.terrain.terrain[column])):
                point = self.terrain.terrain[column][row]
                if point.search():
                    color = 4
                    string = point.char
                    self.draw(column, row, string, color, scr)