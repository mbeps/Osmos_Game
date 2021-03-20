from Entities.ball import Ball

class Mass (Ball):
    """Creates Mass object.
        Mass will have the same functionality of Ball but will have some extra.  
        Args:
            Mass (Ball): super-class of Player. 
        Call:
            super().__init__(position, velocity, radius): calls the constructor of the super class to initialize object.  
        """
    def __init__ (self, position, velocity, radius):
        super().__init__(position, velocity, radius) # Use the initializer from super-class