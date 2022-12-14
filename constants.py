import pygame 
import numpy as np
from active_camera import *

# general constants
FPS = 60
TIME_PERIOD = 1 / FPS
WIDTH = 1200
HEIGHT = 650
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
'''screen_position =
    1 - if it's start screen
    2 - if it's game screen
    3 - if it's score screen
    4 - if it's end screen'''
BLACK = 0x000000
WHITE = 0xffffff
TIME_AFTER_END_OF_THE_ROUND = 500

# constants for ship
REDSHIPIMG = ["graphics/redship1.png", "graphics/redship2.png", "graphics/redship3.png"]
BLUESHIPIMG = ["graphics/blueship1.png", "graphics/blueship2.png", "graphics/blueship3.png"]
AMMOIMG = ["graphics/ammos.png"]
REDSHIPSTR = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_n, pygame.K_m, pygame.K_b]
BLUESHIPSTR = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_t, pygame.K_g, pygame.K_r]
MAX_SPD = 100
FORCE = 500
OMEGA = 200
RELOADTIME = 1000
OMEGAFORAMMO = 120
SHIELDIMG = ["graphics/shield.png", "graphics/void.png"]
INVINCIBLE = 2000

# bullet constants
BULLET_SPD = 200
BULLETIMG = ["graphics/bullet.png"]

# barrier constants

g = 100000000.
field_size = [20, 20]
block_size_x = 20.
block_size_y = 20.

# menu constants
MENU_OBJECTSIMG = [
    "graphics/astro_party_fone.png", 
    "graphics/start_button.png", 
    "graphics/pr_start_button.png",
    "graphics/credits_button.png", 
    "graphics/screen_img.png"
    ]

# score screen constants
SCORETOWIN = 2
SCORE = dict(blueship=0, redship=0)
SCORELINEIMG = ['graphics/score_count_line.png']
BLUECOORDSONSCORELINE = np.array([0, 0])
REDCOORDSONSCORELINE = np.array([HEIGHT, 0])
SCORELINESCALE = 4
TIMEFORMOVE = 1

# win_screen constants
WINIMG = ["graphics/red_win.png", "graphics/blue_win.png", "graphics/draw.png"]
MENU_BUTTON_IMG = ["graphics/menu_button.png", "graphics/pr_menu_button.png"]
FONEIMG = ["graphics/win_fone.png"]

# bomb constants
BOMBIMG = ["graphics/bomb.png"]

# animation constants
PPS = 3

#active camera constants
CAMERA = Cam(1)
SCALE = min(WIDTH, HEIGHT) / (field_size[1] * block_size_x)
MAXSCALE = 5
MINSCALE = min(WIDTH, HEIGHT) / (field_size[1] * block_size_x)
BORDER = WIDTH / 6
SCALE_SPD = 0.00001