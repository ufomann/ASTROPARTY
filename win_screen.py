import pygame 

import constants as cnst
from menu_objects import *

def win_screen(which_ship):
    """Показать экран выигрыша
    which_ship - индекс корабля, который побеждает:
    0 - red
    1 - blue
    """
    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    bg = pygame.image.load(cnst.FONEIMG[0])
    title = Title(cnst.WINIMG[which_ship],550, 200)
    button_to_menu = Back_to_menu_button(cnst.MENU_BUTTON_IMG[0], cnst.MENU_BUTTON_IMG[1], 100, 50, 0.5)

    while not finished:
        cnst.screen.blit(bg,(0,0))

        title.draw()
        button_to_menu.draw()

        clock.tick(cnst.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                cnst.screen_position = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                check_button([button_to_menu], event)
        if cnst.screen_position != 4:
            finished = True
        pygame.display.update()
    