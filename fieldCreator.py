import matplotlib.pyplot as plt
import numpy as np

def is_equal(a, b):
    if (len(a) != len(b)):
        return False
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

#TODO
im = plt.imread('path')
#TODO

print(type(im[0][0]))
aboba = [np.array([255, 255, 255]), np.array([0, 0, 0]), np.array([255, 0, 0]), np.array([0, 0, 255]), np.array([0, 255, 0])]
dict = {0: 0, 1: 2, 2: 4, 3: 8, 4: 9}
n = len(im)
m = len(im[0])
im2 = [[0 for i in range(m)] for i in range(n)]
for i in range(len(im2)):
    for j in range(len(im2[0])):
        for k in range(len(aboba)):
            if is_equal(im[i][j], aboba[k]):
                im2[i][j] = dict[k]
print(im2)