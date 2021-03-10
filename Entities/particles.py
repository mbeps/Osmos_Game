from Entities.ball import Ball

class Particle (Ball):
    """Creates Particle object.
        Particle will have the same functionality of Ball but will have some extra.  
        Args:
            Ball (Ball): super-class of Particle. 
        """
    def __init__ (self, position, velocity, radius, color):
        super().__init__(position, velocity, radius, color) # Use the initializer from super-class