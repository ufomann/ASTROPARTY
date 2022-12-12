import matplotlib.pyplot as plt
import numpy as np
from constants import field_size
from fields import fields


def is_equal(a, b):
    """Checks equality of lists"""
    if len(a) != len(b):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def input_interface():
    """Interface for field creator"""
    instructions = '''
    Welcome to the Field Creator!\n
    1)You need to draw a picture 20 x 20 pixels (for example in Paint).\n
    2) Use folowing colors to identify blocks:\n
    (255, 255, 255) for empty space\n
    (255, 255, 0) for yellow wall\n
    (0, 255, 0) for green wall\n
    (255, 136, 0) for orange wall\n
    (0, 100, 0) for braking wall\n
    (0, 0, 255) for gravitating wall\n
    (255, 0, 255) and (0, 0, 0) for spawn points\n
    3)Save picture as 'name.bmp' and put it into folder 'graphics'.\n
    4)wright name of the picture without type (example: my_picture.bmp --> my_picture)\n
    Waiting for picture's name:\n
    '''
    print(instructions)
    name = input()
    image = plt.imread('graphics/' + name + '.bmp')
    if len(image) != field_size[0] or len(image[0]) != field_size[1]:
        print('Your field is not 20 x 20 pixels!')
    return image


def make_field(image):
    """Makes field from the picture"""
    color_keys = [np.array([255, 255, 255]), np.array([255, 255, 0]),
                  np.array([0, 255, 0]), np.array([255, 136, 0]),
                  np.array([0, 100, 0]), np.array([0, 0, 255]),
                  np.array([255, 0, 255]), np.array([0, 0, 0])]
    blocks = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9}
    field = [[0 for i in range(field_size[1])] for j in range(field_size[0])]
    for i in range(field_size[0]):
        for j in range(field_size[1]):
            for k in range(len(color_keys)):
                if is_equal(image[i][j], color_keys[k]):
                    field[i][j] = blocks[k]
    print(field)




im = input_interface()
make_field(im)
