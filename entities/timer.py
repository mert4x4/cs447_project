import pygame
from datetime import datetime

class Timer():
    def __init__(self):
        self.timer = 0
        self.set_at = datetime.now()
        pass

    def set_timer(self, time):
        self.timer = time
        self.set_at = datetime.now()

    def update(self):
        now = datetime.now()
        delta = now - self.set_at
        self.timer -= delta.total_seconds()
        self.set_at = now

    def draw(self, screen):
        if self.timer < 0:
            return
        pygame.font.init()
        font = pygame.font.Font(None, 20)  
        text_color = (255, 255, 255) 
        text = f"You have to wait {int(self.timer)} seconds"
        timer_text = font.render(text, True, text_color)
        screen.blit(timer_text, (screen.get_width() - timer_text.get_width() - 10, screen.get_height() - timer_text.get_height() - 10))
  
