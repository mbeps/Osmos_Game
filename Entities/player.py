from Entities.ball import Ball

class Player (Ball):
    """Creates Player object.
        Player will have the same functionality of Ball but will have some extra.  
        Args:
            Ball (Ball): super-class of Player. 
        """
    def __init__ (self, position, velocity, radius):
        super().__init__(position, velocity, radius) # Use the initializer from super-class
        self.type = "player".lower
        self.colour = "green"