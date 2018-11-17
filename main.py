from log import Log
from plot import Plot
from terrain import Terrain
import pyxel

pyxel.init(254, 254)
logger = Log()
logger.add("Program started")
plotter = Plot(logger)
plotter.get_circle(10)
logger.print()
terrain = Terrain(5)
plotter.plot_terrain(terrain)

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    plotter.draw_circ(0,0,5,2)

pyxel.run(update, draw)
