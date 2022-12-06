import numpy as np
from math import *

import pygame

from image import *
import constants as cnst
from game_screen import *
from start_screen import *

class Title():
    def __init__(self, path, x, y):
        """Создание объекта Title
        Атрибуты:
        __image - объект класса Image, картинка
        __coord - координаты центра title
        """
        self.__image = Image(path)
        self.__coord = np.array([x, y])

    def draw(self, t = 0, scale = 1.4):
        """Нарисовать title"""
        t_scale = scale*(1 + (sin(t))/10)
        self.__image.draw(0, self.__coord, t_scale)        


class Button():
    def __init__(self, path, path_pr, x, y, scale = 1.2):
        """Создание объекта кнопки
        Атрибуты:
        __image - объект класса Image, картинка
        __coord - координаты центра кнопки
        """
        self.__image = Image(path)
        self.__image_pr = Image(path_pr)
        self.__coord = np.array([x, y])
        self.__scale = scale

    def check_click(self, event):
        """Проверка нажатия на кнопку, возвращает bool"""
        x_click = event.pos[0]
        y_click = event.pos[1]

        left_side = self.__coord[0] - self.__scale*self.__image.get_image().get_width()//2
        right_side = self.__coord[0] + self.__scale*self.__image.get_image().get_width()//2
        top_side = self.__coord[1] - self.__scale*self.__image.get_image().get_height()//2
        down_side = self.__coord[1] + self.__scale*self.__image.get_image().get_height()//2

        if (right_side > x_click > left_side) and (down_side > y_click > top_side):
            return True
        else:
            return False

    def check_pos(self):
        """Проверяет, наведена ли мышь на кнопку"""
        x_click = pygame.mouse.get_pos()[0]
        y_click = pygame.mouse.get_pos()[1]

        left_side = self.__coord[0] - self.__scale*self.__image.get_image().get_width()//2
        right_side = self.__coord[0] + self.__scale*self.__image.get_image().get_width()//2
        top_side = self.__coord[1] - self.__scale*self.__image.get_image().get_height()//2
        down_side = self.__coord[1] + self.__scale*self.__image.get_image().get_height()//2

        if (right_side > x_click > left_side) and (down_side > y_click > top_side):
            return True
        else:
            return False

    def draw(self):
        """Нарисовать кнопку"""
        if self.check_pos():
            self.__image_pr.draw(0, self.__coord, self.__scale)
        else:
            self.__image.draw(0, self.__coord, self.__scale)



class Start_button(Button):
    """Класс кнопки начала игры"""
    def __init__(self, path, path_pr, x, y):
        super().__init__(path, path_pr, x, y)

    def change_screen(self):
        """Поменять экран на game()"""
        game()
    
    def property(self):
        """Основное свойство кнопки"""
        self.change_screen()

class Back_to_menu_button(Button):
    """Класс кнопки возвращения к главному меню"""
    def __init__(self, path, path_pr, x, y, scale=1.2):
        super().__init__(path, path_pr, x, y, scale)

    def change_screen(self):
        """Поменять экран на menu"""
        start_menu()

    def property(self):
        self.change_screen()

def check_button(buttons, event):
    """Проверяет, нажали ли на кнопку. Если какая-либо из кнопок нажата, вызывает ее основной метод"""
    for button in buttons:
        if button.check_click(event):
            button.property()
            break

