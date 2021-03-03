# Main place where the game will start. 
# Other modules are called from here. 
#^ MODULES:
from interactions import Interaction
from Entities.ball import Ball
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Game_Physics.Vector import Vector
from Maps.map import *

#^ CONSTANTS:
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

#^ MAIN:
lines = [Line(Vector(0, 0), Vector(0, CANVAS_HEIGHT)), 
        Line(Vector(CANVAS_WIDTH, 0), Vector(CANVAS_WIDTH, CANVAS_HEIGHT)), 
        Line(Vector(0, 0), Vector(CANVAS_WIDTH, 0)), 
        Line(Vector(0, CANVAS_HEIGHT), Vector(CANVAS_WIDTH, CANVAS_HEIGHT))]
enemies = [Ball(Vector(200, 300), Vector(-1, 2), 10, "blue"),
        Ball(Vector(500, 150), Vector(3, -2), 15, "green")]
interaction = Interaction(lines, enemies)

frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)

frame.start()