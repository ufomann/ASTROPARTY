from math import *
from random import *
import constants as cnst
from ship import *
from bullet import*
import numpy as np
import pygame

pygame.init()
cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
clock = pygame.time.Clock()
finished = False

redship = Ship(np.array([0, 0]), cnst.REDSHIPIMG, cnst.REDSHIPSTR, 0)
blueship = Ship(np.array([cnst.WIDTH, cnst.HEIGHT]), cnst.BLUESHIPIMG, cnst.BLUESHIPSTR, 180)

ships = [redship, blueship]
bullets = []

while not finished:
    #movements
    for i in ships:
        i.changespd()
    '''for i in ships:
        bounce1(i)'''
    collision(ships)
    for i in ships:
        i.move(cnst.SCALE)
    'TODO'
    #movements 

    clock.tick(cnst.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN
            for ship in ships:
                if event.key == ship.get_steer().shoot:
                    ship.shoot()
    pygame.display.update()
    cnst.screen.fill(cnst.BLACK)
pygame.quit()
