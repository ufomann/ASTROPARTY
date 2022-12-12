from image import *
from constants import *
from general import *


class Bomb:
    """Класс бомбы. 
    Бомба взрывается (наносит урон), когда объект подлетает на расстояние,
    не превосходящее heatrad.
    """
    def __init__(self, coords, actrad):
        """Создание объекта класса Bomb
        __coords - координаты бомбы
        __heatrad - радиус видимости бомбы
        __image - картинка
        __isActivated - активирована ли бомба
        """
        self.__heatrad = 50
        self.__coords = coords
        self.__image = Image(BOMBIMG[0])
        self.__isActivated = False
    
    def activate(self, ships):
        """Метод активации бомбы.
        Нанесение урона всем кораблям, попадающим в радиус бомбы
        """
        self.__isActivated = True
        for ship in ships:
            if vec_len(radius_vector(self, ship)) <= self.__heatrad:
                ship.set_dead(True)

    def get_activated(self):
        """Узнать, активирована ли бомба"""
        return self.__isActivated
    
    def draw(self, scale=1):
        self.__image.draw(0, self.__coords, scale)
    
    def get_coord(self):
        return self.__coords

    def get_heatrad(self):
        return self.__heatrad
        

def check_bombs(bombs: list, ships: list):
    """Проходится по списку бомб и кораблей и проверяет, есть ли столкновение c obj y бомб """
    for ship in ships:
        for bomb in bombs:
            if collisionCheck(bomb, ship):
                bomb.activate(ships)
