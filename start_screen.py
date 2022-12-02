import pygame 

import constants as cnst
from menu_buttons import *

def start_menu():
    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    bg = pygame.image.load("graphics/astro_party_fone.png")
    title = Title("graphics/screen_img.png", 550, 400)
    start = Start_button("graphics/start_button.png", "graphics/pr_start_button.png", 570, 600)
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
                cnst.screen_position = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_button(static_obj, event)
        if cnst.screen_position != 2:
            finished = True
        pygame.display.update()
    