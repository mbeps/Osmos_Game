"""This is where the user can set settings. 
		Game settings can be changed thorugh the terminal. 
	"""

from SimpleGUICS2Pygame.simpleguics2pygame import canvas

def set_setting(time_limit, canvas_dimensions):
	"""Asks the user whether they would like to change game settings.
		The function will take the default settings as arguments. 
		It will take the input from the user to evaluate whether they want to change the settings. 
		If they would like to change the settings, then the functions to set time and canvas size will be called and the appropriate arguments will be passed. 
		Otherwise, the nothing will be changed and the function will terminate. 
		
		Args:
			time_limit (int): the time limit of the game in by which the player must win
			canvas_dimensions (int[]): dimensions of the canvas

		Calls:
			set_time(time_limit): set the time limit of the game by changing the default time passed as argument
			set_canvas_size(canvas_size): sets the size of the canvas by changing the default time passed as argument
		"""
	print("Would you like to play with the default settings or would you like to change them?")
	choice = False
	choice = str(input("Choice (yes / no): ")).lower

	if (choice == "yes".lower) or (choice == "y".lower):
		set_time(time_limit)
		set_canvas_size(canvas_dimensions)	

def set_time(time_limit): 
	"""Allows the user select the time limit. 
		The function takes the default time and modifies it. 
		Takes the input from the user and returns in as integer. 
		
		Checks if the input is valid by checking if the input is not less than 0. 
		If the input is invalid, then a message is displayed and user is asked to enter again. 
		This done by recursively calling the current method until the input is valid. 

		To set the time limit to be unlimited, 0 is entered. 
		This will change the variable to -1 (which  is the default). 
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

def set_canvas_size(canvas_dimensions):
	"""Allows the user to input the size of the canvas.
		The functions takes the default size and modifies it. 
		Function takes the input for the height and width from the user and assigns them into the respective variables. 
		Some checks are done on the variable before modifying the sizes in the list. 

		If the user enters an invalid type (for example string), then an error will be displayed. 
		The user will have to reenter the values. 
		This is done by catching the exceptions in the try-catch block. 

		If the input type is valid then other checks are carried out using if statements. 
		If the checks fail, then the user is asked to input the size again. 
		Checks whether the values entered are too small by comparing the default value which are stored in the list. 
		After, it checks whether the input is too large. 
		Finally, it checks if the inputs are 0 in which case the list will be unchanged, as a result the default will be returned. 
		In case the default sizes are not returned, then the initial user input are stored in the list which is then returned. 

		Args:
			canvas_dimensions (int[]): height (x) and width (y) of the canvas

		Returns:
			(int[]): height (x) and width (y) of the canvas
		"""
	print(f'Select the size of the canvas. Selecting 0 will set the default size of {canvas_dimensions[0]} × {canvas_dimensions[1]} which is the minimum size. The maximum size is 1500 × 800')
	try:
		height = int(input("Canvas Height (pixels): "))
		width = int(input("Canvas Width (pixels): "))
	except ValueError: # If the user enters a string
		input("Invalid input. Press any key to continue. ")
		set_canvas_size() # Calls current method to enter input again

	if (height == 0) and (width == 0):
		return canvas_dimensions # Return default size
	elif (height < canvas_dimensions[0]) and (width < canvas_dimensions[1]):
		input("Size too small. Press any key to continue. ")
		set_canvas_size() # Calls current method to enter input again
	elif (height > 1500) and (width > 800):
		input("Size too big. Press any key to continue. ")
		set_canvas_size() # Calls current method to enter input again

	canvas_dimensions[0] = height
	canvas_dimensions[1] = width

	return canvas_dimensions
