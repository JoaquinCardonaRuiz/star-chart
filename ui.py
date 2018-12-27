import curses
class UI():

    def __init__(self, lines, direction):
        self.lines = lines
        self.direction = direction
        self.border = self.gen_border()
        self.selected = None
        self.focused = False

    def gen_border(self):
        if self.direction in ["Left","Right"]:
            #Width is equal to the lenght of the longest item plus 2 for margins
            x = max(len(i) for i in self.lines) + 2
            y = len(self.lines)*4 + 2
        elif self.direction in ["Top","Bottom"]:
            #Width is equal to the sum of the length of all the strings...
            #plus 2 spaces between words, plus 2 for margins
            x = sum([len(i) for i in self.lines]) + len(self.lines)*2 + 3
            y = 1
        return(x,y)

    def focus(self):
        if self.direction == "Top":
            self.border = [self.border[0], 3]
        self.focused = True

    def defocus(self):
        if self.direction == "Top":
            self.border = [self.border[0], 1]
        self.focused = False

    def draw(self,scr,x,y):
        #TODO: move this to plot.py
        #TODO: generalize drawing algorithm
        #TODO: parametrize spaces between words
        #y-=1
        if self.direction == "Left":
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
                if self.selected == i:
                    color = 5
                else:
                    color = 4
                scr.addstr(margin+(i*4)+3,2,self.lines[i],curses.color_pair(color))

        if self.direction == "Right":
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
                if self.selected == i:
                    color = 5
                else:
                    color = 4
                scr.addstr(margin+(i*4)+3,x-2-len(self.lines[i]),self.lines[i],curses.color_pair(color))

        if self.direction == "Top":
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
                if self.selected == i:
                    color = 5
                else:
                    color = 4
                scr.addstr(self.border[1]//2 + 1, margin+3+shift+(2*i),self.lines[i],curses.color_pair(color))
                shift += len(self.lines[i])

        if self.direction == "Bottom":
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
                if self.selected == i:
                    color = 5
                else:
                    color = 4
                scr.addstr(y- (self.border[1]//2)-1, margin+3+shift+(2*i),self.lines[i],curses.color_pair(color))
                shift += len(self.lines[i])
        
