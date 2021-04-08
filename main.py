
#^ MODULES:
from modules import *

#^ MAIN:
#^ Game Environment:
canvas_dimensions = [1456, 819] # Default canvas size (16:9)
time_limit = -1 # Default time is unlimited 

#^ Entities:
enemies = [Enemy(Vector(200, 150), Vector(-3, -3), 35), 
        Enemy(Vector(700, 270), Vector(2,4), 20),
        Enemy(Vector(400, 160), Vector(-2, 1), 15),
        Enemy(Vector(434, 112), Vector(1, 4), 10)]
player = Player(Vector(canvas_dimensions[0] / 2, canvas_dimensions[1] - 100), Vector(0, 0), 30)

frame = simplegui.create_frame("Domain", canvas_dimensions[0], canvas_dimensions[1])
lines = [Line(Vector(0, 0), Vector(0, canvas_dimensions[1])), # Vertical 1
        Line(Vector(0, 0), Vector(canvas_dimensions[0], 0)), # Horizontal 1
        Line(Vector(canvas_dimensions[0], 0), Vector(canvas_dimensions[0], canvas_dimensions[1])), # Vertical 2
        Line(Vector(0, canvas_dimensions[1]), Vector(canvas_dimensions[0], canvas_dimensions[1]))] # Horizontal 2

#^ Backend:
keyboard = Keyboard()
interaction = Interaction(lines, player, enemies, time_limit, keyboard, frame)

#^ Handlers:
frame.set_draw_handler(interaction.draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.add_button("Exit Game", interaction.stop)
frame.start()