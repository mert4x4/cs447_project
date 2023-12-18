
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
        
