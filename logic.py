from log import Log
from plot import Plot
from board import Board
from config import Config
from ui import *
from states import State_Main, State_Terrain


class Logic:
    """Logic module for StarChart. Contains all methods called by main.py.
    
    Class variables:
        lock    -- Holds the coordinates of the locked object, False if nothing is locked
        state   -- Holds the screen UI is currently in
    """
    
    #Initializing
    #TODO: make config file specific to plotter (config_plot.ini)
    #TODO: review previous todo
    #TODO: implement turns and orbits around planets when turns pass
    
    
    #states = main, terrain, battle, tech, etc..
    state = State_Main
    state_chain = [state]
    Plot.start()
    Board.start(5)
    State_Main.init()
    Log.add("Program started")

    @classmethod
    def update_screen_size(cls):
        """ Updates values of width and height of the screen (x,y) in plotter.
        
        If the terminal's size has changed, updates size values in the plotter"""

        #TODO: mobve to  plotter
        y,x = Plot.scr.getmaxyx()
        if (Plot.y != y or Plot.x != x):
            Plot.y, Plot.x = Plot.scr.getmaxyx()
            Plot.y -= 1
        
    @classmethod
    def refresh(cls):
        """Clears screen to draw next frame."""
        #TODO: move to  plotter

        Logic.update_screen_size()
        Plot.scr.refresh()
        Plot.scr.clear()
    
    @classmethod
    def draw_state(cls):
        """Calls various methods in plotter module to draw the board and UI elements."""
        #TODO: this method became superflous
        cls.state.plot()


    @classmethod
    def handle_lock(cls):
        locked = Board.terrain[Logic.lock[0]][Logic.lock[1]]
        if "Ship" in locked.identity:
            Plot.draw_lock(Board.terrain[Logic.lock[0]][Logic.lock[1]],Logic.lock[0],Logic.lock[1])
        """
        elif locked.search() == "Planet":
            Plot.draw_terrain(locked)
        """
 

    @classmethod
    def get_input(cls):
        """Reads keyboard input from user"""
        return Plot.scr.getkey()

    @classmethod
    def handle_input(cls):
        """Takes the key pressed by the user and calls the appropiate method.
        
        Bindings:
            q       -- Quits game / Quits Menu
            w,a,s,d -- Moves cursor / UI Selection
            e       -- locks and unlocks cursor / Accept
            t y u
            g h j
            b n m
        """
        #change will be False if there is no need to change stage
        #if there is, change[0] will contain a string indicating either the stage
        #or an instruction for moving in the stage chain (like "back")
        #further indexes will contain the necessary arguments for the transition, like the object

        key = cls.get_input()

        change = cls.state.handle_input(key)
        if change:
            if change[0] == "end":
                cls.end()

            elif change[0] == "terrain":
                cls.state = State_Terrain
                cls.state_chain.append(cls.state)
                cls.state.init(change[1])

            elif change[0] in ["Minerals","Humidity","Elevation","Info"]:
                cls.state = State_Terrain
                cls.state_chain[-1] = cls.state
                cls.state.change_view(change[0])

            elif change[0] in ["Build", "Select", "Remove"]:
                cls.state.change_action(change[0])

            elif change[0] == "back":
                cls.state_chain = cls.state_chain[:-1]
                cls.state = cls.state_chain[-1]

            elif change[0] == "main":
                cls.state_chain = cls.state_chain[0]
                cls.state = cls.state_chain[0]

            Log.add(str(cls.state_chain))

        

    @classmethod    
    def end(cls, exception = ''):
        """Calls method to perform necessary steps for clean exit."""
        Plot.end()
        if exception:
            Log.add(str(exception))
        Log.add('Exiting program')
        Log.print()
        exit()