
#^ MODULES:
        # import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
        # from Game_Physics.Vector import Vector
        # from Entities.ball import Ball
        # from Entities.player import Player
        # from Entities.enemy import Enemy
        # from Entities.mass import Mass
        # from Maps.line import Line
        # from interaction import Interaction
from modules import *

#^ CONSTANTS:
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

#^ MAIN:
#^ Setting Up Environment:
balls = [Enemy(Vector(400, 100), Vector(-3, -3), 10),
        Enemy(Vector(150, 100), Vector(4, -3), 15),
        Enemy(Vector(150, 300), Vector(5, 7), 10),
        Player(Vector(150, 134), Vector(5, 6), 20)]
lines = [Line(Vector(0, 0), Vector(0, CANVAS_HEIGHT)), # Vertical 1
        Line(Vector(0, 0), Vector(CANVAS_WIDTH, 0)), # Horizontal 1
        Line(Vector(CANVAS_WIDTH, 0), Vector(CANVAS_WIDTH, CANVAS_HEIGHT)), # Vertical 2
        Line(Vector(0, CANVAS_HEIGHT), Vector(CANVAS_WIDTH, CANVAS_HEIGHT))] # Horizontal 2
interaction = Interaction(balls, lines)

#^ Setting Up Backend:
frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)
frame.start()