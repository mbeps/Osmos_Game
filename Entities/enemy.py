from Entities.ball import Ball

class Enemy (Ball):
    """Creates Enemy object.
        Enemy will have the same functionality of Ball but will have some extra.  
        Args:
            Enemy (Ball): super-class of Player. 
        """
    def __init__ (self, position, velocity, radius):
        super().__init__(position, velocity, radius) # Use the initializer from super-class
        self.type = "enemy"
        self.colour = "red"