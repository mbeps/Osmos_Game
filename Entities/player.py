from Entities.ball import Ball

class Player (Ball):
    """Creates Player object.
        Player will have the same functionality of Ball but will have some extra. 
        The player is green. 
        
        Args:
            `Ball (Ball)`: super-class of Player. 
        Call:
            `super().__init__(position, velocity, radius)`: calls the constructor of the super class to initialize object.  
        """
    def __init__ (self, position, velocity, radius):
        super().__init__(position, velocity, radius) # Use the initializer from super-class
        self.type = "Player"
        self.colour = "Green"
        self.alive = True
        self.move = True
        self.power_up = "None" #* (None / Speed). More can be added

    def can_move(self):
        """Checks if there is enough mass to move. 
            Since the player loses mass to change direction manually, 
            an if statement is used to check if there is enough mass. 
            If there is not, the player cannot change direction until it has enough mass. 
            The radius is checked for this operation. 
            """
        radius_limit = 10
        if (self.radius <= radius_limit): # Less than 6 means that there is no enough mass to move manually
            self.move = False # Indiacates that cannot manually move
        elif (self.radius > radius_limit): # Greater than 5 means that the player can move manually
            self.move = True # Indicates that the player can move