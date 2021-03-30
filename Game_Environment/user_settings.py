"""This is where the user can set settings. 
		Game settings can be changed thorugh the terminal. 
	"""

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
	try:
		time_limit = int(input("Time Limit (secs): "))
	except ValueError:
		input("Invalid input. Press any key to continue. ")
		set_time() # Calls current method to enter input again
	
	if (time_limit < 0): # Input is invalid if less than 0
		input("Invalid time. Press any key to continue. ")
		set_time() # Calls current method to enter input again
	elif (time_limit == 0):
		time_limit = -1 # Game ends when 0 is reached. Therefore, the game will never end. 
	
	return time_limit