import numpy as np
import constants as cnst
import pygame

class Image:
    '''TODO'''
    def __init__(self, path):
        self.__image = pygame.image.load(path).convert_alpha()
        self.__SIZE = np.array([self.__image.get_width(), self.__image.get_height()])

    def draw(self, angle, coords, scale):
        crd = cnst.CAMERA.transform(coords)
        temp = pygame.transform.scale(self.__image, self.__SIZE * scale)
        temp = pygame.transform.rotate(temp, angle)
        cnst.screen.blit(temp, (crd[0] - temp.get_width() // 2, crd[1] - temp.get_height() // 2))
    
    def get_image(self):
        return self.__image