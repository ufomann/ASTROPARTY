import numpy as np
from math import *

def vec_len(vec):
    return np.dot(vec, vec)**0.5

def ed_vec(angle):
    return np.array([np.cos(radians(angle)), np.sin(radians(angle))])
