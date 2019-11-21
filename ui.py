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
        if not ((self.selected + n) >= len(self.lines) or (self.selected + n) < 0):
            self.selected += n

    def gen_border(self):
        #TODO: decide if fixed or variable width for l/r
        if self.direction in ["left","right"]:
            #Width is equal to the lenght of the longest item plus 2 for margins... or 13, idk anymore
            x = 13 #max(len(i) for i in self.lines) + 2
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
            margin = int((y - self.border[1])/2)
            #Draw top border
            scr.addstr(margin,0,"╠" + "═"*self.border[0] + "╗")
            #Draw side border
            for i in range(1,self.border[1]+1):
                scr.addstr(margin+i,1," "*self.border[0] + "║")
            #Draw bottom border
            scr.addstr(y-margin,0,"╠" +"═"*self.border[0] + "╝")
            #Draw items
            for i in range(len(self.lines)):
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr(margin+(i*4)+3,2,self.lines[i],curses.color_pair(color))

        if self.direction == "right":
            margin = int((y - self.border[1])/2)
            #Draw top border
            scr.addstr(margin,x - (self.border[0]+2),"╔" + "═"*self.border[0] + "╣")
            #Draw side border
            for i in range(1,self.border[1]+1):
                scr.addstr(margin+i,x - (self.border[0]+2),"║"+" "*self.border[0])
            #Draw bottom border
            scr.addstr(y-margin,x - (self.border[0]+2),"╚" + "═"*self.border[0] + "╣")
            #Draw items
            for i in range(len(self.lines)):
                if self.selected == i and self.focused:
                    color = 5
                else:
                    color = 4
                scr.addstr(margin+(i*4)+3,x-2-len(self.lines[i]),self.lines[i],curses.color_pair(color))

        if self.direction == "top":
            margin = int((x - self.border[0])/2)
            #Draw left border
            scr.addstr(0,margin,"╦")
            for i in range(self.border[1]):
                scr.addstr(1+i,margin,"║"+" "*self.border[0])
            #Draw right border
            scr.addstr(0,margin+self.border[0]+1,"╦")
            for i in range(self.border[1]):
                scr.addstr(1+i,margin+self.border[0]+1,"║")
            #Draw bottom border
            scr.addstr(self.border[1]+1 ,margin,"╚" + "═"*self.border[0] + "╝")
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
            margin = int((x - self.border[0])/2)
            #Draw left border
            try:
                scr.addstr(y,margin,"╩")
            except curses.error as e:
                pass
            for i in range(self.border[1]):
                scr.addstr(y-i-1,margin,"║"+" "*self.border[0])
            #Draw right border
            scr.addstr(y,margin+self.border[0]+1,"╩")
            for i in range(self.border[1]):
                scr.addstr(y-1-i,margin+self.border[0]+1,"║")
            #Draw top border
            scr.addstr(y-self.border[1]-1,margin,"╔" + "═"*self.border[0] + "╗")
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
            marginY = int((y - self.border[1])/2)
            marginX = int((x - self.border[0])/2)
            try:
                #Top border
                scr.addstr(marginY,marginX,"╔" + "═"*self.border[0] + "╗")
                #Bottom border
                scr.addstr(y-marginY,marginX,"╚" +"═"*self.border[0] + "╝")
                #Left Side
                for i in range(1,self.border[1]+1):
                    scr.addstr(marginY+i,marginX,"║"+" "*self.border[0])
                #Right Side
                for i in range(1,self.border[1]+1):
                    scr.addstr(marginY+i,marginX+self.border[0]+1,"║"+" "*self.border[0])
                #Draw items
                for i in range(len(self.lines)):
                    if self.selected == i and self.focused:
                        color = 5
                    else:
                        color = 4
                    scr.addstr(marginY+(i*4)+3,marginX+(self.border[0]//2)-len(self.lines[i])//2,self.lines[i],curses.color_pair(color))
            except curses.error as e:
                pass

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

    def draw(self,scr):
        width, height = self.get_size(scr)
        Window.__init__(self,width,height)

        #draw top border
        scr.addstr(self.y_margin,self.x_margin,"╔"+"═"*self.width+"╗")
        
        #draw sides
        for i in range(self.height):
            scr.addstr(self.y_margin+i+1,self.x_margin,"║"+ " "*self.width+"║")
        
        #draw bottom border
        scr.addstr(self.y_margin + self.height+1,self.x_margin,"╚" + "═"*self.width + "╝")

        #if necessary, merge with border
        if self.x_margin == 0:
            scr.addstr(self.y_margin,0,"╠")
            scr.addstr(self.y_margin+self.height,0,"╠")
            scr.addstr(self.y_margin,self.width+2,"╣")
            scr.addstr(self.y_margin+self.height,self.width+2,"╣")

        if self.y_margin == 0:
            scr.addstr(0,self.x_margin,"╦")
            scr.addstr(0,self.x_margin + self.width+1,"╦")
            scr.addstr(self.height+1,self.x_margin,"╩")
            scr.addstr(self.height+1,self.x_margin + self.width+1,"╩")
        