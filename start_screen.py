import pygame 

import constants as cnst
from menu_objects import *

def start_menu():
    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    bg = pygame.image.load(cnst.MENU_OBJECTSIMG[0])
    title = Title(cnst.MENU_OBJECTSIMG[4], cnst.WIDTH/24*11, cnst.HEIGHT/2)
    start = Start_button(cnst.MENU_OBJECTSIMG[1], cnst.MENU_OBJECTSIMG[2], cnst.WIDTH/2, cnst.HEIGHT/4*3)
    static_obj = [start]
    dynamic_obj = [title]
    obj_pos = 0

    while not finished:
        cnst.screen.blit(bg,(0,0))
        for obj in static_obj:
            obj.draw()
        for obj in dynamic_obj:
            obj.draw(obj_pos)
        obj_pos+=0.1

        clock.tick(cnst.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_button(static_obj, event)
        pygame.display.update()
    