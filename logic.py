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
        if "Ship" in locked.identity:
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
                    Log.add("Trying to move ship...")
                    if Terrain.terrain[Logic.lock[0]][Logic.lock[1]].identity[-1] == "Ship":
                        Log.add("Ship id positive, moving...")
                        Terrain.move(Logic.lock[0], Logic.lock[1], Plot.posx, Plot.posy)
                    else:
                        Log.add("Not a ship")
                    Logic.lock = False
                else:
                    s = Terrain.terrain[Plot.posx][Plot.posy].identity
                    if s != ["Empty"]:
                        Logic.lock = (Plot.posx,Plot.posy)
                        Log.add("Locked onto " +str(Logic.lock))
                        if "Planet" in s:
                            Logic.stage = "Terrain"
                            Plot.set_ui(Logic.stage)
                    else:
                        Log.add("Nothing to lock onto")
                            

        if Logic.stage == "Terrain":
            if key == "q":
                Logic.lock = False
                Logic.stage = "Main"
                Plot.set_ui(Logic.stage)

            elif key in ['w','a','s','d']:
                locked = Terrain.terrain[Logic.lock[0]][Logic.lock[1]]
                Plot.pan_terrain_camera(key, locked)

        selection_keys = {"g": "left", "y": "top", "j": "right", "n": "bottom"}
        movement_keys = {"b":"bottom_left", "m":"bottom_right", "t":"top_left","u":"top_right"}

        if key in selection_keys.keys():
            for ui in [i for i in Plot.uis if (Plot.uis[i] != None and i != "static")]:
                Plot.uis[ui].defocus()
            #if not(any([Plot.uis[i].focused if (Plot.uis[i] != None and "Window" not in Plot.uis[i].identity ) else False for i in Plot.uis])):
            Plot.uis[selection_keys[key]].toggle_focus()

        if key in movement_keys:
            ui = [i for i in [i for i in Plot.uis if Plot.uis[i] != None] if Plot.uis[i].focused]
            if ui != []:
                ui = ui[0]
            
            if Plot.uis[ui].direction == "Left":
                if key == "b":
                    Plot.uis[ui].move_selection(1)
                if key == "t":
                    Plot.uis[ui].move_selection(-1)

            if Plot.uis[ui].direction == "Right":
                if key == "m":
                    Plot.uis[ui].move_selection(1)
                if key == "u":
                    Plot.uis[ui].move_selection(-1)
            
            if Plot.uis[ui].direction == "Top":
                if key == "u":
                    Plot.uis[ui].move_selection(1)
                if key == "t":
                    Plot.uis[ui].move_selection(-1)
            
            if Plot.uis[ui].direction == "Bottom":
                if key == "m":
                    Plot.uis[ui].move_selection(1)
                if key == "b":
                    Plot.uis[ui].move_selection(-1)

            #TODO: mover indice del panel


        elif key == 'h':
            Plot.uis["static"] = None
            Logic.stage = "Main"
            for win in Plot.uis:
                try:
                    Plot.uis[win].defocus()
                except:
                    pass
        

    @staticmethod    
    def end():
        """Calls method to perform necessary steps for clean exit."""

        Plot.end()  