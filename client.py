import pygame
from entities.grid import Grid
from entities.color_picker import ColorPicker
from socketHandler import *
from datetime import datetime
import re

check_mes = "you have to"

printData =""


init_data_chunks = {'init1': "", 'init2': "", 'init3': "", 'init4': "", 'init5': "", 'init6': "", 'init7': "", 'init8': "", 'init9': "", 'init10': "", 'init11': "", 'init12': ""}

def data_receive_event(received_data, grid, color_picker):
    global printData

    if check_mes in received_data:
        printData = received_data
    else:
        printData = ""

    if 'click' in received_data:
        data = received_data.split(';')
        grid.check_by_grid_coordinate(int(data[2]), int(data[3]), int(data[1]), int(data[4]), color_picker.colors)

    if 'init' in received_data:
        data_parts = received_data.split(';')
        init_key = data_parts[0]

        if init_key in init_data_chunks:
            init_data_chunks[init_key] += ''.join(data_parts[1:])

        if 'init_end' in received_data:
            complete_init_data = ''.join(init_data_chunks.values())
            complete_init_data = complete_init_data.replace('init10', '').replace('init11', '').replace('init12', '')
            complete_init_data = re.sub(r'init\d', '', complete_init_data)
            final_data = [int(x) for x in re.findall(r'-?\d+', complete_init_data)]
            print(complete_init_data)            
            grid.load_checked(final_data, color_picker.colors)

            for key in init_data_chunks:
                init_data_chunks[key] = ""


def draw_received_data(screen, received_data):
    pygame.font.init()
    font = pygame.font.Font(None, 20)  
    text_color = (255, 255, 255) 
    received_data_text = font.render(received_data, True, text_color)
    screen.blit(received_data_text, (screen.get_width() - received_data_text.get_width() - 10, screen.get_height() - received_data_text.get_height() - 10))


def draw(grid, color_picker, screen, received_data):
    grid.draw_grid(screen)
    color_picker.draw(screen)
    draw_received_data(screen, received_data) 
    pygame.display.flip()

def event_handler(e, grid, color_picker, socketHandler):
    mouse_button = 0

    if e.type == pygame.MOUSEBUTTONDOWN:
        mouse_button = e.button
        color_picker.check_click(e.pos)
        color_id, color = color_picker.get_current_color()
        #grid.check_by_click(e.pos, mouse_button, color_id, color)
        socketHandler.send_message('click;'+ str(mouse_button)+ ';' + str(grid.mouse_coordinate_to_grid_coordinate(e.pos)[0]) + ';' +str(grid.mouse_coordinate_to_grid_coordinate(e.pos)[1]) + ';' + str(color_id) + ";"+ datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if e.type == pygame.KEYDOWN:
        keys =[pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4]
        for i in range(len(keys) - 1):
            if e.key == keys[i]:
                if i <= len(grid.colors) - 1: 
                    grid.selected_color = i

def main():
    screen_size = (840, 480)
    grid_size = (640, 480)
    color_picker_size = (200, 480)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("map_builder")
    clock = pygame.time.Clock()
    running = True

    grid = Grid(grid_size)
    grid.append_grid()
    color_picker = ColorPicker(color_picker_size, grid_size[0])
    socketHandler = SocketHandler("34.125.100.23", 2000, receive_callback=lambda data: data_receive_event(data, grid, color_picker))

    socketHandler.connect()
    socketHandler.start_receive_thread()

    while running:
        global printData
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            event_handler(event, grid, color_picker, socketHandler)
                
        draw(grid, color_picker, screen, printData)
        clock.tick(60)

    socketHandler.close()
    pygame.quit()

if __name__ == "__main__":
    main()
