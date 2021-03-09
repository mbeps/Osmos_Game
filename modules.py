"""List of all modules that will be used from main. 
    This will allow only for one module to be imported which will import all the necessary modules. 
    """
from interactions import Interaction
from Entities.enemy import Enemy
from Entities.ball import Ball
from Game_Physics.Vector import Vector
from Maps.map import Line
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui