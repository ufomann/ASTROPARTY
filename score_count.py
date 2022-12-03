import pygame 

import constants as cnst
from menu_buttons import *
from ship import *
import general

def score_line(rdscore, blscore): 
    '''rdscore - red ship's score after round (can be from -1 to 1)
       bluescore - blue ship's score after round (can be from -1 to 1)'''
    cnst.screen = pygame.display.set_mode((cnst.WIDTH, cnst.HEIGHT))
    clock = pygame.time.Clock()
    finished = False

    bg = pygame.image.load(cnst.MENU_OBJECTSIMG[0])
    blueship = Ship(cnst.BLUECOORDSONSCORELINE, BLUESHIPIMG, BLUESHIPSTR, 0)
    redship = Ship(cnst.REDCOORDSONSCORELINE, REDSHIPIMG, REDSHIPSTR, 0)
    scoreline = Image(cnst.SCORELINEIMG[0])
    scorelinecoords = arr(WIDTH / 2, HEIGHT / 2)
    width = scoreline.get_image().get_width()
    height = scoreline.get_image().get_height()
    step = 10/12 * height / SCORETOWIN
    localscale = cnst.SCORELINESCALE
    redship.set_coord(scorelinecoords + arr(-5 / 12 * height + SCORE['redship'] * step, width / 4) * localscale)
    blueship.set_coord(scorelinecoords + arr(-5 / 12 * height + SCORE['blueship'] * step, -width / 4) * localscale)

    scoreline.draw(-90, scorelinecoords, localscale)
    clock.tick(cnst.FPS)
    redship.move(localscale)
    blueship.move(localscale)
    pygame.display.update()
    pygame.time.delay(1000)

    spd = np.array([step * localscale / cnst.TIMEFORMOVE ,0])
    if not (rdscore < 0 and SCORE['redship'] <= 0):
        SCORE['redship'] = max(0, SCORE['redship'] + rdscore)
        redship.set_spd(signum(rdscore) * spd)
    if not (blscore < 0 and SCORE['blueship'] <= 0):
        SCORE['blueship'] = max(0, SCORE['blueship'] + blscore)
        blueship.set_spd(signum(blscore) * spd)
    time = 0

    while time < cnst.FPS * cnst.TIMEFORMOVE:
        time += 1
        scoreline.draw(-90, scorelinecoords, localscale)
        clock.tick(cnst.FPS)
        redship.move(localscale)
        blueship.move(localscale)
        pygame.display.update()
    pygame.time.delay(1000)
    
    if (SCORE['redship'] == SCORETOWIN and SCORE['blueship'] == SCORETOWIN):
        return 'both'
    elif (SCORE['blueship'] == SCORETOWIN):
        return 'blue'
    elif (SCORE['redship'] == SCORETOWIN):
        return 'red'
    else:
        return 'none'
'''for testing'''
'''print(score_line(-1, -1))
print(score_line(1, -1))
print(score_line(-1, 1))
print(score_line(-1, 1))
print(score_line(-1, 1))
print(score_line(0, 1))'''