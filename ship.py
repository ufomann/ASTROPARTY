from bullet import *
from anim_image import *
import constants as cnst


def center_mass_speed(ship1, ship2):
    """mass of each ship is 1"""
    return (ship1.get_spd() + ship2.get_spd()) / 2


class Steering:
    '''This class links buttons on keybord and actions of a ship'''
    def __init__(self, buttons):
        self.up = buttons[0]
        self.down = buttons[1]
        self.conterclockwise = buttons[2]
        self.clockwise = buttons[3]
        self.shoot = buttons[4]
        self.ulta = buttons[5]
        self.coolshoot = buttons[6]


class Ammo:
    '''This class is for ammo of a ship, it has the following attributes:
    1)__angle - angle between ship and it's ammo                     type: float
    2)__paths - list of paths to ammo's pictures                     type: str
    3)__image - ammo's image                                         type: class Image
    4)__ammo - count of ammo remaining (can be between 0 and 3)      type: int
    5)__lastshot - time, when last shot was made                     type: int

    Methods: 
    1)moveAmmo - moves Ammo around a ship
    2)shoot - checks if ship can shoot and removes ammo if it can.
    '''
    def __init__(self, paths):
        self.__angle = 0
        self.__paths = paths
        self.__image = Image(self.__paths)
        self.__ammo = 0
        self.__lastshot = -1

    def moveAmmo(self, coords):
        self.__angle += cnst.OMEGAFORAMMO * cnst.TIME_PERIOD
        self.__angle %= 360
        for i in range(self.__ammo):
            self.__image.draw(self.__angle + i * 120, coords, cnst.SCALE)
        if self.__ammo == 3:
            self.__lastshot = -1
        else:
            if pygame.time.get_ticks() - self.__lastshot >= cnst.RELOADTIME:
                self.__lastshot = pygame.time.get_ticks()
                self.__ammo += 1
    
    def shoot(self):
        if (self.__ammo > 0):
            self.__lastshot = pygame.time.get_ticks()
            self.__ammo -= 1
            return True
        else:
            return False


class Ship:
    """this is ship class, it has the following atributes:
    1)__id - ship's id (can be 'red' of 'blue')                                         type: str
    2)__paths - list of paths to ship's pictures.                                       type: str
    3)__coords - coordinates of the ship (default coordinate system)                    type: numpy.array
    4)__angle - angle between 0x and ships direction (positive direction - clockwise)   type: float
    5)__spd - velocity of the ship                                                      type: numpy.array
    6)__force - engine force vector                                                     type: numpy.array
    7)__steer - steering buttons (check class Steering description)                     type: class Steering   
    8)__image - ship's image (check class Image description)                            type: class Image
    9)__heatrad - ship's heatbox is circle and this is it's radius                      type: float
   11)__wallTouch - to check if ship touches walls (dict{"l", bool}, {"r", bool}, 
                                                        {"u", bool}, {"d", bool})       type: dict 
   12)__extForce - external force vector (for example white holes can push you)         type: numpy.array
   13)__shield - ship's shield status (True if ship still has shield)                   type: bool
   14)__dead - ship's status (True if alive and False if dead)                          type: bool
   15)__nosetaildist - distance between ship's nose and tail                            type: float
   16)__ammo - ship's ammo (check class Ammo description)                               type: class Ammo
   17)__shieldImage - shield's image (check class Image description)                    type: class Image
   18)__blinkingShield - blinking shield's image                                        type: class Anim_image
   19)__gotDamaged - time, when ship got damaged                                        type: float

   Methods:
   1)__normSpd - ship constantly accelerates (changes velicity's direction), but speed is restricted. 
   normSpd is speed restrictor.
   2) changeSpd - changes ship's velocity according to external forces and player's actions.
   3) move - changes ship's coordinates and draws it's picture on screen.
   4) shoot - releases shoot if there are enough ammo.
   5) cool_shoot - ship shoot to all directions.
    """
    def __init__(self, coords, paths, steering, angle, id):
        self.__id = id
        self.__paths = paths
        self.__coords = np.array(coords, dtype=float)
        self.__angle = angle
        self.__spd = np.array([0, 0], dtype=float)
        self.__force = ed_vec(0) * 0
        self.__steer = Steering(steering)
        self.__image = Anim_image(self.__paths, cnst.PPS)
        self.__heatrad = 0
        self.__wallTouch = dict(l=False, r=False, u=False, d=False)
        self.__extForce = np.array([0, 0], dtype=float)
        self.__shield = True
        self.__dead = False
        self.__nosetaildist = self.__image.get_image().get_height() // 2 
        self.__ammo = Ammo(cnst.AMMOIMG[0])
        self.__shieldImage = Image(cnst.SHIELDIMG[0])
        self.__blinkingShield = Anim_image(cnst.SHIELDIMG, cnst.PPS)
        self.__gotDamaged = -1

    def __normSpd(self):
        if vec_len(self.__spd) >= cnst.MAX_SPD:
            self.__spd = self.__spd / vec_len(self.__spd) * cnst.MAX_SPD 

    def changespd(self):
        keystatus = pygame.key.get_pressed()
        if keystatus[self.__steer.conterclockwise]:
            # decrease angle if player spinning conterclockwise
            self.__angle -= cnst.OMEGA * cnst.TIME_PERIOD
        if keystatus[self.__steer.clockwise]:
            # increase angle if player spinning clockwise
            self.__angle += cnst.OMEGA * cnst.TIME_PERIOD
        self.__force = ed_vec(self.__angle) * cnst.FORCE + self.__extForce
        self.__spd += self.__force * cnst.TIME_PERIOD
        self.__normSpd()

    def move(self, scale, ammo=True):
        self.__coords += self.__spd * cnst.TIME_PERIOD
        self.__heatrad = self.__image.get_image().get_width() // 2
        self.__image.draw(-self.__angle - 90, self.__coords, scale)

        if self.__shield:
            self.__shieldImage.draw(-self.__angle - 90, self.__coords, scale)
        if self.__gotDamaged != -1:
            self.__blinkingShield.draw(-self.__angle - 90, self.__coords, scale)
            if pygame.time.get_ticks() - self.__gotDamaged > cnst.INVINCIBLE:
                self.__gotDamaged = -1
        if ammo:
            self.__ammo.moveAmmo(self.__coords)

    def shoot(self, bullets):
        if (self.__ammo.shoot()):
            bulCoords = self.get_coord() + ed_vec(self.__angle) * self.__nosetaildist / 2
            bullets.append(Bullet(bulCoords, self.get_spd(), self.__angle, self.__nosetaildist))

    def cool_shoot(self, bullets):
        number_of_bullets = 25
        bulCoords = []
        bulAngle = []
        bulCoords.append(self.get_coord() + ed_vec(self.__angle) * self.__nosetaildist / 2)
        bulAngle.append(self.get_angle())
        for i in range(1, number_of_bullets):
            angle = self.__angle + 360 / number_of_bullets*i
            bulCoords.append(self.get_coord() + ed_vec(angle) * self.__nosetaildist / 2)
            bulAngle.append(angle)
        for k in range(number_of_bullets):
            bullets.append(Bullet(bulCoords[k], self.get_spd(), bulAngle[k], self.__nosetaildist / 2))

    def get_injured(self):
        if self.__gotDamaged == -1:
            if self.__shield:
                self.__shield = False
                self.__gotDamaged = pygame.time.get_ticks()
            else:
                self.__dead = True

    '''getters'''
    def get_coord(self):
        return self.__coords

    def get_angle(self):
        return self.__angle

    def get_spd(self):
        return self.__spd

    def get_heatrad(self):
        return self.__heatrad

    def get_walltouch(self):
        return self.__wallTouch

    def get_dead(self):
        return self.__dead

    def get_steer(self):
        return self.__steer

    def get_id(self):
        return self.__id

    '''setters'''
    def set_coord(self, coord):
        self.__coords = coord

    def set_extForce(self, extForce):
        self.__extForce = extForce

    def set_shield(self, shield):
        self.__shield = shield

    def set_spd(self, spd):
        self.__spd = spd

    def set_walltouch(self, wallTouch):
        self.__wallTouch = wallTouch

    def set_dead(self, isDead):
        self.__dead = isDead


def collision(ships):
    '''calculates collisions between ships'''

    for ship in ships:
        touch = ship.get_walltouch()
        v = ship.get_spd()
        if touch['r']:
            v[0] = max(v[0], 0)
        if touch['d']:
            v[1] = max(v[1], 0)
        if touch['l']:
            v[0] = min(v[0], 0)
        if touch['u']:
            v[1] = min(v[1], 0)

    for i in range(len(ships)):
        for j in range(i + 1, len(ships)):
            if collisionCheck(ships[i], ships[j]):
                vcm = center_mass_speed(ships[i], ships[j])  # calculate center mass
                if np.dot(ships[i].get_spd() - vcm, radius_vector(ships[i], ships[j])) > 0:
                    # if ships move towards each other (above) ^
                    # velocities in frame of reference of center mass
                    v1cm = ships[i].get_spd() - vcm
                    v2cm = ships[j].get_spd() - vcm
                    # getting vectors with len = 1 pointing from ship1 to ship2 and opposite
                    erv1 = radius_vector(ships[i], ships[j])/vec_len(radius_vector(ships[i], ships[j]))
                    erv2 = -erv1
                    # getting speed components (n and t)
                    v1cmt = np.dot(v1cm, erv1) * erv1
                    v1cmn = v1cm - v1cmt
                    v2cmt = np.dot(v2cm, erv2) * erv2
                    v2cmn = v2cm - v2cmt
                    vcmt = (v1cmt + v2cmt) / 2
                    v1 = v1cmn + vcmt + vcm
                    v2 = v2cmn + vcmt + vcm
                    touch1 = ships[i].get_walltouch()
                    touch2 = ships[j].get_walltouch()
                    # moving through the ship, which touches the wall is prohibited
                    if touch1['r'] or touch2['r']:
                        v1[0] = max(v1[0], 0)
                        v2[0] = max(v2[0], 0)
                    if touch1['d'] or touch2['d']:
                        v1[1] = max(v1[1], 0)
                        v2[1] = max(v2[1], 0)
                    if touch1['l'] or touch2['l']:
                        v1[0] = min(v1[0], 0)
                        v2[0] = min(v2[0], 0)
                    if touch1['u'] or touch2['u']:
                        v1[1] = min(v1[1], 0)
                        v2[1] = min(v2[1], 0)
                    ships[i].set_spd(v1)
                    ships[j].set_spd(v2)
