import pygame 

import constants as cnst
import menu_objects as mn
import active_camera as cam

def win_screen(which_ship):
    cnst.CAMERA = cam.Cam(1)
    """Показать экран выигрыша
    which_ship - индекс корабля, который побеждает:
    0 - red
    1 - blue
    2 - both
    """
    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    bg = pygame.image.load(cnst.FONEIMG[0])
    title = mn.Title(cnst.WINIMG[which_ship],cnst.WIDTH/24*11, cnst.HEIGHT/4)
    button_to_menu = mn.Back_to_menu_button(cnst.MENU_BUTTON_IMG[0], cnst.MENU_BUTTON_IMG[1], 100, 50, 0.5)
    
    ships_img = []
    if which_ship == 0:
        ships_img.append(mn.Image(cnst.REDSHIPIMG[0]))
    elif which_ship == 1:
        ships_img.append(mn.Image(cnst.BLUESHIPIMG[0]))
    else:
        ships_img.append(mn.Image(cnst.REDSHIPIMG[0]))
        ships_img.append(mn.Image(cnst.BLUESHIPIMG[0]))
    
    angle = 0

    while not finished:
        cnst.screen.blit(bg,(0,0))

        if len(ships_img) == 1:
            ships_img[0].draw(angle, [cnst.WIDTH/24*11, cnst.HEIGHT/2], 5)
        else:
            ships_img[0].draw(angle, [cnst.WIDTH/24*9, cnst.HEIGHT/2], 5)
            ships_img[1].draw(angle, [cnst.WIDTH/24*13, cnst.HEIGHT/2], 5)
        title.draw(scale=2)
        button_to_menu.draw()

        angle += 10

        clock.tick(cnst.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mn.check_button([button_to_menu], event)
        pygame.display.update()
    