from math import *
from random import *
import constants as cnst
from ship import *
from bullet import*
import numpy as np
import pygame
from barrier import *

def game(field_type1):
    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    redship = Ship(np.array([200, 200]), cnst.REDSHIPIMG, cnst.REDSHIPSTR, 0)
    blueship = Ship(np.array([cnst.WIDTH, cnst.HEIGHT]), cnst.BLUESHIPIMG, cnst.BLUESHIPSTR, 180)

    ships = [redship, blueship]

    field = Field(field_type1, field_size, block_size_x, block_size_y, SCALE)

    walls = []
    coords_red, coords_blue = build_walls(field_type1, field_size, walls, paths, block_size_x, block_size_y, SCALE)
    bullets = []

    while not finished:
        # drawing walls
        for wall in walls:
            wall.draw(SCALE)

        # movements
        for i in ships:
            i.changespd()
        for ship in ships:
            ship.set_walltouch(field.get_wall_touch(ship.get_coord(), ship.get_heatrad(), ship.get_spd()))
            print(field.get_wall_touch(ship.get_coord(), ship.get_heatrad(), ship.get_spd()))
        collision(ships)
        for i in ships:
            i.move(cnst.SCALE)
        for b in bullets:
            b.move(cnst.SCALE)
        for bullet in bullets:
            bullet.collision_with_ship(ships)
        for ship in ships:
            if (ship.get_dead()):
                ships.remove(ship)
        for bullet in bullets:
            if (bullet.get_dead()):
                bullets.remove(bullet)
        #movements 

        clock.tick(cnst.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                cnst.screen_position = 0
            if event.type == pygame.KEYDOWN:
                for ship in ships:
                    if event.key == ship.get_steer().shoot:
                        ship.shoot(bullets, cnst.SCALE)
        pygame.display.update()
        cnst.screen.fill(cnst.BLACK)
