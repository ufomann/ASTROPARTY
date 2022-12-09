from image import *
from constants import *

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
Also special reductions are used for special walls:
br_wall -- wall that can be broken 
'''
paths = {'yry': 'graphics/yry.png',
         'gbg': 'graphics/gbg.png',
         'o': 'graphics/o.png',
         'br_wall': 'graphics/breaking_wall.png',
         'g_wall': 'graphics/gravitating_wall.png'}


def distance(coord1: np.ndarray, coord2: np.ndarray):
    """Calculate distance between two objects"""
    return coord1[0] - coord2[0], coord1[1] - coord2[1]


class Field:
    """TODO"""
    def __init__(self, field: list,
                 field_size: list,
                 block_size_x: int,
                 block_size_y: int,
                 scale: int,
                 width: int,
                 height: int):
        self.scale = scale / 5 * min(WIDTH, HEIGHT) / (field_size[1] * block_size_x)
        self.__field = field
        self.__size = field_size
        self.__dx = block_size_x * self.scale
        self.__dy = block_size_y * self.scale
        self.__shift_x = (width - self.__size[0] * self.__dx)/2
        self.__shift_y = (height - self.__size[1] * self.__dy)/2

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
        for i in range(self.__size[0]):
            for j in range(self.__size[1]):
                if self.__field[i][j] != 0 and self.__field[i][j] != 9\
                        and self.__field[i][j] != 8 and self.__field[i][j] != 5:
                    block_coords = np.array([self.__shift_x + float(j*self.__dx) + self.__dx/2,
                                             self.__shift_y + float(i*self.__dy) + self.__dy/2])
                    neighbours = {'l': False, 'r': False, 'u': False, 'd': False}
                    # filling of dict neighbours:
                    if (j-1) >= 0:
                        if self.__field[i][j-1] != 0:
                            neighbours['l'] = True
                    if (j+1) < self.__size[1]:
                        if self.__field[i][j+1] != 0:
                            neighbours['r'] = True
                    if (i-1) >= 0:
                        if self.__field[i-1][j] != 0:
                            neighbours['u'] = True
                    if (i+1) < self.__size[0]:
                        if self.__field[i+1][j] != 0:
                            neighbours['d'] = True
                    # calculating collisions:
                    ro_x, ro_y = distance(block_coords, coords)
                    R = self.__dx / 2 + heatrad
                    if abs(ro_x) <= R and abs(ro_y) <= R:
                        # Touching from upward:
                        if ro_y > 0. and abs(ro_y) >= abs(ro_x) and (not neighbours['u']):
                            touch['u'] = True
                        # Touching from downward:
                        if ro_y < 0. and abs(ro_y) >= abs(ro_x) and (not neighbours['d']):
                            touch['d'] = True
                        # Touching from the left:
                        if ro_x > 0. and abs(ro_y) <= abs(ro_x) and (not neighbours['l']):
                            touch['l'] = True
                        # Touching from the right:
                        if ro_x < 0. and abs(ro_y) <= abs(ro_x) and (not neighbours['r']):
                            touch['r'] = True
        return touch

    def bullet_touch(self, bullet, coords: np.ndarray, velosity: np.ndarray):
        for i in range(self.__size[0]):
            for j in range(self.__size[1]):
                if self.__field[i][j] != 0 and self.__field[i][j] != 5 \
                        and self.__field[i][j] != 9 and self.__field[i][j] != 8:
                    block_coords = np.array([self.__shift_x + float(j * self.__dx) + self.__dx / 2,
                                             self.__shift_y + float(i * self.__dy) + self.__dy / 2])
                    ro_x, ro_y = distance(block_coords, coords)
                    if (ro_x**2 + ro_y**2 <= 0.5 * self.__dx ** 2) and (np.dot(np.array([ro_x, ro_y]), velosity) >= 0):
                        if self.__field[i][j] == 4:
                            self.__field[i][j] = 0
                        bullet.set_dead(True)

    def get_wall_touch(self, coords: np.ndarray, heatrad: float, velocity: np.ndarray):
        return self.__wall_touch(coords, heatrad, velocity)

    def get_new_field(self):
        return self.__field

    def get_force(self, coords):
        force = np.array([0, 0], dtype=float)
        for i in range(self.__size[0]):
            for j in range(self.__size[1]):
                if self.__field[i][j] == 5:
                    block_coords = np.array([self.__shift_x + float(j*self.__dx) + self.__dx/2,
                                             self.__shift_y + float(i*self.__dy) + self.__dy/2])
                    dist = np.dot(block_coords - coords, block_coords - coords)
                    force += -g * (block_coords - coords)/dist**2
        return force


def build_walls(field: list,
                field_size: list,
                walls: list,
                path: dict,
                block_size_x: int,
                block_size_y: int,
                scale: int):

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
    scale = scale / 5 * min(WIDTH, HEIGHT) / (field_size[1] * block_size_x)
    dx = block_size_x * scale
    dy = block_size_y * scale
    shift_x = (WIDTH - field_size[0] * dx)/2
    shift_y = (HEIGHT - field_size[1] * dy)/2
    for i in range(field_size[0]):
        for j in range(field_size[1]):
            crd = [shift_x + j * dx + dx/2, shift_y + i * dy + dy/2]
            if field[i][j] == 1:
                walls.append(Wall(crd, path['yry']))
            if field[i][j] == 2:
                walls.append(Wall(crd, path['gbg']))
            if field[i][j] == 3:
                walls.append(Wall(crd, path['o']))
            if field[i][j] == 4:
                walls.append(Wall(crd, path['br_wall']))
            if field[i][j] == 5:
                walls.append(Wall(crd, path['g_wall']))
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
        scale = scale / 5 * min(WIDTH, HEIGHT) / (field_size[1] * block_size_x)
        self.__image.draw(self.__angle, self.__coords, scale)

