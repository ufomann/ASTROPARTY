import numpy as np
import pygame
from image import *
from constants import *


#field_size = [10, 10]
#block_size_x = 20
#block_size_y = 20
# intrinsic scaling coefficient, it rescales field from "template" field to working one
SCALE = SCALE/5 * min(WIDTH, HEIGHT) // (field_size[1] * block_size_x)

clock = pygame.time.Clock()
finished = False

# Paths to images:
'''
Generally barriers consist of several rows. Keys show what colors this rows are.
reductions used:
o -- orange
y -- yellow
g -- green
b -- blue
w -- white
r -- red
'''
paths = {'yry': 'graphics/yry.png',
         'gbg': 'graphics/gbg.png',
         'o': 'graphics/o.png'}


def distance(coord1: np.ndarray, coord2: np.ndarray):
    """Calculate distance between two objects"""
    return np.dot(coord1 - coord2, coord1 - coord2)**0.5


class Field:
    """TODO"""
    def __init__(self, field: list,
                 field_size: list,
                 block_size_x: int,
                 block_size_y: int,
                 scale: int,
                 width: int,
                 height: int):
        self.field = field
        self.size = field_size
        self.dx = block_size_x * scale
        self.dy = block_size_y * scale
        self.shift_x = (width - min(width, height))/2
        self.shift_y = (height - min(width, height))/2

    def __wall_touch(self, coords: np.ndarray, heatrad: float, velocity: np.ndarray):
        """Checks touching with walls
        returns dictionary with bool value:
        'l' -- touching from left
        'r' -- touching from right
        'u' -- touching from upward
        'd' -- touching from downward

        Important comment:
        1) object can possibly touch many walls, but we don't care if it touches more
        than one wall from each direction.
        2) dictionary 'neighbours' provides opportunity to the ship to travel along wall without stopping. It contains
        information about blocks nearby.
        """
        velocity_x = velocity[0]
        velocity_y = velocity[1]
        touch = {'l': False, 'r': False, 'u': False, 'd': False}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.field[i][j] != 0:
                    block_coords = np.array([float(j*self.dx) + self.dx/2, float(i*self.dy) + self.dy/2])
                    neighbours = {'l': False, 'r': False, 'u': False, 'd': False}
                    # filling of dict neighbours:
                    if (j-1) >= 0:
                        if self.field[i][j-1] != 0:
                            neighbours['l'] = True
                    if (j+1) < self.size[1]:
                        if self.field[i][j+1] != 0:
                            neighbours['r'] = True
                    if (i-1) >= 0:
                        if self.field[i-1][j] != 0:
                            neighbours['u'] = True
                    if (i+1) < self.size[0]:
                        if self.field[i+1][j] != 0:
                            neighbours['d'] = True
                    # calculating collisions:
                    if distance(coords, block_coords) < (heatrad + np.sqrt(self.dx**2 + self.dy**2)):
                        # Touching from upward:
                        if velocity_y > 0. and 0. < (block_coords[1] - coords[1]) < (self.dy / 2 + heatrad) \
                                and (not neighbours['u']):
                            touch['u'] = True
                        # Touching from downward:
                        if velocity_y < 0. and 0. < (coords[1] - block_coords[1]) < (self.dy / 2 + heatrad) \
                                and (not neighbours['d']):
                            touch['d'] = True
                        # Touching from the left:
                        if velocity_x > 0. and 0. < (block_coords[0] - coords[0]) < (self.dx / 2 + heatrad) \
                                and (not neighbours['l']):
                            touch['l'] = True
                        # Touching from the right:
                        if velocity_x < 0. and 0. < (coords[0] - block_coords[0]) < (self.dx / 2 + heatrad) \
                                and (not neighbours['r']):
                            touch['r'] = True
        return touch

    def get_wall_touch(self, coords: np.ndarray, heatrad: float, velocity: np.ndarray):
        return self.__wall_touch(coords, heatrad, velocity)


def build_walls(field: list,
                field_size: list,
                walls: list,
                path: dict,
                block_size_x: int,
                block_size_y: int,
                scale: int) -> list:

    """Useing field-map like    1111
                                1001
                                1111
       define walls by init of class wall
       numeric codes for walls:
       0 --> no wall
       1 --> yellow-red-yellow wall
       2 --> green-blue-green wall
       3 --> orange wall
    """
    dx = block_size_x * scale
    dy = block_size_y * scale
    shift_x = (WIDTH - min(WIDTH, HEIGHT))/2
    shift_y = (HEIGHT - min(WIDTH, HEIGHT))/2
    for i in range(field_size[0]):
        for j in range(field_size[1]):
            #crd = [shift_x + i * dx + dx/2, shift_y + j * dy + dy/2]
            crd = [i * dx + dx/2, j * dy + dy/2]
            if field[i][j] == 1:
                walls.append(Wall(crd, path['yry']))
            if field[i][j] == 2:
                walls.append(Wall(crd, path['gbg']))
            if field[i][j] == 3:
                walls.append(Wall(crd, path['o']))
            if field[i][j] == 9:
                coords_red = np.array(crd)
            if field[i][j] == 8:
                coords_blue = np.array(crd)
    return coords_red, coords_blue


class Wall:
    """Class of barriers, it has the following attributes:
    1)__path -- string of path to the wall picture                                       type: str
    2)__coords -- coordinates of the wall block (default coordinate system)              type: numpy.array
    3)__image -- wall's image (check class Image description)                            type: calss Image
    4)__angle -- angle between 0x and ships direction (positive direction - clockwise)   type: float

    Methods:
    1) draw -- draws block on a screen
    """
    def __init__(self, coords: list, path: str, angle: float = 0):
        self.__path = path
        self.__coords = np.array(coords, dtype=float)
        self.__angle = angle
        self.__image = Image(self.__path)

    def draw(self, scale):
        self.__image.draw(self.__angle, self.__coords, scale)


field_type1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 3, 3, 0, 0, 3, 1],
               [1, 0, 9, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 8, 0, 1],
               [1, 3, 0, 0, 3, 3, 0, 0, 0, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


'''
while not finished:
    # drawing walls
    for wall in walls:
        wall.draw(SCALE)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
'''