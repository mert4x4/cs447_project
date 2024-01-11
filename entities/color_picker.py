import pygame

class ColorPicker():
  def __init__(self, size, x_offset):
    self.size = size
    self.x_offset = x_offset
    self.colors = [(0,200,130),(0,100,130),(78,10,130)]
    self.selected_color = 0

  def draw(self,screen):
    pygame.draw.rect(screen,(0,0,0),(self.x_offset,0,self.size[0],self.size[1]),0)
    for i in range(len(self.colors)):
      if i == self.selected_color:
        pygame.draw.rect(screen,(255,255,255),(self.x_offset + 10 - 5, 10 + i * 50 - 5, self.size[0] - 20 + 10, 40 + 10),0)
        pygame.draw.rect(screen,(0,0,0),(self.x_offset + 10 - 5, 10 + i * 50 - 5, self.size[0] - 20 + 10, 40 + 10),1)
      pygame.draw.rect(screen,self.colors[i],(self.x_offset + 10, 10 + i * 50, self.size[0] - 20, 40),0)
      pygame.draw.rect(screen,(0,0,0),(self.x_offset + 10, 10 + i * 50, self.size[0] - 20, 40),1)

  
  def get_current_color(self):
    return [self.selected_color, self.colors[self.selected_color]]
  
  def check_click(self,pos):
    # Check if the mouse is over the color picker
    if pos[0] > self.x_offset and pos[0] < self.x_offset + self.size[0]:
      if pos[1] > 10 and pos[1] < 10 + len(self.colors) * 50:
        # Check which color is selected
        for i in range(len(self.colors)):
          if pos[1] > 10 + i * 50 and pos[1] < 10 + i * 50 + 40:
            self.selected_color = i
            break

    #print(self.selected_color)
    
