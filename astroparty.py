from math import *
from random import *
import numpy as np
import pygame

FPS = 60
TIME_PERIOD = 1 / FPS
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BLACK = 0x000000
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WIDTH = 1200
HEIGHT = 800
REDSHIPIMG = ["graphics/redship1.png", "graphics/redship2.png", "graphics/redship3.png"]
BLUESHIPIMG = ["graphics/blueship1.png", "graphics/blueship2.png", "graphics/blueship3.png"]
BULLETIMG = ["bullet.png"]

REDSHIPSTR = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_n, pygame.K_m]
BLUESHIPSTR = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_t, pygame.K_g]
MAX_SPD = 200
BULLET_SPD = 300
SCALE = 5
FORCE = 500
OMEGA = 200

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

def vec_len(vec):
    return np.dot(vec, vec)**0.5

def ed_vec(angle):
    return np.array([np.cos(radians(angle)), np.sin(radians(angle))])

def bounce1(ship):
    '''calculates colision between ship and wall'''
    spd = ship.get_spd()
    new_spd = spd
    if (ship.get_coord()[0] < ship.get_rad()) and spd[0] < 0:
        new_spd[0] = 0
    if (ship.get_coord()[0] > WIDTH - ship.get_rad()) and spd[0] > 0:
        new_spd[0] = 0
    if (ship.get_coord()[1] < ship.get_rad()) and spd[1] < 0:
        new_spd[1] = 0
    if (ship.get_coord()[1] > HEIGHT - ship.get_rad()) and spd[1] > 0:
        new_spd[1] = 0
    ship.set_spd(new_spd)

def radius_vector(obj1, obj2):
    '''return radius vector from obj1 to obj2
        obj1 -----> obj2'''
    return obj2.get_coord() - obj1.get_coord()

def collizionCheck(obj1, obj2):
    '''checks if there is collizion between obj1 and obj2'''
    rad_vec = radius_vector(obj1, obj2)
    dist = vec_len(rad_vec)
    if (dist > obj1.get_rad() + obj2.get_rad()):
        return False
    return True

def center_mass_speed(ship1, ship2):
    """mass of each ship is 1"""
    return (ship1.get_spd() + ship2.get_spd()) / 2

def wall_touch_check(ship):
    '''returns boolean dict:
        x0 = True - if x = 0
        y0 = True - if y = 0
        xm = True - if x = Width
        ym = True - if y = height'''
    ans = dict()
    ans['x0'] = ans['y0'] = ans['xm'] = ans['ym'] = False
    if (ship.get_coord()[0] < ship.get_rad()):
        ans['x0'] = True
    if (ship.get_coord()[0] > WIDTH - ship.get_rad()):
        ans['xm'] = True
    if (ship.get_coord()[1] < ship.get_rad()):
        ans['y0'] = True
    if (ship.get_coord()[1] > HEIGHT - ship.get_rad()):
        ans['ym'] = True
    return ans

def collizion(ships):
    '''calculates collisions between every pair of ships'''
    for i in range(len(ships)):
        for j in range(i + 1, len(ships)):
            if (collizionCheck(ships[i], ships[j])):
                vcm = center_mass_speed(ships[i], ships[j]) #calculate center mass
                if (np.dot(ships[i].get_spd() - vcm, radius_vector(ships[i], ships[j])) > 0): #if ships move towards each other
                    #velocities in frame of reference of center mass
                    v1cm = ships[i].get_spd() - vcm
                    v2cm = ships[j].get_spd() - vcm
                    #getting vectors with len = 1 pointing from ship1 to ship2 and opposite
                    erv1 = radius_vector(ships[i], ships[j])/vec_len(radius_vector(ships[i], ships[j]))
                    erv2 = -erv1
                    #getting speed components (n and t)
                    v1cmt = np.dot(v1cm, erv1) * erv1
                    v1cmn = v1cm - v1cmt
                    v2cmt = np.dot(v2cm, erv2) * erv2
                    v2cmn = v2cm - v2cmt
                    vcmt = (v1cmt + v2cmt) / 2
                    v1 = v1cmn + vcmt + vcm
                    v2 = v2cmn + vcmt + vcm
                    iftouches1 = wall_touch_check(ships[i])
                    iftouches2 = wall_touch_check(ships[j])
                    #moving through the ship, which touches the wall is prohibited
                    if (iftouches1['x0'] or iftouches2['x0']):
                        v1[0] = max(v1[0], 0)
                        v2[0] = max(v2[0], 0)
                    if (iftouches1['y0'] or iftouches2['y0']):
                        v1[1] = max(v1[1], 0)
                        v2[1] = max(v2[1], 0)
                    if (iftouches1['xm'] or iftouches2['xm']):
                        v1[0] = min(v1[0], 0)
                        v2[0] = min(v2[0], 0)
                    if (iftouches1['ym'] or iftouches2['ym']):
                        v1[1] = min(v1[1], 0)
                        v2[1] = min(v2[1], 0)
                    ships[i].set_spd(v1)
                    ships[j].set_spd(v2)

class Steering:
    '''TODO'''
    def __init__(self, buttons):
        self.up = buttons[0]
        self.down = buttons[1]
        self.conterclockwise = buttons[2]
        self.clockwise = buttons[3]
        self.shoot = buttons[4]
        self.ulta = buttons[5]

class Image:
    '''TODO'''
    def __init__(self, path):
        self.__image = pygame.image.load(path).convert_alpha()
        self.__SIZE = np.array([self.__image.get_width(), self.__image.get_height()])

    def draw(self, angle, coords, scale):
        temp = pygame.transform.scale(self.__image, self.__SIZE * scale)
        temp = pygame.transform.rotate(temp, angle)
        screen.blit(temp, (coords[0] -temp.get_width() // 2, coords[1] -temp.get_height() // 2))
    
    def get_image(self):
        return self.__image

class Ship:
    """this is ship class, it has the following atributes and methods:
    1)all atributes are protected, so to access them we have setters and getters
    2)__paths - list of paths to ship's pictures.                                       type: str
    3)__coords - coordinates of the ship (default coordinate system)                    type: numpy.array
    4)__angle - angle between 0x and ships direction (positive direction - clockwise)   type: float
    5)__spd - velocity of the ship                                                      type: numpy.array
    6)__force - force vector                                                            type: numpy.array
    7)__steer - steering buttons (check class Steering description)                     type: class Steering   
    8)__image - ship's image (check class Image description)                            type: calss Image
    9)__heatrad - ship's heatbox is circle and this is it's radius                      type: float
    """
    def __init__(self, coords, paths, steering):
        self.__paths = paths
        self.__coords = np.array(coords, dtype=float)
        self.__angle = 0
        self.__force = ed_vec(0) * 0
        self.__steer = Steering(steering)
        self.__spd = np.array([0, 0], dtype=float)
        self.__image = Image(self.__paths[0])
        self.__heatrad = 0

    def __normSpd(self):
        '''ships can't move faster than MAX_SPD'''
        if (vec_len(self.__spd) >=  MAX_SPD):
            self.__spd = self.__spd / vec_len(self.__spd) * MAX_SPD 

    def changespd(self):
        '''this function is for changing ship's velocity according to player's actions'''
        keystatus = pygame.key.get_pressed()
        if keystatus[self.__steer.conterclockwise]:
            #decrease angle if player spinning conterclockwise
            self.__angle -= OMEGA * TIME_PERIOD
        if keystatus[self.__steer.clockwise]:
            #increase angle if player spinning clockwise
            self.__angle += OMEGA * TIME_PERIOD
        self.__force = ed_vec(self.__angle) * FORCE
        self.__spd += self.__force * TIME_PERIOD
        self.__normSpd()

    def move(self, scale):
        self.__coords += self.__spd * TIME_PERIOD
        self.__heatrad = self.__image.get_image().get_width() // 2 * scale * 1
        self.__image.draw(-self.__angle - 90, self.__coords, scale)

    def shoot(self):
        bulcrd = self.get_coord()
        bullets.append(Bullet())

    def get_spd(self):
        return self.__spd
    
    def get_coord(self):
        return self.__coords
    
    def get_rad(self):
        return self.__heatrad
    
    def set_spd(self, spd):
        self.__spd = spd

class Bullet:

    def __init__(self, coords, spd, paths):   
        self.__paths = paths
        self.__coords = coords
        self.__spd = spd + spd / vec_len(spd) * BULLET_SPD
        self.__force = np.array([0, 0])
        self.__image = Image(BULLETIMG[0])
        self.__heatrad = 0
        self.__angle = 0

    def move(self, scale):
        self.__spd += self.__force * TIME_PERIOD
        self.__coords += self.__spd * TIME_PERIOD
        self.__heatrad = self.__image.get_image().get_width() // 2 * scale * 1
        self.__image.draw(-self.__angle - 90, self.__coords, scale)

    def get_spd(self):
        return self.__spd
    
    def set_spd(self, spd):
        self.__spd = spd
    
    def get_coords(self):
        return self.__coords
    


redship = Ship([200, 200], REDSHIPIMG, REDSHIPSTR)
blueship = Ship([200, 200], BLUESHIPIMG, BLUESHIPSTR)
ships = [redship, blueship]
bullets = []

while not finished:
    #movements
    for i in ships:
        i.changespd()
    for i in ships:
        bounce1(i)
    collizion(ships)
    for i in ships:
        i.move(SCALE)
    #movements

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
