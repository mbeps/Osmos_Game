from Entities.ball import Ball

class Enemy (Ball):
    """Enemy objects are supposed to attack the player.
        Enemy is sub-class of Ball which means that it inherits the functionalities such as movement and bounce. 
        """
    def __init__ (self, position, velocity, radius):
        """Initializes the enemy object. 
            Enemy class calls the initializer from Ball class which is the super-class.
            Enemy has different colour from the Ball. 

            Args:
                `position (Vector)`: initial position of the ball.
                `velocity (Vector)`: direction of the ball.
                `radius (int)`: size of the radius.
            """
        super().__init__(position, velocity, radius) # Use the initializer from super-class
        self.type = "enemy"
        self.colour = "red"