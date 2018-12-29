from log import Log
from plot import Plot
from terrain import Terrain
import configparser


class Logic:
    """Logic module for StarChart. Contains all methods called by main.py.
    
    Class variables:
        plotter -- Instance of graphics module for star-chart (plotter.py)
        scr     -- Curses screen object
        lock    -- Boolean: True when cursor is locked in a ship
    """
    
    #Initializing
    #TODO: move scr to plotter
    #TODO: keep terrain here, remove from plotter
    #TODO: move init of logger, config and terrain to plotter
    #TODO: make config file specific to plotter (config_plot.ini)
    #TODO: keep logger here, remove from plotter
    #TODO: implement turns and orbits around planets when turns pass

    logger = Log()
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except:
        print("init error")
        quit()
    terrain = Terrain(5,logger,config)
    plotter = Plot(logger, config, terrain)
    scr = plotter.start(logger)
    lock = False
    logger.add("Program started")


    def update_screen_size():
        """ Updates values of width and height of the screen (x,y) in plotter.
        
        If the terminal's size has changed, updates size values in the plotter"""

        #TODO: move x,y to Logic, get them out of plotter
        y,x = Logic.scr.getmaxyx()
        if (Logic.plotter.y != y or Logic.plotter.x != x):
            Logic.plotter.y, Logic.plotter.x = Logic.scr.getmaxyx()
            Logic.plotter.y -= 1
        

    def refresh():
        """Clears screen to draw next frame."""

        Logic.update_screen_size()
        Logic.scr.refresh()
        Logic.scr.clear()
    

    def draw_state():
        """Calls various methods in plotter module to draw the board and UI elements."""

        #TODO: clean up lock logic, it looks like java
        Logic.plotter.plot_terrain(Logic.scr)
        Logic.plotter.draw_border(Logic.scr)
        if Logic.lock:
            Logic.plotter.draw_lock(Logic.terrain.terrain[Logic.lock[0]][Logic.lock[1]], Logic.scr,Logic.lock[0],Logic.lock[1])
        Logic.plotter.draw_UI(Logic.scr)


    def get_input():
        """Reads keyboard input from user"""

        return Logic.scr.getkey()


    def handle_input(key):
        """Takes the key pressed by the user and calls the appropiate method.
        
        Bindings:
            q       -- Quits game
            w,a,s,d -- Moves cursor
            e       -- locks and unlocks cursor
        """
        
        if key == "q":
            Logic.logger.add("Closing Program...")
            Logic.end()
            Logic.logger.print()
            exit()
        
        elif key in ['w','a','s','d']:
            Logic.plotter.pan_camera(key)

        elif key == 'e':
            if Logic.lock:
                Logic.terrain.move(Logic.lock[0], Logic.lock[1], Logic.plotter.posx, Logic.plotter.posy)
                Logic.lock = False
            else:
                if Logic.terrain.terrain[Logic.plotter.posx][Logic.plotter.posy].search():
                    Logic.lock = (Logic.plotter.posx,Logic.plotter.posy)
                    Logic.logger.add("Locked onto " +str(Logic.lock))

            
    def end():
        """Calls method to perform necessary steps for clean exit."""

        Logic.plotter.end(Logic.scr)