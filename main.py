
#^ MODULES:
from modules import *

#^ MAIN:
#^ Setting Up Environment:
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

keyboard = Keyboard()
time_limit = set_time()
balls = [Enemy(Vector(200, 100), Vector(-3, -3), 15), 
        Enemy(Vector(700, 270), Vector(2,4), 20),
        Enemy(Vector(400, 160), Vector(-2, 1), 10),
        Enemy(Vector(434, 112), Vector(1, 4), 5)]
# balls = [Enemy(Vector(400, 300), Vector(-1, -1), 10)]

player = Player(Vector(400, 400), Vector(0, 0), 20)
frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
lines = [Line(Vector(0, 0), Vector(0, CANVAS_HEIGHT)), # Vertical 1
        Line(Vector(0, 0), Vector(CANVAS_WIDTH, 0)), # Horizontal 1
        Line(Vector(CANVAS_WIDTH, 0), Vector(CANVAS_WIDTH, CANVAS_HEIGHT)), # Vertical 2
        Line(Vector(0, CANVAS_HEIGHT), Vector(CANVAS_WIDTH, CANVAS_HEIGHT))] # Horizontal 2
interaction = Interaction(lines, player, balls, time_limit, keyboard, frame)

#^ Setting Up Backend:
frame.set_draw_handler(interaction.draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.add_button("Exit Game", frame.stop)
frame.start()