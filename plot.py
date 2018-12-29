import math
from log import Log 
import curses
import configparser
import utils
import time
from ui import Panel
from random import randint

class Plot:
    """Graphics module for StarChart. Handles drawing all elements.
    
    Class variables:
        x,y         -- Screen width and height
        posx, posy  -- Cursor coordinates on the board (0,0 in upper-left corner)
        panx, pany  -- Camera displacement from center 
        middle      -- Coordinates of the center of the board
        terrain     -- Instance of terrain class (terrain.py), which holds board state
        config      -- Config file reader
        uis         -- Array of user interface elements
    """

    def __init__(self, logger, config, terrain):

        #TODO: Don't keep middle as an instance variable
        #TODO: Reestructure UI elements' storage
        #TODO: Create dict with ui elements {'right': UI(blah,right), 'bottom': UI(blah, bottom...)}
        self.x ,self.y, self.panx, self.pany, self.posx, self.posy = 0,0,0,0,0,0
        self.middle = [int(terrain.size[0]/2),int(terrain.size[1]/2)]
        self.terrain = terrain
        self.config = config
        self.uis = []
        logger.add('Plotter initialized')


    def pan_camera(self, direction):
        """Takes a direction in the form of a character and moves cursor and camera appropriately."""

        #TODO: Rename method. It moves the cursor as well as panning the camera
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
        """Initializes graphics engine, and returns an instance of the curses Screen class.
        
        Sets starting positions for cursor and camera, initializes color profiles and terminal settigs.
        """

        #TODO: have scr be saved in plotter, instead of returning it
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
        """Draws the border that surrounds the screen."""

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
        """Terminates graphics engine cleanly"""

        curses.nocbreak()
        scr.keypad(False)
        curses.echo()
        curses.endwin()


    def draw(self, x, y, str, color, scr):
        """Draws a string or character on the screen.
        
        Keyword Arguments:
            x,y     -- Coordinates where first character will be drawn
            str     -- String or character to draw
            color   -- Color profile to use
            scr     -- Instance of the Curses Screen object. The screen to draw on
        """

        #TODO: don't get scr as an argument, move scr to plotter
        try:
            scr.addstr(-int(self.pany) + y, -int(self.panx) + x*2,str,curses.color_pair(color))
        except curses.error as e:
            pass


    def draw_orbits(self,scr):
        """ Draws the orbits stored in the Terrain instance around the star."""

        #TODO: use character from config file
        #TODO: don't get scr as an argument, move scr to plotter
        for r in self.terrain.orbits:
            to_add = utils.get_circle(r)
            for coord in to_add:
                x,y = self.middle[0]+coord[0],self.middle[1]+coord[1]
                self.draw(x, y, '.',4,scr)
                

    def draw_radius(self, ship, scr):
        """ Draws a circle around a ship indicating where it can move.
        
        Gets called when cursor is on top of ship. Calculates radius from ship's fuel.
        """
        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = self.posx + coord[0], self.posy + coord[1]
            #self.draw(x, y, '░',233,scr)
            self.draw(x, y, '.',2,scr)

    def draw_lock(self, ship, scr,cx,cy):
        """ Draws a circle around a ship indicating where it can move when locked onto.
        
        Gets called when cursor is locked on ship. Calculates radius from ship's fuel.
        """

        #TODO: merge with draw_radius
        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = cx + coord[0], cy + coord[1]
            #self.draw(x, y, '░',233,scr)
            self.draw(x, y, '.',3,scr)
    
    def draw_pointer(self,scr):
        """Draws cursor on screen."""

        #TODO: use different char for cursor when moving ship
        #TODO: rename to draw_cursor ?
        #TODO: read char from config file
        self.draw(self.posx,self.posy, '░',4, scr)

    
    def draw_UI(self,scr):
        """Draws UI menus.
        
        Currently only draws placeholders.
        """

        #TODO: Reestructure UI elements' storage
        test_ui = Panel(["Ships", "Production","Resources"],"Left")
        test_ui_right = Panel(["Colonies","Research","Pause"],"Right")
        test_ui_top = Panel(["Map", "Info","Ship","Battle","Tech"],"Top")
        test_ui_bottom = Panel(["Next Turn"],"Bottom")
        test_ui.draw(scr,self.x,self.y)
        test_ui_right.draw(scr,self.x,self.y)
        test_ui_top.draw(scr,self.x,self.y)
        test_ui_bottom.draw(scr,self.x,self.y)

    def plot_terrain(self, scr):
        """Draws the state of the board, along with the orbit, pointers and ship's movement radius."""
        
        #TODO: rename to draw_state and create a new plot_terrain to handle the board
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
        #self.terrain.orbit()