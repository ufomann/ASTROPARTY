from math import *

import pygame
from image import *
from constants import *
from general import *


class Bullet: 
    def __init__(self, coords, spd, angle):
        """
        Создание пули. Надо указать координаты стреляющего корабля, его скорость, путь до картинки с пулей, экран для рисования
        Атрибуты:
        __image - объект класса Image, создаваемый на основе BULLETIMG
        __coords - координаты пули (в начале совпадают с координатами корабля)
        __spd - скорость пули (высчитывается, как скорость относительно корабля + скорость корабля)
        __heatrad - радиус, на котором пуля видна
        __is_dead - уничтожена ли пуля
        """
        self.__image = Image(BULLETIMG[0])
        self.__coords = coords
        self.__spd = spd + ed_vec(angle)*BULLET_SPD
        self.__heatrad = self.__image.get_image().get_width() // 2 * SCALE * 1
        self.__is_dead = False
        self.__extForce = np.array([0,0], dtype=float)
    
    def change_spd(self):
        self.__spd += self.__extForce*TIME_PERIOD

    def move(self, scale):
        """Перемещение пули за TIME_PERIOD
        При каждом вызове пуля сразу отрисовывается с помощь метода класса Image
        """
        self.__coords += self.__spd*TIME_PERIOD
        self.__image.draw(0, self.__coords, scale)

    def get_coord(self):
        """Получить координаты пули """
        return self.__coords

    def get_spd(self):
        """Получить скорость пули"""
        return self.__spd

    def get_heatrad(self):
        """Получить 'радиус видимости' пули  """
        return self.__heatrad

    def get_dead(self):
        """Узнать, уничтожена ли пуля """
        return self.__is_dead

    def set_dead(self, bool_var):
        """Изменить статус пули """
        self.__is_dead = bool_var
    
    def set_extForce(self, extForce):
        self.__extForce = extForce

    def collision_with_ship(self, ships):
        """Столкновение пули с кораблем """
        for ship in ships:
            if collisionCheck(ship, self):
                ship.get_injured()
                self.__is_dead = True
        
