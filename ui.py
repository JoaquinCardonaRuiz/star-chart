import curses
from utils import identify


class Panel():

    def __init__(self, lines, direction):
        self.lines = lines
        self.direction = direction
        self.border = self.gen_border()
        self.selected = len(lines) // 2
        self.focused = False
        self.identity = identify(self)

    def move_selection(self, n):
        self.selected += n
        if self.selected >= len(self.lines):
            self.selected = 0
        if self.selected < 0:
            self.selected = len(self.lines) - 1

    def gen_border(self):
        #TODO: decide if fixed or variable width for l/r
        if self.direction in ["left","right"]:
            #Width is equal to the lenght of the longest item plus 2 for margins
            x = max(len(i) for i in self.lines) + 2
            y = len(self.lines)*4 + 2
        elif self.direction in ["top","bottom"]:
            #Width is equal to the sum of the length of all the strings...
            #plus 2 spaces between words, plus 2 for margins
            x = sum([len(i) for i in self.lines]) + len(self.lines)*2 + 3
            y = 1
        elif self.direction == "center":
            x = 13
            y = len(self.lines)*4 + 2
        return(x,y)

    def toggle_focus(self):
        if self.focused:
            self.defocus()
        elif not self.focused:
            self.focus()

    def focus(self):
        if self.direction == "top":
            self.border = [self.border[0], 3]
        self.focused = True

    def defocus(self):
        if self.direction == "top":
            self.border = [self.border[0], 1]
        self.focused = False

    def draw(self,scr,x,y):
        #TODO: move this to plot.py
        #TODO: generalize drawing algorithm
        #TODO: parametrize spaces between words
        #TODO: get margins in separate function
        #y-=1
        if self.direction == "left":
            color = 4
            margin = int((y - self.border[1])/2)
            #Draw top border
            scr.addstr(margin,0,"╠" + "═"*self.border[0] + "╗",curses.color_pair(color))
            #Draw side border
            for i in range(1,self.border[1]+1):
                scr.addstr(margin+i,1," "*self.border[0] + "║",curses.color_pair(color))
            #Draw bottom border
            scr.addstr(y-margin,0,"╠" +"═"*self.border[0] + "╝",curses.color_pair(color))
            #Draw items
            for i in range(len(self.lines)):
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr(margin+(i*4)+3,2,self.lines[i],curses.color_pair(color))

        if self.direction == "right":
            color = 4
            margin = int((y - self.border[1])/2)
            #Draw top border
            scr.addstr(margin,x - (self.border[0]+2),"╔" + "═"*self.border[0] + "╣",curses.color_pair(color))
            #Draw side border
            for i in range(1,self.border[1]+1):
                scr.addstr(margin+i,x - (self.border[0]+2),"║"+" "*self.border[0],curses.color_pair(color))
            #Draw bottom border
            scr.addstr(y-margin,x - (self.border[0]+2),"╚" + "═"*self.border[0] + "╣",curses.color_pair(color))
            #Draw items
            for i in range(len(self.lines)):
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr(margin+(i*4)+3,x-2-len(self.lines[i]),self.lines[i],curses.color_pair(color))

        if self.direction == "top":
            color = 4
            margin = int((x - self.border[0])/2)
            #Draw left border
            scr.addstr(0,margin,"╦")
            for i in range(self.border[1]):
                scr.addstr(1+i,margin,"║"+" "*self.border[0],curses.color_pair(color))
            #Draw right border
            scr.addstr(0,margin+self.border[0]+1,"╦",curses.color_pair(color))
            for i in range(self.border[1]):
                scr.addstr(1+i,margin+self.border[0]+1,"║",curses.color_pair(color))
            #Draw bottom border
            scr.addstr(self.border[1]+1 ,margin,"╚" + "═"*self.border[0] + "╝",curses.color_pair(color))
            #Draw items
            shift = 0
            for i in range(len(self.lines)):
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr(self.border[1]//2 + 1, margin+3+shift+(2*i),self.lines[i],curses.color_pair(color))
                shift += len(self.lines[i])

        if self.direction == "bottom":
            color = 4
            margin = int((x - self.border[0])/2)
            #Draw left border
            try:
                scr.addstr(y,margin,"╩",curses.color_pair(color))
            except curses.error as e:
                pass
            for i in range(self.border[1]):
                scr.addstr(y-i-1,margin,"║"+" "*self.border[0],curses.color_pair(color))
            #Draw right border
            scr.addstr(y,margin+self.border[0]+1,"╩",curses.color_pair(color))
            for i in range(self.border[1]):
                scr.addstr(y-1-i,margin+self.border[0]+1,"║",curses.color_pair(color))
            #Draw top border
            scr.addstr(y-self.border[1]-1,margin,"╔" + "═"*self.border[0] + "╗",curses.color_pair(color))
            #Draw items
            shift = 0
            for i in range(len(self.lines)):
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr(y- (self.border[1]//2)-1, margin+3+shift+(2*i),self.lines[i],curses.color_pair(color))
                shift += len(self.lines[i])

        if self.direction == "center":
            color = 4
            marginY = int((y - self.border[1])/2)
            marginX = int((x - self.border[0])/2)
            try:
                #Top border
                scr.addstr(marginY,marginX,"╔" + "═"*self.border[0] + "╗",curses.color_pair(color))
                #Bottom border
                scr.addstr(y-marginY,marginX,"╚" +"═"*self.border[0] + "╝",curses.color_pair(color))
                #Left Side
                for i in range(1,self.border[1]+1):
                    scr.addstr(marginY+i,marginX,"║"+" "*self.border[0],curses.color_pair(color))
                #Right Side
                for i in range(1,self.border[1]+1):
                    scr.addstr(marginY+i,marginX+self.border[0]+1,"║"+" "*self.border[0],curses.color_pair(color))
                #Draw items
                for i in range(len(self.lines)):
                    if self.selected == i and self.focused:
                        color = 5
                    else:
                        color = 4
                    scr.addstr(marginY+(i*4)+3,marginX+(self.border[0]//2)-len(self.lines[i])//2,self.lines[i],curses.color_pair(color))
            except curses.error as e:
                pass

class ItemPanel(Panel):

    def gen_border(self):
        #TODO: decide if fixed or variable width for l/r
        if self.direction in ["left","right"]:
            #Width is equal to the lenght of the longest item plus 2 for margins
            text_lens = []
            for item in self.lines:
                for text in item:
                    text_lens.append(len(text))
            x = max(text_lens) + 2
            y = len(self.lines)*4 + 2
        return(x,y)

    def draw(self,scr,x,y):
        #TODO: move this to plot.py
        #TODO: generalize drawing algorithm
        #TODO: parametrize spaces between words
        #TODO: get margins in separate function
        #y-=1
        if self.direction == "left":
            color = 4
            margin = int((y - self.border[1])/2)
            #Draw top border
            scr.addstr(margin,0,"╠" + "═"*self.border[0] + "╗",curses.color_pair(color))
            #Draw side border
            for i in range(1,self.border[1]+1):
                scr.addstr(margin+i,1," "*self.border[0] + "║",curses.color_pair(color))
            #Draw bottom border
            scr.addstr(y-margin,0,"╠" +"═"*self.border[0] + "╝",curses.color_pair(color))
            #Draw items
            for i in range(len(self.lines)):
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr(margin+(i*4)+3,2,self.lines[i],curses.color_pair(color))

        if self.direction == "right":
            color = 4
            #Draw side border
            for i in range(1,y):
                scr.addstr(i,x - (self.border[0]+2),"║"+" "*self.border[0],curses.color_pair(color))
            #Draw top border
            scr.addstr(0, x - (self.border[0]+2), "╦" + "═"*self.border[0] + "╗",curses.color_pair(color))
            #Draw items
            for i in range(len(self.lines)):
                if i != 0:
                    scr.addstr((i*4), x - (self.border[0]+2), "╠" + "-"*self.border[0] + "╣",curses.color_pair(color))
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr((i*4)+1, x-2-len(self.lines[i][0]), self.lines[i][0],curses.color_pair(color))
                scr.addstr((i*4)+2, x-2-len(self.lines[i][1]), self.lines[i][1],curses.color_pair(color))
                scr.addstr((i*4)+3, x-2-len(self.lines[i][2]), self.lines[i][2],curses.color_pair(color))
                color = 4
                scr.addstr((i*4)+4, x - (self.border[0]+2), "╠" + "-"*self.border[0] + "╣",curses.color_pair(color))
    

class Window():
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.identity = identify(self)
        
class Static_Window():
    def __init__(self,x_margin,y_margin):
        self.identity = identify(self)
        self.focused = True
        self.x_margin = x_margin*2
        self.y_margin = y_margin
        
    def get_size(self,scr):
        y,x = scr.getmaxyx()
        #Not sure why the -2 is necessary to center the window
        width,height = x - 2*self.x_margin-2, y - 2*self.y_margin-2
        return (width,height)

    def draw(self,scr,x=0,y=0):
        color = 4
        width, height = self.get_size(scr)
        Window.__init__(self,width,height)

        #draw top border
        scr.addstr(self.y_margin,self.x_margin,"╔"+"═"*self.width+"╗",curses.color_pair(color))
        
        #draw sides
        for i in range(self.height):
            scr.addstr(self.y_margin+i+1,self.x_margin,"║"+ " "*self.width+"║",curses.color_pair(color))
        
        #draw bottom border
        scr.addstr(self.y_margin + self.height+1,self.x_margin,"╚" + "═"*self.width + "╝",curses.color_pair(color))

        #if necessary, merge with border
        if self.x_margin == 0:
            scr.addstr(self.y_margin,0,"╠",curses.color_pair(color))
            scr.addstr(self.y_margin+self.height,0,"╠",curses.color_pair(color))
            scr.addstr(self.y_margin,self.width+2,"╣",curses.color_pair(color))
            scr.addstr(self.y_margin+self.height,self.width+2,"╣",curses.color_pair(color))

        if self.y_margin == 0:
            scr.addstr(0,self.x_margin,"╦",curses.color_pair(color))
            scr.addstr(0,self.x_margin + self.width+1,"╦",curses.color_pair(color))
            scr.addstr(self.height+1,self.x_margin,"╩",curses.color_pair(color))
            scr.addstr(self.height+1,self.x_margin + self.width+1,"╩",curses.color_pair(color))
        
class Widget():
    def __init__(self,lines):
        self.lines = lines
        self.identity = identify(self)
        self.focused = False

    def get_width_height(self):
        height = len(self.lines)

        max_width = 0
        for line in self.lines:
            width = len(line['label']) + len(str(line['value']))
            if width > max_width:
                max_width = width

        return (width+2,height+1)


    def draw(self,scr,x,y):
        #TODO: move this to plot.py
        #TODO: generalize drawing algorithm
        #TODO: parametrize spaces between words
        #TODO: get margins in separate function

        color = 4
        width, height = self.get_width_height()
        #Draw top border
        scr.addstr(0,width,"╦",curses.color_pair(color))
        #Draw side border
        for i in range(1,height+1):
            scr.addstr(i,width,"║",curses.color_pair(color))
        #Draw bottom border
        scr.addstr(height,0,"╠" +"═"*(width-1)+ "╝",curses.color_pair(color))
        #Draw items
        for i,line in enumerate(self.lines):
            scr.addstr(i+1,1,line['label']+str(line['value']),curses.color_pair(color))

    def update_val(self,ix,value):
        self.lines[ix]['value'] = value

    def update_all_values(self, values):
        if len(values) == len(self.lines):
            for i,val in enumerate(values):
                self.lines[i]['value'] = val
        else:
            raise(Exception('List of values to assign to widget does not match widget lines'))