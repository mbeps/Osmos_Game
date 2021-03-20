from Entities.ball import Ball

class Player (Ball):
    """Creates Player object.
        Player will have the same functionality of Ball but will have some extra.  
        Args:
            Ball (Ball): super-class of Player. 
        Call:
            super().__init__(position, velocity, radius): calls the constructor of the super class to initialize object.  
        """
    def __init__ (self, position, velocity, radius):
        super().__init__(position, velocity, radius) # Use the initializer from super-class
        self.type = "player"
        self.colour = "green"