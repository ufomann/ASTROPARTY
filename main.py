from math import *
from random import *
import constants as cnst
from ship import *
from bullet import*
from barrier import *
import numpy as np
import pygame

pygame.init()
cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
clock = pygame.time.Clock()
finished = False

ships = []
bullets = []

while not finished:
    #movements
    """for i in ships:
        i.changespd()
    for i in ships:
        bounce1(i)
    collizion(ships)
    for i in ships:
        i.move(SCALE)"""
    'TODO'
    #movements

    clock.tick(cnst.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(cnst.BLACK)

pygame.quit()
