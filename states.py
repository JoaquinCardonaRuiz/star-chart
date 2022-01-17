from plot import Plot
from board import Board
from config import Config
from entities.buildings import buildings
from entities.bodies import Planet
from log import Log
import utils
from ui import *

class State(metaclass=utils.Meta):
    #We define utils.Meta as the metaclass to gain use of __repr__ for the class instead of the instance
    #uis = {}

    @classmethod
    def draw_ui(cls):
        for i in cls.uis:
            if cls.uis[i] is not None:
                cls.uis[i].draw(Plot.scr,Plot.x,Plot.y)

    @classmethod
    def handle_ui_input(cls,key):
        #TODO: Parametrize actions for each key, so no need to use so many elifs
        #Actually they all do the same so this is dumb. Correct asap

        selection_keys = {"g": "left", "y": "top", "j": "right", "n": "bottom"}
        movement_keys = {"b":"bottom_left", "m":"bottom_right", "t":"top_left","u":"top_right"}

        if key in selection_keys.keys():
            uis = [cls.uis[i] for i in cls.uis if (cls.uis[i] != None and i != "static")]
            selected_uis = [i for i in uis if i.focused]
            if selected_uis == []:
                if selection_keys[key] in cls.uis:
                    cls.uis[selection_keys[key]].toggle_focus()
            else:
                ui = selected_uis[0]
                if ui.direction == "left" and key == "g":
                    return [ui.lines[ui.selected]]
                elif ui.direction == "right" and key == "j":
                    return [ui.lines[ui.selected]]
                elif ui.direction == "top" and key == "y":
                    return [ui.lines[ui.selected]]
                elif ui.direction == "bottom" and key == "n":
                    return [ui.lines[ui.selected]]
                elif ui.direction == "center":
                    if key == "n":
                        ui.move_selection(1)
                    elif key == "y":
                        ui.move_selection(-1)
                    elif key == "h":
                        return [ui.lines[ui.selected]]
                else:
                    ui.defocus()
                    if selection_keys[key] in cls.uis:
                        cls.uis[selection_keys[key]].toggle_focus()                        

        if key in movement_keys:
            ui = [i for i in [i for i in cls.uis if (cls.uis[i] != None and i != "static")] if cls.uis[i].focused]
            if ui != []:
                ui = ui[0]
                if cls.uis[ui].direction == "left":
                    if key == "b":
                        cls.uis[ui].move_selection(1)
                    if key == "t":
                        cls.uis[ui].move_selection(-1)

                if cls.uis[ui].direction == "right":
                    if key == "m":
                        cls.uis[ui].move_selection(1)
                    if key == "u":
                        cls.uis[ui].move_selection(-1)
                
                if cls.uis[ui].direction == "top":
                    if key == "u":
                        cls.uis[ui].move_selection(1)
                    if key == "t":
                        cls.uis[ui].move_selection(-1)
                
                if cls.uis[ui].direction == "bottom":
                    if key == "m":
                        cls.uis[ui].move_selection(1)
                    if key == "b":
                        cls.uis[ui].move_selection(-1)

            #TODO: mover indice del panel

        if key == 'h':
            #TODO have this return "back" if on a main window, but if on ui panel return something that takes back to that window
            for win in cls.uis:
                try:
                    cls.uis[win].defocus()
                except:
                    pass
        
        return False

class State_Main(State):
    #TODO resolve conflict between names "main" and "map". Leave as map
    uis = {}

    @classmethod
    def init(cls):
        cls.string_repr = "Main State"
        cls.uis["static"] = None
        cls.uis["left"] = Panel(["Ships", "Production","Resources"],"left")
        cls.uis["right"] = Panel(["Colonies","Research","Pause"],"right")
        cls.uis["bottom"] = Panel(["Next Turn"],"bottom")
        cls.uis["top"] = Panel(["Map", "Info","Ship","Battle","Tech"],"top")
        cls.lock = False
        middle = [i//2 for i in Board.size]
        cls.posx,cls.posy = middle[0],middle[1]
        cls.panx,cls.pany = Board.size[0] - int(Plot.x /2), 18 + int(0.5 * ((Board.size[1] - int(Plot.y *2)))) 
        Log.add('State set to map')

    @classmethod
    def draw_orbits(cls):
        """ Draws the orbits stored in the Board instance around the star."""

        #TODO: use character from config file
        middle = [i//2 for i in Board.size]
        for r in Board.orbits:
            to_add = utils.get_circle(r)
            for coord in to_add:
                x,y = middle[0]+coord[0],middle[1]+coord[1]
                Plot.draw(x, y, cls.panx, cls.pany,'.', 4)

    @classmethod
    def draw_pointer(cls):
        """Draws cursor on screen."""

        #TODO: use different char for cursor when moving ship
        #TODO: rename to draw_cursor ?
        #TODO: read char from config file
        #TODO: have tile change background color when pointer on object
        Plot.draw(cls.posx,cls.posy,cls.panx,cls.pany, '░', 4)

    @classmethod
    def draw_radius(cls, ship):
        """ Draws a circle around a ship indicating where it can move.
        
        Gets called when cursor is on top of ship. Calculates radius from ship's fuel.
        """

        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = cls.posx + coord[0], cls.posy + coord[1]
            Plot.draw(x, y ,cls.panx,cls.pany,'.', 2)

    @classmethod
    def draw_lock(cls, ship, cx, cy):
        """ Draws a circle around a ship indicating where it can move when locked onto.
        
        Gets called when cursor is locked on ship. Calculates radius from ship's fuel.
        """

        #TODO: merge with draw_radius
        to_add = utils.get_circle(ship.fuel,False)
        for coord in to_add:
            x,y = cx + coord[0], cy + coord[1]
            Plot.draw(x, y,cls.panx,cls.pany, '.', 3)

    @classmethod
    def draw_terrain(cls):
        """Draws the state of the board, along with the orbit, pointers and ship's movement radius."""
        current = Board.terrain[cls.posx][cls.posy]
        if "Ship" in current.identity:
            cls.draw_radius(current)
        for column in range(len(Board.terrain)):
            for row in range(len(Board.terrain[column])):
                point = Board.terrain[column][row]
                if point.identity[0] != "Empty":
                    color = 4
                    string = Config.chars['Chars'][point.identity[0]]                   
                    Plot.draw(column, row,cls.panx,cls.pany, string, color)
    
    @classmethod
    def pan_camera(cls, direction):
        """Takes a direction in the form of a character and moves cursor and camera appropriately."""

        #TODO: Rename method. It moves the cursor as well as panning the camera
        y,x = Plot.get_screen_coords(cls.posx, cls.posy, cls.panx,cls.pany)
        if direction == 's' and cls.posy < Board.size[1]-1:
            cls.posy += 1
            if (y >= Plot.y*0.8):
                cls.pany += 1
        elif direction == 'w' and cls.posy > 0:
            cls.posy -= 1
            if (y <= Plot.y*0.2):
                cls.pany -= 1
        elif direction == 'd' and cls.posx < Board.size[0] - 1:
            cls.posx += 1
            if (x >= Plot.x*0.8):
                cls.panx += 2
        elif direction == 'a' and cls.posx > 0:
            cls.posx -= 1
            if (x <= Plot.x*0.2):
                cls.panx -= 2

    @classmethod
    def handle_input(cls, key):
        #TODO call handle_ui_input where handle_input is called, not inside here
        if key == "q":
            Log.add("Closing Program...")
            return ["end"]
            
        elif key in ['w','a','s','d']:
            cls.pan_camera(key)

        elif key == 'e':
            if cls.lock:
                Log.add("Trying to move ship...")
                if Board.terrain[cls.lock[0]][cls.lock[1]].identity[-1] == "Ship":
                    Log.add("Ship id positive, moving...")
                    Board.move(cls.lock[0], cls.lock[1], cls.posx, cls.posy)
                else:
                    Log.add("Not a ship")
                cls.lock = False
            else:
                s = Board.terrain[cls.posx][cls.posy].identity
                if s != ["Empty"]:
                    cls.lock = (cls.posx,cls.posy)
                    Log.add("Locked onto " +str(cls.lock))
                    if "Planet" in s:
                        planet = Board.terrain[cls.lock[0]][cls.lock[1]]
                        cls.lock = False
                        return ["terrain",planet]
                else:
                    Log.add("Nothing to lock onto")
        return cls.handle_ui_input(key)

    @classmethod
    def handle_lock(cls):
        locked = Board.terrain[cls.lock[0]][cls.lock[1]]
        if "Ship" in locked.identity:
            cls.draw_lock(Board.terrain[cls.lock[0]][cls.lock[1]],cls.lock[0],cls.lock[1])
        """
        elif locked.search() == "Planet":
            Plot.draw_terrain(locked)
        """

    @classmethod
    def plot(cls):
        #TODO: move handle_lock to some logic based method inside the class
        cls.draw_orbits()
        cls.draw_pointer()
        cls.draw_terrain()
        Plot.draw_border()
        cls.draw_ui()
        if cls.lock:
            cls.handle_lock()


class State_Terrain(State):
    uis = {}

    @classmethod
    def init(cls,locked):
        cls.uis["static"] = Static_Window(16,0)
        cls.uis["left"] = Panel(["Info", "Minerals", "Elevation","Humidity"],"left")
        cls.uis["right"] = Panel(["Build", "Select","Remove"],"right")
        cls.uis["info"] = Widget([{'label':'Height: ','value':0},
                                  {'label':'Minerals: ','value':0},
                                  {'label':'Humidity: ','value':0}])
        cls.locked = locked
        cls.view = "Elevation"
        cls.string_repr = "Terrain State - " + cls.view
        Log.add('State set to terrain')


    @classmethod
    def draw_terrain(cls):
        #TODO: do away with static window
        win = cls.uis["static"]
        win.draw(Plot.scr)
        
        #limits horizontal panning to width of terrain
        if win.width > len(cls.locked.terrain)*2 - cls.locked.panx*2 and cls.locked.panx > 0:
            cls.locked.panx -= 1

        #limits vertical panning to width of terrain
        if win.height > len(cls.locked.terrain[0]) - cls.locked.pany and cls.locked.pany > 0:
            cls.locked.pany -= 1

        if cls.locked.panx < 0:
            cls.locked.panx += 1
        
        if cls.locked.pany <= 0:
            cls.locked.pany += 1

        #draws terrain
        for column in range(win.width-2):
            for row in range(win.height):
                #limits drawing to borders of window
                if column +  cls.locked.panx < len(cls.locked.terrain) \
                and column*2  < win.width \
                and row + cls.locked.pany < len(cls.locked.terrain[0]) \
                and column +  cls.locked.panx >= 0 \
                and row + cls.locked.pany >= 0:
                    tile = cls.locked.terrain[column+int(cls.locked.panx)][row+int(cls.locked.pany)]
                    if cls.view == "Elevation":
                        if   tile.height < 0.20:  s = "  "
                        elif tile.height < 0.40:  s = "░░"
                        elif tile.height < 0.60:  s = "▒▒"
                        elif tile.height < 0.80:  s = "▓▓"
                        else:                     s = "██"
                    elif cls.view == "Minerals":
                        if   tile.minerals == 0:    s = "  "
                        elif tile.minerals < 1250:  s = "░░"
                        elif tile.minerals < 2500:  s = "▒▒"
                        elif tile.minerals < 3750:  s = "▓▓"
                        else:                       s = "██"
                    elif cls.view == "Humidity":
                        if   tile.humidity < 0.20:  s = "  "
                        elif tile.humidity < 0.40:  s = "░░"
                        elif tile.humidity < 0.60:  s = "▒▒"
                        elif tile.humidity < 0.80:  s = "▓▓"
                        else:                       s = "██"
                    if cls.locked.posx == column+int(cls.locked.panx) and cls.locked.posy + 1 == row+int(cls.locked.pany):
                        s = "<>"
                    x = win.x_margin+column*2+1
                    y = win.y_margin+row+1
                    Plot.scr.addstr(y, x, s, curses.color_pair(4))

    @classmethod
    def draw_info(cls):
        win = cls.uis["static"]
        win.draw(Plot.scr)
        for i,key in enumerate(cls.locked.characteristics.keys()):
            s = key + ": " + str(cls.locked.characteristics[key]['value'])
            if cls.locked.characteristics[key]['key']:
                s += " (" + cls.locked.characteristics[key]['key']+")" 
            Plot.scr.addstr(i+1,win.x_margin+2,s,curses.color_pair(4))


    @classmethod
    def pan_terrain_camera(cls, direction):
        #TODO simplify panning ifs... good luck tho
        if direction == 's' and cls.locked.posy + 1 < Planet.sizes[str(cls.locked.size)] - 1:
            cls.locked.posy += 1
            if (cls.locked.posy - cls.locked.pany >= 0.8 * cls.uis["static"].get_size(Plot.scr)[1]):
                cls.locked.pany += 1
        elif direction == 'w' and cls.locked.posy > 0:
            cls.locked.posy -= 1
            if (cls.locked.posy - cls.locked.pany <= 0.2 * cls.uis["static"].get_size(Plot.scr)[1]):
                cls.locked.pany -= 1
        elif direction == 'd' and cls.locked.posx < Planet.sizes[str(cls.locked.size)] - 1:
            cls.locked.posx += 1
            if (cls.locked.posx * 2 - cls.locked.panx*2 >= 0.8 * cls.uis["static"].get_size(Plot.scr)[0]):
                cls.locked.panx += 1
        elif direction == 'a' and cls.locked.posx > 0:
            cls.locked.posx -= 1
            if (cls.locked.posx * 2 - cls.locked.panx*2 <= 0.2 * cls.uis["static"].get_size(Plot.scr)[0]):
                cls.locked.panx -= 1

    @classmethod
    def handle_input(cls, key):
        if key == "q":
            return ["back"]

        elif key in ['w','a','s','d']:
            #locked = Board.terrain[cls.lock[0]][cls.lock[1]]
            if cls.view in ['Minerals','Elevation','Humidity']:
                cls.pan_terrain_camera(key)
                tile = cls.locked.terrain[cls.locked.posx][cls.locked.posy]
                cls.uis["info"].update_all_values([tile.height,tile.minerals,tile.humidity])

        return cls.handle_ui_input(key)

    @classmethod
    def plot(cls):
        Plot.draw_border()
        cls.draw_ui()
        if cls.view == "Info":
            cls.draw_info()
        else:
            cls.draw_terrain()
        


    @classmethod
    def change_view(cls,view):
        cls.view = view
        cls.change_action('Select')
        cls.string_repr = "Terrain State - " + cls.view
        if cls.view in ['Minerals','Elevation','Humidity']:
            cls.uis["info"] = Widget([{'label':'Height: ','value':0},
                                  {'label':'Minerals: ','value':0},
                                  {'label':'Humidity: ','value':0}])
        else:
            cls.uis['info'] = None   

    @classmethod
    def change_action(cls,action):
        cls.action = action
        if cls.action == 'Select':
            cls.uis["right"] = Panel(["Build", "Select","Remove"],"right")
        
        if cls.action == 'Build':
            cls.uis["right"] = ItemPanel([building.item_repr() for building in buildings],"right")
            cls.uis["right"].selected = 0
            cls.uis["right"].focused = True
            

class State_Pause(State):
    pass


class State_Ships(State):
    pass

    