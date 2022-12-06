import constants as cnst
from game_screen import *
from start_screen import *
from barrier import *
from win_screen import *

execution_finished = False

while not execution_finished:
    if cnst.screen_position == 1:
        start_menu()
    elif cnst.screen_position == 2:
        game(field_type1)
    elif cnst.screen_position == 4:
        win_screen(0)
    else:
        execution_finished = True
pygame.quit()
