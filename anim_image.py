import pygame
import constants as cnst
import numpy as np

class Anim_image:
    def __init__(self, paths, pps):
        self.__list_img = []
        for path in paths:
            self.__list_img.append(pygame.image.load(path).convert_alpha())
        self.__pps = pps
        self.__last_change = pygame.time.get_ticks()
        self.__currPic = 0
        self.__SIZE = np.array([self.__list_img[0].get_width(), self.__list_img[0].get_height()])

    def change_main_img(self):
        """Меняет картинку, с помощью коротой рисуется объект"""
        n = len(self.__list_img)
        self.__currPic = (self.__currPic + 1) % n
        self.__last_change = pygame.time.get_ticks()
        

    def draw(self, angle, coords, scale):
        crd = cnst.CAMERA.transform(coords)
        if pygame.time.get_ticks() - self.__last_change >= 1/self.__pps * 1000:
            self.change_main_img()
        temp = pygame.transform.scale(self.__list_img[self.__currPic], self.__SIZE * scale)
        temp = pygame.transform.rotate(temp, angle)
        cnst.screen.blit(temp, (crd[0] -temp.get_width() // 2, crd[1] -temp.get_height() // 2))

    def get_image(self):
        return self.__list_img[self.__currPic]
        


    

    
