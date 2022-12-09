from math import *
from random import *
import constants as cnst
from ship import *
from bullet import*
import numpy as np
import pygame
from barrier import *
from constants import *
from score_count import *
from bomb import *

def game():
    field_type1 = CURRFIELD

    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    redship = Ship(np.array([200, 200]), cnst.REDSHIPIMG, cnst.REDSHIPSTR, 0, 'red')
    blueship = Ship(np.array([cnst.WIDTH, cnst.HEIGHT]), cnst.BLUESHIPIMG, cnst.BLUESHIPSTR, 180, 'blue')

    ships = [redship, blueship]

    field = Field(field_type1, field_size, block_size_x, block_size_y, SCALE, WIDTH, HEIGHT)

    walls = []
    coords_red, coords_blue = build_walls(field_type1, field_size, walls, paths, block_size_x, block_size_y, SCALE)
    redship.set_coord(coords_red)
    blueship.set_coord(coords_blue)
    bullets = []
    endtime = -1
    
    while not finished:
        # drawing walls
        walls = []
        build_walls(field.get_new_field(), field_size, walls, paths, block_size_x, block_size_y, SCALE)
        for wall in walls:
            wall.draw(SCALE)
        # movements
        for ship in ships:
            ship.set_extForce(field.get_force(ship.get_coord()))
            ship.changespd()
        for ship in ships:
            ship.set_walltouch(field.get_wall_touch(ship.get_coord(), ship.get_heatrad(), ship.get_spd()))
        collision(ships)
        for i in ships:
            i.move(cnst.SCALE)
        for b in bullets:
            b.set_extForce(field.get_force(b.get_coord()))
            b.changespd()
        for b in bullets:
            b.move(cnst.SCALE)
        for bullet in bullets:
            bullet.collision_with_ship(ships)
            field.bullet_touch(bullet, bullet.get_coord(), bullet.get_spd())
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
                exit()
            if event.type == pygame.KEYDOWN:
                for ship in ships:
                    if event.key == ship.get_steer().shoot:
                        ship.shoot(bullets, cnst.SCALE)
            if len(ships) < 2 and endtime == -1:
                endtime = pygame.time.get_ticks()
            if endtime != -1 and ((pygame.time.get_ticks() - endtime) > TIME_AFTER_END_OF_THE_ROUND):
                if len(ships) == 0:
                    score_line(0, 0)
                elif ships[0].get_id() == 'red':
                    score_line(1, 0)
                else:
                    score_line(0, 1)
        pygame.display.update()
        cnst.screen.fill(cnst.BLACK)
