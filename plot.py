import math
from log import Log 
import curses
import utils
import time
from ui import Panel, Window, Static_Window
from board import Board
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
    scr = None

    @classmethod
    def start(cls):
        """Initializes graphics engine, and returns an instance of the curses Screen class.
        
        Sets starting positions for cursor and camera, initializes color profiles and terminal settigs.
        """
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
        Log.add(str(cls.x))
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
        Log.add('Terminated plotter')
        
    @classmethod
    def draw(cls, x,y,panx,pany, str, color):
        """Draws a string or character on the screen.
        
        Keyword Arguments:
            x,y     -- Coordinates where first character will be drawn
            str     -- String or character to draw
            color   -- Color profile to use
        """
        try:
            cY, cX = cls.get_screen_coords(x,y,panx,pany)
            cls.scr.addstr(cY, cX, str,curses.color_pair(color))
        except curses.error as e:
            pass


    @classmethod
    def get_screen_coords(cls,x,y,panx,pany):
        return (-int(pany) + y, -int(panx) + x*2)


    """
        elif s == "Pause":
            cls.uis["left"], cls.uis["right"], cls.uis["bottom"], cls.uis["top"] = None, None, None, None
            cls.uis["static"] = Panel(["Main","Options","Exit"],"center")
            cls.uis["static"].focus()
    """