import pygame 

#general constants
FPS = 60
TIME_PERIOD = 1 / FPS
SCALE = 5
WIDTH = 1200
HEIGHT = 800
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_position = 2
BLACK = 0x000000
WHITE = 0xffffff

#constants for ship
REDSHIPIMG = ["graphics/redship1.png", "graphics/redship2.png", "graphics/redship3.png"]
BLUESHIPIMG = ["graphics/blueship1.png", "graphics/blueship2.png", "graphics/blueship3.png"]
REDSHIPSTR = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_n, pygame.K_m]
BLUESHIPSTR = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_t, pygame.K_g]
MAX_SPD = 200
SCALE = 5
FORCE = 500
OMEGA = 200

#bullet constants
BULLET_SPD = 500
BULLETIMG = ["graphics/bullet.png"]

#barrier constants
