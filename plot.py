import math
from log import Log 
import curses
import utils
import time
from ui import Panel, Window, Static_Window, Floating_Window
from terrain import Terrain
from random import randint
from config import Config
from entities.bodies import Planet


class Plot:
    """Graphics module for StarChart. Handles drawing all elements.
    
    Class variables:
        x,y         -- Screen width and height
        posx, posy  -- Cursor coordinates on the board (0,0 in upper-left corner)
        panx, pany  -- Camera displacement from center 
        uis         -- Array of user interface elements
    """

    x,y = 0,0
    panx,pany = 0,0
    posx,posy = 0,0
    uis = {'right': None, 'bottom': None, 'left': None, 'top': None, 'static': None}
    scr = None

    @classmethod
    def pan_camera(cls, direction):
        """Takes a direction in the form of a character and moves cursor and camera appropriately."""

        #TODO: Rename method. It moves the cursor as well as panning the camera
        y,x = cls.get_screen_coords(cls.posx, cls.posy)
        if direction == 's' and cls.posy < Terrain.size[1]-1:
            cls.posy += 1
            if (y >= cls.y*0.8):
                cls.pany += 1
        elif direction == 'w' and cls.posy > 0:
            cls.posy -= 1
            if (y <= cls.y*0.2):
                cls.pany -= 1
        elif direction == 'd' and cls.posx < Terrain.size[0] - 1:
            cls.posx += 1
            if (x >= cls.x*0.8):
                cls.panx += 2
        elif direction == 'a' and cls.posx > 0:
            cls.posx -= 1
            if (x <= cls.x*0.2):
                cls.panx -= 2


    @classmethod
    def pan_terrain_camera(cls, direction, planet):
        #TODO simplify panning ifs
        cls.scr.addstr(1, 1, str(planet.panx)+ ", "+str(planet.pany), curses.color_pair(4))
        if direction == 's' and planet.posy + 1 < Planet.sizes[str(planet.size)] - 1:
            planet.posy += 1
            if (planet.posy - planet.pany >= 0.8 * cls.uis["static"].get_size(cls.scr)[1]):
                planet.pany += 1
        elif direction == 'w' and planet.posy > 0:
            planet.posy -= 1
            if (planet.posy - planet.pany <= 0.2 * cls.uis["static"].get_size(cls.scr)[1]):
                planet.pany -= 1
        elif direction == 'd' and planet.posx < Planet.sizes[str(planet.size)] - 1:
            planet.posx += 1
            if (planet.posx * 2 - planet.panx*2 >= 0.8 * cls.uis["static"].get_size(cls.scr)[0]):
                planet.panx += 1
        elif direction == 'a' and planet.posx > 0:
            planet.posx -= 1
            if (planet.posx * 2 - planet.panx*2 <= 0.2 * cls.uis["static"].get_size(cls.scr)[0]):
                planet.panx -= 1


    @classmethod
    def start(cls):
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
        cls.y, cls.x = scr.getmaxyx()
        cls.y -= 1
        cls.panx = Terrain.size[0] - int(cls.x /2)
        Log.add(str(cls.x))
        middle = [i//2 for i in Terrain.size]
        cls.posx = middle[0]
        cls.posy = middle[1]
        cls.pany = 18 + int(0.5 * ((Terrain.size[1] - int(cls.y *2)))) 
        cls.scr = scr
        Log.add('Plotter initialized')


    @classmethod
    def draw_border(cls):
        """Draws the border that surrounds the screen."""

        for i in range(1,cls.x-1):
            cls.scr.addstr(0,i,Config.config['Chars']['DHorizontal'])
            cls.scr.addstr(cls.y,i,Config.config['Chars']['DHorizontal'])

        for j in range(1,cls.y):
            cls.scr.addstr(j,0,Config.config['Chars']['DVertical'])
            cls.scr.addstr(j,cls.x-1,Config.config['Chars']['DVertical'])

        cls.scr.addstr(0,0,Config.config['Chars']['DUpperLeft'])
        cls.scr.addstr(0,cls.x-1,Config.config['Chars']['DUpperRight'])
        cls.scr.addstr(cls.y,0,Config.config['Chars']['DLowerLeft'])

        #TODO: use draw method
        # https://stackoverflow.com/questions/36387625/curses-fails-when-calling-addch-on-the-bottom-right-corner
        try:
            cls.scr.addstr(cls.y,cls.x-1,Config.config['Chars']['DLowerRight'])
        except curses.error as e:
            pass

    @classmethod
    def end(cls):
        """Terminates graphics engine cleanly"""

        curses.nocbreak()
        cls.scr.keypad(False)
        curses.echo()
        curses.endwin()

    @classmethod
    def draw(cls, x, y, str, color):
        """Draws a string or character on the screen.
        
        Keyword Arguments:
            x,y     -- Coordinates where first character will be drawn
            str     -- String or character to draw
            color   -- Color profile to use
        """

        #TODO: don't get scr as an argument, move scr to plotter
        try:
            cY, cX = cls.get_screen_coords(x,y)
            cls.scr.addstr(cY, cX, str,curses.color_pair(color))
        except curses.error as e:
            pass


    @classmethod
    def get_screen_coords(cls,x,y):
        return (-int(cls.pany) + y, -int(cls.panx) + x*2)


    @classmethod
    def draw_orbits(cls):
        """ Draws the orbits stored in the Terrain instance around the star."""

        #TODO: use character from config file
        middle = [i//2 for i in Terrain.size]
        for r in Terrain.orbits:
            to_add = utils.get_circle(r)
            for coord in to_add:
                x,y = middle[0]+coord[0],middle[1]+coord[1]
                cls.draw(x, y, '.', 4)
                
    @classmethod
    def draw_radius(cls, ship):
        """ Draws a circle around a ship indicating where it can move.
        
        Gets called when cursor is on top of ship. Calculates radius from ship's fuel.
        """

        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = cls.posx + coord[0], cls.posy + coord[1]
            cls.draw(x, y, '.', 2)

    @classmethod
    def draw_lock(cls, ship, cx, cy):
        """ Draws a circle around a ship indicating where it can move when locked onto.
        
        Gets called when cursor is locked on ship. Calculates radius from ship's fuel.
        """

        #TODO: merge with draw_radius
        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = cx + coord[0], cy + coord[1]
            cls.draw(x, y, '.', 3)
    
    @classmethod
    def draw_pointer(cls):
        """Draws cursor on screen."""

        #TODO: use different char for cursor when moving ship
        #TODO: rename to draw_cursor ?
        #TODO: read char from config file
        cls.draw(cls.posx,cls.posy, '░', 4)

    @classmethod
    def draw_main_ui(cls):
        """Draws UI menus. """
        
        for i in cls.uis:
            if cls.uis[i] is not None:
                cls.uis[i].draw(cls.scr,cls.x,cls.y)

    @classmethod
    def draw_terrain(cls, planet):
        #creates static window
        win = Plot.uis["static"]
        Plot.uis["left"].draw(cls.scr,cls.x,cls.y)
        Plot.uis["right"].draw(cls.scr,cls.x,cls.y)
        win.draw(cls.scr)
        
        #limits horizontal panning to width of terrain
        if win.width > len(planet.terrain)*2 - planet.panx*2 and planet.panx > 0:
            planet.panx -= 1

        #limits vertical panning to width of terrain
        if win.height > len(planet.terrain[0]) - planet.pany and planet.pany > 0:
            planet.pany -= 1

        if planet.panx < 0:
            planet.panx += 1
        
        if planet.pany <= 0:
            planet.pany += 1

        #draws terrain
        for column in range(win.width):
            for row in range(win.height):
                #limits drawing to borders of window
                if column +  planet.panx < len(planet.terrain) \
                and column*2  < win.width \
                and row + planet.pany < len(planet.terrain[0]) \
                and column +  planet.panx >= 0 \
                and row + planet.pany >= 0:
                    tile = planet.terrain[column+int(planet.panx)][row+int(planet.pany)]
                    if   tile.height < 0.25:  s = "░░"
                    elif tile.height < 0.50:  s = "▒▒"
                    elif tile.height < 0.75:  s = "▓▓"
                    else:                     s = "██"
                    if planet.posx == column+int(planet.panx) and planet.posy + 1 == row+int(planet.pany):
                        s = "<>"
                    x = win.x_margin+column*2+1
                    y = win.y_margin+row+1
                    cls.scr.addstr(y, x, s, curses.color_pair(4))

        


    @classmethod
    def plot_terrain(cls):
        """Draws the state of the board, along with the orbit, pointers and ship's movement radius."""
        
        #TODO: rename to draw_state and create a new plot_terrain to handle the board
        cls.draw_orbits()
        cls.draw_pointer()
        current = Terrain.terrain[cls.posx][cls.posy]
        if current.search() == "Ship":
            cls.draw_radius(current)
        for column in range(len(Terrain.terrain)):
            for row in range(len(Terrain.terrain[column])):
                point = Terrain.terrain[column][row]
                if point.search():
                    color = 4
                    string = point.char
                    cls.draw(column, row, string, color)


    @classmethod
    def set_ui(cls, s):
        if s == "Terrain":
            cls.uis["static"] = Static_Window(8,0)
            cls.uis["left"] = Panel(["Temperature", "Elevation","Humidity"],"Left")
            cls.uis["right"] = Panel(["Build", "Select","Remove"],"Right")


        elif s == "Main":
            cls.uis["static"] = None
            cls.uis["left"] = Panel(["Ships", "Production","Resources"],"Left")
            cls.uis["right"] = Panel(["Colonies","Research","Pause"],"Right")
            cls.uis["bottom"] = Panel(["Next Turn"],"Bottom")
            cls.uis["top"] = Panel(["Map", "Info","Ship","Battle","Tech"],"Top")
