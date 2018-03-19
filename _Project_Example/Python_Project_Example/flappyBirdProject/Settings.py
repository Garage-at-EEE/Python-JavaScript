from itertools import cycle
import random
import sys

import pygame
from pygame.locals import *

# initialization 
FPS = 30 #Frames Per Second -- Define the change of graph in respect to the time.
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
# amount by which base can maximum shift to left
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dictionary( Pairs of key - value binding )
IMAGES, HITMASKS = {}, {}
# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)
# tuple inside a tuple #

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)

# variable
#--------------- 
# integer
# float
# tupple
# set/dictionary
# [list]
