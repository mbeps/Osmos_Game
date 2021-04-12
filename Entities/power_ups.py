from Game_Control.Vector import Vector
from Entities.ball import Ball

class Power_Up (Ball):
    """Power Up objects are supposed to give certain power ups to the player.
        Power is sub-class of Ball which means that it inherits the functionalities such as movement and bounce.
		When there is a collision with the player, a specific power up (speed / mass) will be given for a limited time. 
        
        """
    def __init__ (self, position):
        """Initializes the Power Up object. 
            Power Up class calls the initializer from Ball class which is the super-class.
            Power Up has different colour from the Ball. 

            Args:
                `position (Vector)`: initial position of the ball.
                `velocity (Vector)`: direction of the ball.
            """
        super().__init__(position, Vector(0, 0), 5) # Use the initializer from super-class
        self.type = "Power_Up"
        self.colour = "Yellow"