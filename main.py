
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

#^ FUNCTIONS:
def set_time():
	"""Allows the user select the time limit. 
		Takes the input from the user and returns in as integer. 
		
		Checks if the input is valid by checking if the input is not less than 0. 
		If the input is invalid, then a message is displayed and user is asked to enter again. 
		This done by recursively calling the current method until the input is valid. 

		To set the time limit to be unlimited, 0 is entered. 
		This will change the variable to -1. 
		This is done so that when decrementing the timer in the interaction module 0 is never reached. 
		If 0 is never reached the game will not terminate because the timer ran out (reached 0). 

		Returns:
			(int): time limit
		"""
	print("Select the time limit for the game. Setting 0 will mean that there is no time limit. ")
	time_limit = int(input("Time Limit (secs): "))
	if (time_limit < 0): # Input is invalid if less than 0
		input("Invalid time. Press any key to continue. ")
		set_time() # Calls current method to enter input again
	elif (time_limit == 0):
		time_limit = -1 # Game ends when 0 is reached. Therefore, the game will never end. 
	
	return time_limit

#^ MAIN:
#^ Setting Up Environment:
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