from bullet import *


def center_mass_speed(ship1, ship2):
    """mass of each ship is 1"""
    return (ship1.get_spd() + ship2.get_spd()) / 2


class Steering:
    '''TODO'''
    def __init__(self, buttons):
        self.up = buttons[0]
        self.down = buttons[1]
        self.conterclockwise = buttons[2]
        self.clockwise = buttons[3]
        self.shoot = buttons[4]
        self.ulta = buttons[5]

class Ammo:
    def __init__(self, paths):
        self.__angle = 0
        self.__paths = paths
        self.__image = Image(self.__paths)
        self.__ammo = 0
        self.__lastshot = -1

    def moveAmmo(self, shipAng, coords):
        self.__angle += OMEGAFORAMMO * TIME_PERIOD
        self.__angle %= 360
        for i in range(self.__ammo):
            self.__image.draw(self.__angle + i * 120, coords, SCALE)
        if self.__ammo == 3:
            self.__lastshot = -1
        else:
            if pygame.time.get_ticks() - self.__lastshot >= RELOADTIME:
                self.__lastshot = pygame.time.get_ticks()
                self.__ammo += 1
    
    def shoot(self):
        if (self.__ammo > 0):
            self.__lastshot = pygame.time.get_ticks()
            self.__ammo -= 1
            return True
        else:
            return False

        self.coolshoot = buttons[6]


class Ship:
    """this is ship class, it has the following atributes and methods:
    1)all atributes are protected, so to access them we have setters and getters
    2)__paths - list of paths to ship's pictures.                                       type: str
    3)__coords - coordinates of the ship (default coordinate system)                    type: numpy.array
    4)__angle - angle between 0x and ships direction (positive direction - clockwise)   type: float
    5)__spd - velocity of the ship                                                      type: numpy.array
    6)__force - engine force vector                                                     type: numpy.array
    7)__steer - steering buttons (check class Steering description)                     type: class Steering   
    8)__image - ship's image (check class Image description)                            type: calss Image
    9)__heatrad - ship's heatbox is circle and this is it's radius                      type: float
   10)__screen - this is for drawing ship                                               type: pygame.display
   11)__wallTouch - to check if ship touches walls (dict{"l", bool}, {"r", bool}, 
                                                        {"u", bool}, {"d", bool})       type: dict 
   12)__extForce - external force vector (for example anti black holes can push you)    type: numpy.array
   13)__id - identificator of ship; can be 'red' of 'blue'                              type: str
    """
    def __init__(self, coords, paths, steering, angle, id):
        self.__paths = paths
        self.__coords = np.array(coords, dtype=float)
        self.__angle = angle
        self.__force = ed_vec(0) * 0
        self.__steer = Steering(steering)
        self.__spd = np.array([0, 0], dtype=float)
        self.__image = Image(self.__paths[0])
        self.__heatrad = 0
        self.__wallTouch = dict(l=False, r=False, u=False, d=False)
        self.__Shield = True
        self.__dead = False
        self.__nosetaildist = self.__image.get_image().get_height() // 2 * SCALE
        self.__extForce = np.array([0, 0], dtype=float)
        self.__id = id
        self.__ammo = Ammo(AMMOIMG[0])

    def __normSpd(self):
        '''ships can't move faster than MAX_SPD'''
        if vec_len(self.__spd) >= MAX_SPD:
            self.__spd = self.__spd / vec_len(self.__spd) * MAX_SPD 

    def changespd(self):
        """this function is for changing ship's velocity according to player's actions"""
        keystatus = pygame.key.get_pressed()
        if keystatus[self.__steer.conterclockwise]:
            # decrease angle if player spinning conterclockwise
            self.__angle -= OMEGA * TIME_PERIOD
        if keystatus[self.__steer.clockwise]:
            # increase angle if player spinning clockwise
            self.__angle += OMEGA * TIME_PERIOD
        self.__force = ed_vec(self.__angle) * FORCE + self.__extForce
        self.__spd += self.__force * TIME_PERIOD
        self.__normSpd()

    def move(self, scale):
        self.__coords += self.__spd * TIME_PERIOD
        self.__heatrad = self.__image.get_image().get_width() // 2 * scale * 1
        self.__image.draw(-self.__angle - 90, self.__coords, scale)
        self.__ammo.moveAmmo(self.__angle, self.__coords)

    def shoot(self, bullets, scale):
        if (self.__ammo.shoot()):
            bulCoords = self.get_coord() + ed_vec(self.__angle) * self.__nosetaildist
            bullets.append(Bullet(bulCoords, self.get_spd(), self.__angle))

    def cool_shoot(self, bullets):
        number_of_bullets = 5
        bulCoords = []
        bulAngle = []
        bulCoords.append(self.get_coord() + ed_vec(self.__angle) * self.__nosetaildist)
        bulAngle.append(self.get_angle())
        for i in range(1, number_of_bullets):
            angle = self.__angle + 360/number_of_bullets*i
            bulCoords.append(self.get_coord() + ed_vec(angle) * self.__nosetaildist)
            bulAngle.append(angle)
        for k in range(number_of_bullets):
            bullets.append(Bullet(bulCoords[k], self.get_spd(), bulAngle[k]))

    def get_coord(self):
        return self.__coords

    def get_angle(self):
        return self.__angle

    def get_spd(self):
        return self.__spd

    def set_spd(self, spd):
        self.__spd = spd
    
    def get_heatrad(self):
        return self.__heatrad
    
    def get_walltouch(self):
        return self.__wallTouch

    def set_walltouch(self, wallTouch):
        self.__wallTouch = wallTouch

    def get_injured(self):
        if self.__Shield:
            self.__Shield = False
        else:
            self.__dead = True

    def get_dead(self):
        return self.__dead
    
    def set_dead(self, isDead):
        self.__dead = isDead
    
    def get_steer(self):
        return self.__steer

    def set_coord(self, coord):
        self.__coords = coord
    
    def set_extForce(self, extForce):
        self.__extForce = extForce

    def get_id(self):
        return self.__id


def collision(ships):
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
    '''calculates collisions between every pair of ships'''
    for i in range(len(ships)):
        for j in range(i + 1, len(ships)):
            if collisionCheck(ships[i], ships[j]):
                vcm = center_mass_speed(ships[i], ships[j]) # calculate center mass
                if np.dot(ships[i].get_spd() - vcm, radius_vector(ships[i], ships[j])) > 0:
                    # if ships move towards each other
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
