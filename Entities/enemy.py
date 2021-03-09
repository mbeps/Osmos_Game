from Entities.ball import Ball

class Enemy (Ball):
    """Creates enemy object.
        Enemy will have the same functionality of Ball but will have some extra.  
        Args:
            Ball (Ball): super-class of Enemy. 
        """
    def __init__ (self, position, velocity, radius, color):
        super.__init__(position, velocity, radius, color) # Use the initializer from super-class