import numpy as np
import constants as cnst

class Cam:
    '''This is "active" camera class. Active camera follows the ships to provide the user with optimal viewing point
     It has the following methods:
     1) calc - finds the best viewing point
     2) transform - releases transform from game coordinate system to screen coordinate system'''
    def __init__(self, scale):
        self.__crdPoint = np.array([0, 0])
        cnst.SCALE = scale
    
    def calc(self, shp1, shp2):
        self.__crdPoint = (shp1 + shp2) / 2 - 1 / (2 * cnst.SCALE) * np.array([cnst.WIDTH, cnst.HEIGHT])
        shp1 = cnst.CAMERA.transform(shp1) * 1
        shp2 = cnst.CAMERA.transform(shp2) * 1
        curr = min(shp1[0], shp2[0], shp1[1], shp2[1])
        cnst.SCALE -= (cnst.BORDER - curr) ** 3 * cnst.SCALE_SPD * cnst.TIME_PERIOD
        cnst.SCALE = max(cnst.SCALE, cnst.MINSCALE)
        cnst.SCALE = min(cnst.SCALE, cnst.MAXSCALE)
        
    def transform(self, crd):
        ans = (crd - self.__crdPoint) * cnst.SCALE
        return ans
    
