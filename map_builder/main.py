import pygame
from grid import *
from socketHandler import *

screen_size = (640, 480)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("map_builder")
clock = pygame.time.Clock()
running = True

mouse_button = 0

keys = {pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4}


def data_receive_event(received_data):
    print(received_data)

socketHandler = SocketHandler("127.0.0.1", 2000, receive_callback=data_receive_event)  # Pass the callback

def draw():
    grid.draw_grid(screen)
    pygame.display.flip()


def event_handler(e):
    global mouse_button

    if e.type == pygame.MOUSEBUTTONDOWN:
        mouse_button = e.button
        grid.check_by_click(e.pos, mouse_button)

    if e.type == pygame.MOUSEBUTTONUP:
        mouse_button = 0
        grid.check_by_click(e.pos, mouse_button)

    if e.type == pygame.MOUSEMOTION:
        grid.check_by_click(e.pos, mouse_button)

    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_s:
            print("saved")
        elif e.key == pygame.K_l:
            print("loaded")


def main():
    global grid
    global socketHandler
    grid = Grid(screen_size)
    grid.append_grid()
    socketHandler.connect()
    socketHandler.start_receive_thread()


def loop():
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            event_handler(event)

        draw()
        clock.tick(60)


def exit():
    socketHandler.close()
    pygame.quit()


if __name__ == "__main__":
    main()
    loop()
    exit()
