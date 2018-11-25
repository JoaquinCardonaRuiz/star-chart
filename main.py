from log import Log
from plot import Plot
from terrain import Terrain
from curses import wrapper
from time import sleep
import configparser

logger = Log()
logger.add("Program started")
config = configparser.ConfigParser()
config.read('config.ini')
plotter = Plot(logger,config)
scr = plotter.start()
terrain = Terrain(5,logger,config)

try:
    while True:
        y, x = scr.getmaxyx()
        sleep(0.001)
        scr.clear()
        if y >= 38 and x >= 150:
            plotter.draw_border(scr,x,y)
            plotter.plot_terrain(scr, terrain)
            #CODE BEFORE HERE
            key = scr.getkey()
            #scr.addstr(2,2,key)
            if key == "q":
                logger.add("Closing Program...")
                plotter.end(scr)
                logger.print()
                exit()
            else:
                plotter.pan_camera(key)
        else:
            string = "Window must be at least 150x38"
            scr.addstr(int(y/2),int(x/2) - int(len(string)/2),string)
        scr.refresh()
except:
    raise
finally:    
    plotter.end(scr)
