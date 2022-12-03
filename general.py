import numpy as np
from math import *

def radius_vector(obj1, obj2):
    '''return radius vector from obj1 to obj2
        obj1 -----> obj2'''
    return obj2.get_coord() - obj1.get_coord()

def vec_len(vec):
    return np.dot(vec, vec)**0.5

def ed_vec(angle):
    return np.array([np.cos(radians(angle)), np.sin(radians(angle))])

def collisionCheck(obj1, obj2):
    '''checks if there is collizion between obj1 and obj2'''
    rad_vec = radius_vector(obj1, obj2)
    dist = vec_len(rad_vec)
    if (dist > obj1.get_heatrad() + obj2.get_heatrad()):
        return False
    return True

def arr(a, b):
    return np.array([a, b])

def signum(a):
    if a == 0:
        return a
    return a / abs(a)