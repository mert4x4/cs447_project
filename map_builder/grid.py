import pygame

class Rectangle():
    def __init__(self,x,y,color,gridlen):
        self.x = x
        self.y = y
        self.color = color
        self.gridlen = gridlen
        self.real_x = self.x*gridlen
        self.real_y = self.y*gridlen
        self.checked = -1
        self.color = (0,200,130)

    def check(self,color_id):
        self.checked = color_id

    def set_color(self,color):
        self.color = color

    def uncheck(self):
        self.color = (255,255,255)
        self.checked = -1
        

class Grid():
    def __init__(self,screen_size):
        self.rectangles = []
        self.gridlen = 20
        self.screen_size = screen_size
        self.colors = [(0,200,130),(0,100,130),(78,10,130)]
        self.selected_color = 0

    def append_grid(self):
        x_ = self.screen_size[0]/self.gridlen
        y_ = self.screen_size[1]/self.gridlen
        for x in range(0,int(x_)):
            for y in range(0,int(y_)):
                self.rectangles.append(Rectangle(x,y,(255,255,255),self.gridlen))

    def draw_grid(self,screen):
        for rect in self.rectangles:
            pygame.draw.rect(screen,rect.color,(rect.real_x,rect.real_y,self.gridlen,self.gridlen),0)
            pygame.draw.rect(screen,(0,0,0),(rect.real_x,rect.real_y,self.gridlen,self.gridlen),1)

    def check_by_click(self,pos,button):
        for rect in self.rectangles:
            if(pos[0]//self.gridlen == rect.x and pos[1]//self.gridlen == rect.y):
                rect.set_color(self.colors[self.selected_color])
                if button == 1:
                    rect.check(self.selected_color)
                elif button == 2:
                    print(rect.x,rect.y)
                elif button == 3:
                    rect.uncheck()

    def check_by_grid_coordinate(self,x,y,button,selected_color):
        for rect in self.rectangles:
            if(x == rect.x and y == rect.y):
                rect.set_color(self.colors[selected_color])
                if button == 1:
                    rect.check(selected_color)
                elif button == 3:
                    rect.uncheck()


    def mouse_coordinate_to_grid_coordinate(self,pos):
        return (pos[0]//self.gridlen, pos[1]//self.gridlen)
    

    def get_checked_array(self):
        array = []
        for i in self.rectangles:
            array.append(i.checked)
        return array


    def reset(self):
        self.rectangles = []
        self.append_grid()
    
    def load_checked(self,array):
        for i in range(len(self.rectangles)):
            if array[i] != -1:
                self.rectangles[i].set_color(self.colors[array[i]])
                self.rectangles[i].check(i)
            else:
                self.rectangles[i].set_color((255,255,255))
                self.rectangles[i].uncheck()