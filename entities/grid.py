from .rectangle import Rectangle
import pygame

class Grid():
    def __init__(self,screen_size):
        self.rectangles = []
        self.gridlen = 20
        self.screen_size = screen_size

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

    def check_by_click(self,pos,button, color_id, color):
        for rect in self.rectangles:
            if(pos[0]//self.gridlen == rect.x and pos[1]//self.gridlen == rect.y):
                rect.set_color(color)
                if button == 1:
                    rect.check(color_id)
                elif button == 2:
                    print(rect.x,rect.y)
                elif button == 3:
                    rect.uncheck()

    def check_by_grid_coordinate(self,x,y,button, color_id, colors):
        for rect in self.rectangles:
            if(x == rect.x and y == rect.y):
                rect.set_color(colors[color_id])
                if button == 1:
                    rect.check(color_id)
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
    
    def load_checked(self,array,colors):
        for i in range(len(self.rectangles)):
            if array[i] != -1:
                self.rectangles[i].set_color(colors[array[i]])
                self.rectangles[i].check(i)
            else:
                self.rectangles[i].set_color((255,255,255))
                self.rectangles[i].uncheck()