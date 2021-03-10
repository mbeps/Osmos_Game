from Entities.ball import Ball

class Mass (Ball):
    """Creates Mass object.
        Mass will have the same functionality of Ball but will have some extra.  
        Args:
            Mass (Ball): super-class of Player. 
        """
    def __init__ (self, position, velocity, radius):
        super().__init__(position, velocity, radius) # Use the initializer from super-class