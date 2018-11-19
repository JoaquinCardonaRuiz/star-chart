from log import Log
from plot import Plot
from terrain import Terrain
from curses import wrapper
from time import sleep

logger = Log()
logger.add("Program started")
plotter = Plot(logger)
logger.add("Program started")
scr = plotter.start()

try:
    while True:
            y, x = scr.getmaxyx()
            sleep(0.1)
            scr.clear()
            if y >= 35 and x >= 135:
                plotter.draw_border(scr,x,y)
                key = scr.getkey()
                scr.addstr(2,2,key)
                if key == "q":
                    logger
                    plotter.end(scr)
                    exit()
            else:
                string = "Window must be at least 135x35"
                scr.addstr(int(y/2),int(x/2) - int(len(string)/2),string)
            scr.refresh()
except:
    raise
finally:    
    plotter.end(scr)

'''
terrain = Terrain(5)
plotter.plot_terrain(terrain)
'''
