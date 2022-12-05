import pygame 

import constants as cnst
from menu_buttons import *

def win_screen(ship):
    """Показать экран выигрыша
    ship - индекс корабля, который побеждает
    """
    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    bg = pygame.image.load(cnst.FONEIMG[0])
    title = Title(cnst.WINIMG[ship],550, 400)

    dynamic_obj = [title]
    obj_pos = 0

    while not finished:
        cnst.screen.blit(bg,(0,0))

        for obj in dynamic_obj:
            obj.draw(obj_pos)
        obj_pos+=0.1

        clock.tick(cnst.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                cnst.screen_position = 0
        if cnst.screen_position != 2:
            finished = True
        pygame.display.update()
    