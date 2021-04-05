"""List of all modules needed in main
    """
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

from Entities.ball import Ball
from Entities.player import Player
from Entities.enemy import Enemy
from Entities.mass import Mass

from Maps.line import Line

from Game_Control.Vector import Vector
from Game_Control.interactions import Interaction
from Game_Control.keyboard import Keyboard

from Game_Environment.user_settings import *