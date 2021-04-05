
#^ MODULES:
from Entities.power_ups import Power_Up
from SimpleGUICS2Pygame.simpleguics2pygame.frame import create_frame
from modules import *

def create_power_ups(power_ups): #* For testing only
	power_ups.append(Power_Up(Vector(random.randint(5, 790), random.randint(5, 490)), Vector(0, 0), 5))


#^ MAIN:
#^ Setting Up Environment:
canvas_dimensions = [800, 500] # Default canvas size
time_limit = -1 # Default time is unlimited 

enemies = [Enemy(Vector(200, 100), Vector(-3, -3), 15), 
        Enemy(Vector(700, 270), Vector(2,4), 20),
        Enemy(Vector(400, 160), Vector(-2, 1), 10),
        Enemy(Vector(434, 112), Vector(1, 4), 5)]
player = Player(Vector(canvas_dimensions[0] / 2, canvas_dimensions[1] - 100), Vector(0, 0), 20)
power_ups = []

for i in range(5): #* For testing only
	create_power_ups(power_ups)

frame = simplegui.create_frame("Domain", canvas_dimensions[0], canvas_dimensions[1])
lines = [Line(Vector(0, 0), Vector(0, canvas_dimensions[1])), # Vertical 1
        Line(Vector(0, 0), Vector(canvas_dimensions[0], 0)), # Horizontal 1
        Line(Vector(canvas_dimensions[0], 0), Vector(canvas_dimensions[0], canvas_dimensions[1])), # Vertical 2
        Line(Vector(0, canvas_dimensions[1]), Vector(canvas_dimensions[0], canvas_dimensions[1]))] # Horizontal 2
keyboard = Keyboard()
interaction = Interaction(lines, player, enemies, power_ups, time_limit, keyboard, frame)

#^ Setting Up Backend:
frame.set_draw_handler(interaction.draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.add_button("Exit Game", frame.stop)
frame.start()