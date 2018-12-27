from log import Log
from plot import Plot
from terrain import Terrain
import configparser


class Logic:
    '''
    Logic module for StarChart. 
    Contains all methods called by main.py,
    as well as a plotter, the class responsible for graphics.
    '''
    
    #Initializing
    logger = Log()                              #Responsible for logging events
    config = configparser.ConfigParser()        #Config file reader
    try:
        config.read('config.ini')
    except:
        print("init error")
        quit()
    terrain = Terrain(5,logger,config)          #Holds the state of the board
    plotter = Plot(logger, config, terrain)     #Responsible for graphics
    scr = plotter.start(logger)                 #Screen object
    lock = False                                #Holds the coordinates of the locked object, otherwise False
    logger.add("Program started")

    def update_screen_size():
        #If the terminal's size has changed, updates size values in the plotter
        y,x = Logic.scr.getmaxyx()
        if (Logic.plotter.y != y or Logic.plotter.x != x):
            Logic.plotter.y, Logic.plotter.x = Logic.scr.getmaxyx()
            Logic.plotter.y -= 1
        

    def refresh():
        Logic.update_screen_size()
        Logic.scr.refresh()
        Logic.scr.clear()
    
    def draw_state():
        #Calls plotter module to draw the board and UI elements
        Logic.plotter.plot_terrain(Logic.scr)
        Logic.plotter.draw_border(Logic.scr)
        if Logic.lock:
            Logic.plotter.draw_lock(Logic.terrain.terrain[Logic.lock[0]][Logic.lock[1]], Logic.scr,Logic.lock[0],Logic.lock[1])
        Logic.plotter.draw_UI(Logic.scr)

    def get_input():
        return Logic.scr.getkey()

    def handle_input(key):
        #Takes the key pressed by the user and calls the appropiate method
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
        Logic.plotter.end(Logic.scr)