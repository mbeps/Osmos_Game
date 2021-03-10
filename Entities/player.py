from Entities.ball import Ball

class Player (Ball):
    """Creates Player object.
        Player will have the same functionality of Ball but will have some extra.  
        Args:
            Ball (Ball): super-class of Player. 
        """
    def __init__ (self, position, velocity, radius, color):
        super().__init__(position, velocity, radius, color) # Use the initializer from super-class
    
    def bounce(self, normal):
        return self.velocity.reflect(normal) # Bounce works by reflecting the ball in the normal
    
    def update(self):
        self.position.add(self.velocity) # Everytime this method is called, the velocity will be added to make it move