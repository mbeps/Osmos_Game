
#^ MODULES:
from interactions import Interaction
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Game_Physics.Vector import Vector
from map import *

#^ CONSTANTS:
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

#^ MAIN:
#^ Testing
lines = [Line(Vector(0, 0), Vector(0, CANVAS_HEIGHT)), 
        Line(Vector(CANVAS_WIDTH, 0), Vector(CANVAS_WIDTH, CANVAS_HEIGHT)), 
        Line(Vector(0, 0), Vector(CANVAS_WIDTH, 0)), 
        Line(Vector(0, CANVAS_HEIGHT), Vector(CANVAS_WIDTH, CANVAS_HEIGHT))]

interaction = Interaction(lines)

frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)

frame.start()