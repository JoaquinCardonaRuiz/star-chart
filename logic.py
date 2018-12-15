from log import Log
from plot import Plot
from terrain import Terrain
import configparser


class Logic:

    logger = Log()
    logger.add("Program started")
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except:
        print("init error")
        quit()
    terrain = Terrain(5,logger,config)
    plotter = Plot(logger,config, terrain)
    scr = plotter.start()
    y, x = scr.getmaxyx()
    lock = False

    def refresh():
        Logic.scr.refresh()

    def pause(string):
        Logic.scr.addstr(int(Logic.y/2),int(Logic.x/2) - int(len(string)/2),string)
    
    def check_screen_size():
        Logic.scr.clear()
        return(Logic.y >= 38 and Logic.x >= 150)

    def draw_state():
        Logic.plotter.plot_terrain(Logic.scr)
        Logic.plotter.draw_border(Logic.scr,Logic.x,Logic.y)

    def get_input():
        return Logic.scr.getkey()

    def handle_input(key):
        if key == "q":
            Logic.logger.add("Closing Program...")
            Logic.plotter.end(Logic.scr)
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
            
    def end():
        Logic.plotter.end(Logic.scr)