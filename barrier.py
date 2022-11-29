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

SCALE = 5
WIDTH = 200
HEIGHT = 200
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False

#Paths to images:
'''
Generely barriers consist of several rows. Keys show what colors this rows are.
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


field_size = np.array([10, 10])
field = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 3, 0, 0, 3, 3, 0, 0, 3, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 2, 2, 2, 2, 0, 0, 1],
         [1, 0, 0, 2, 2, 2, 2, 0, 0, 1],
         [1, 0, 0, 2, 2, 2, 2, 0, 0, 1],
         [1, 0, 0, 2, 2, 2, 2, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 3, 0, 0, 3, 3, 0, 0, 3, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

class Image:
    '''TODO'''

    def __init__(self, path):
        self.__image = pygame.image.load(path).convert_alpha()
        self.__SIZE = np.array([self.__image.get_width(), self.__image.get_height()])

    def draw(self, angle, coords, scale):
        temp = pygame.transform.scale(self.__image, self.__SIZE * scale)
        temp = pygame.transform.rotate(temp, angle)
        screen.blit(temp, (coords[0] - temp.get_width() // 2, coords[1] - temp.get_height() // 2))

    def get_image(self):
        return self.__image


def build_walls(field: list, field_size: np.ndarray, walls: list, path: dict) -> list:
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
    for i in range(field_size[0]):
        for j in range(field_size[1]):
            if field[i][j] == 1:
                walls.append(Wall([i * 20 + 20/2, j * 20 + 20/2], path['yry']))
            if field[i][j] == 2:
                walls.append(Wall([i * 20 + 20/2, j * 20 + 20/2], path['gbg']))
            if field[i][j] == 3:
                walls.append(Wall([i * 20 + 20 / 2, j * 20 + 20 / 2], path['o']))

class Wall:
    '''TODO'''
    def __init__(self, coords: list, path: str, angle: float = 0):
        self.__path = path
        self.__coords = np.array(coords, dtype=float)
        self.__angle = angle
        self.__image = Image(self.__path)

    def draw(self, scale):
        self.__image.draw(self.__angle, self.__coords, scale)

walls = []
build_walls(field, field_size, walls, paths)


while not finished:
    #drawing walls
    for wall in walls:
        wall.draw(1)

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
