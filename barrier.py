import numpy as np
import pygame


FPS = 60
TIME_PERIOD = 1 / FPS
BLACK = 0x000000

WIDTH = 400
HEIGHT = 400
field_size = [10, 10]
block_size_x = 20
block_size_y = 20
# global scaling coefficient
SCALE = 1
# intrinsic scaling coefficient, it rescales field from "template" field to working one
scale_par = WIDTH // (field_size[1] * block_size_x)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    def __init__(self, field: list, field_size: list, block_size_x: int, block_size_y: int, scale: int):
        self.field = field
        self.size = field_size
        self.dx = block_size_x * scale
        self.dy = block_size_y * scale

    def __wall_touch(self, coords: np.ndarray, heatrad: float, velocity_x: float, velocity_y: float):
        """Checks touching with walls
        returns dictionary with bool value:
        'l' -- touching from left
        'r' -- touching from right
        'u' -- touching from upward
        'd' -- touching from downward

        Important comment: object can possibly touch many walls, but we don't care if it touches more
        than one wall from each direction.
        """
        touch = {'l': False, 'r': False, 'u': False, 'd': False}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.field[i][j] != 0:
                    block_coords = np.array([float(j*self.dx) + self.dx/2, float(i*self.dy) + self.dy/2])
                    if distance(coords, block_coords) < (heatrad + np.sqrt(self.dx**2 + self.dy**2)):
                        # Touching from upward:
                        if velocity_y > 0. and 0. < (block_coords[1] - coords[1]) < (self.dy / 2 + heatrad):
                            touch['u'] = True
                        # Touching from downward:
                        if velocity_y < 0. and 0. < (coords[1] - block_coords[1]) < (self.dy / 2 + heatrad):
                            touch['d'] = True
                        # Touching from the left:
                        if velocity_x > 0. and 0. < (block_coords[0] - coords[0]) < (self.dx / 2 + heatrad):
                            touch['l'] = True
                        # Touching from the right:
                        if velocity_x < 0. and 0. < (coords[0] - block_coords[0]) < (self.dx / 2 + heatrad):
                            touch['r'] = True
        return touch

    def get_wall_touch(self, coords: np.ndarray, heatrad: float, velocity_x: float, velocity_y: float):
        return self.__wall_touch(coords, heatrad, velocity_x, velocity_y)


class Image:
    """TODO"""

    def __init__(self, path):
        self.__image = pygame.image.load(path).convert_alpha()
        self.__SIZE = np.array([self.__image.get_width(), self.__image.get_height()])

    def draw(self, angle, coords, scale):
        temp = pygame.transform.scale(self.__image, self.__SIZE * scale)
        temp = pygame.transform.rotate(temp, angle)
        screen.blit(temp, (coords[0] - temp.get_width() // 2, coords[1] - temp.get_height() // 2))

    def get_image(self):
        return self.__image


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
    for i in range(field_size[0]):
        for j in range(field_size[1]):
            if field[i][j] == 1:
                walls.append(Wall([i * dx + dx/2, j * dy + dy/2], path['yry']))
            if field[i][j] == 2:
                walls.append(Wall([i * dx + dx/2, j * dy + dy/2], path['gbg']))
            if field[i][j] == 3:
                walls.append(Wall([i * dx + dx / 2, j * dy + dy / 2], path['o']))


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
               [1, 3, 0, 0, 3, 3, 0, 0, 3, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 3, 0, 0, 3, 3, 0, 0, 3, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
field_size = [10, 10]
block_size_x = 20
block_size_y = 20

field = Field(field_type1, field_size, block_size_x, block_size_y, scale_par)

walls = []
build_walls(field_type1, field_size, walls, paths, block_size_x, block_size_y, scale_par)

while not finished:
    # drawing walls
    for wall in walls:
        wall.draw(SCALE * scale_par)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
