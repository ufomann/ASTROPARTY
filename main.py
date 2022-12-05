import constants as cnst
from game_screen import *
from start_screen import *
from barrier import *

execution_finished = False

while not execution_finished:
    if cnst.screen_position == 1:
        game(field_type1)
    elif cnst.screen_position == 2:
        start_menu()
    else:
        execution_finished = True
pygame.quit()
