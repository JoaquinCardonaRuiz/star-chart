from log import Log
from plot import Plot
from terrain import Terrain
from config import Config
from ui import *


class Logic:
    """Logic module for StarChart. Contains all methods called by main.py.
    
    Class variables:
        lock    -- Holds the coordinates of the locked object, False if nothing is locked
        stage   -- Holds the screen UI is currently in
    """
    
    #Initializing
    #TODO: make config file specific to plotter (config_plot.ini)
    #TODO: implement turns and orbits around planets when turns pass
    
    
    lock = False
    #stages = main, terrain, battle, tech, etc..
    stage = "Main"
    Plot.start()
    Plot.set_ui("Main")
    Terrain.start(5)
    Log.add("Program started")

    @staticmethod
    def update_screen_size():
        """ Updates values of width and height of the screen (x,y) in plotter.
        
        If the terminal's size has changed, updates size values in the plotter"""

        #TODO: move x,y to Logic, get them out of plotter
        y,x = Plot.scr.getmaxyx()
        if (Plot.y != y or Plot.x != x):
            Plot.y, Plot.x = Plot.scr.getmaxyx()
            Plot.y -= 1
        
    @staticmethod
    def refresh():
        """Clears screen to draw next frame."""

        Logic.update_screen_size()
        Plot.scr.refresh()
        Plot.scr.clear()
    
    @staticmethod
    def draw_state():
        """Calls various methods in plotter module to draw the board and UI elements."""
        if Logic.stage == "Main":
            Plot.plot_terrain()
            Plot.draw_border()
            Plot.draw_main_ui()
        if Logic.stage == "Terrain":
            Plot.draw_border()
            locked = Terrain.terrain[Logic.lock[0]][Logic.lock[1]]
            Plot.draw_terrain(locked)
        if Logic.lock:
            Logic.handle_lock()


    @staticmethod
    def handle_lock():
        locked = Terrain.terrain[Logic.lock[0]][Logic.lock[1]]
        if locked.search() == "Ship":
            Plot.draw_lock(Terrain.terrain[Logic.lock[0]][Logic.lock[1]],Logic.lock[0],Logic.lock[1])
        """
        elif locked.search() == "Planet":
            Plot.draw_terrain(locked)
        """
 

    @staticmethod
    def get_input():
        """Reads keyboard input from user"""

        return Plot.scr.getkey()

    @staticmethod
    def handle_input(key):
        """Takes the key pressed by the user and calls the appropiate method.
        
        Bindings:
            q       -- Quits game / Quits Menu
            w,a,s,d -- Moves cursor / UI Selection
            e       -- locks and unlocks cursor / Accept
            t y u
            g h j
            b n m
        """
        
        if Logic.stage == "Main":
            if key == "q":
                Log.add("Closing Program...")
                Logic.end()
                Log.print()
                exit()
            
            elif key in ['w','a','s','d']:
                Plot.pan_camera(key)

            elif key == 'e':
                if Logic.lock:
                    if Terrain.terrain[Logic.lock[0]][Logic.lock[1]].search() == "Ship":
                        Terrain.move(Logic.lock[0], Logic.lock[1], Plot.posx, Plot.posy)
                    Logic.lock = False
                else:
                    s = Terrain.terrain[Plot.posx][Plot.posy].search()
                    if s:
                        Logic.lock = (Plot.posx,Plot.posy)
                        Log.add("Locked onto " +str(Logic.lock))
                        if s == "Planet":
                            Logic.stage = "Terrain"
                            Plot.set_ui(Logic.stage)
                            

        if Logic.stage == "Terrain":
            if key == "q":
                Logic.lock = False
                Logic.stage = "Main"
                Plot.set_ui(Logic.stage)

            elif key in ['w','a','s','d']:
                locked = Terrain.terrain[Logic.lock[0]][Logic.lock[1]]
                Plot.pan_terrain_camera(key, locked)

        uikeys = {"g": "left", "y": "top", "j": "right", "n": "bottom"}

        if key in list(uikeys.keys()):
            Plot.uis[uikeys[key]].focus() 


    @staticmethod    
    def end():
        """Calls method to perform necessary steps for clean exit."""

        Plot.end()