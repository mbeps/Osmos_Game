
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
keyboard = Keyboard()
balls = [Enemy(Vector(200, 100), Vector(-3, -3), 20), Enemy(Vector(700, 270), Vector(2,4), 30)]
# balls = [Enemy(Vector(1000, 1000), Vector(-3, -3), 20)]

player = Player(Vector(300, 200), Vector(0, 0), 20)

lines = [Line(Vector(0, 0), Vector(0, CANVAS_HEIGHT)), # Vertical 1
        Line(Vector(0, 0), Vector(CANVAS_WIDTH, 0)), # Horizontal 1
        Line(Vector(CANVAS_WIDTH, 0), Vector(CANVAS_WIDTH, CANVAS_HEIGHT)), # Vertical 2
        Line(Vector(0, CANVAS_HEIGHT), Vector(CANVAS_WIDTH, CANVAS_HEIGHT))] # Horizontal 2
interaction = Interaction(lines, player, balls, keyboard)

#^ Setting Up Backend:
frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.start()