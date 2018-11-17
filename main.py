from log import Log
from plot import Plot
from terrain import Terrain

logger = Log()
plotter = Plot(logger)
plotter.get_circle(10)
logger.print()
terrain = Terrain()
terrain.add_circle(plotter,20)
terrain.add_circle(plotter,10,(20,0))
plotter.plot_terrain(terrain)
