from Entities.ball import Ball
from Game_Control.Vector import Vector

class Player (Ball):
    """Creates Player object.
        Player will have the same functionality of Ball but will have some extra. 
        The player is green. 
        
        Args:
            `Ball (Ball)`: super-class of Player. 
        Call:
            `super().__init__(position, velocity, radius)`: calls the constructor of the super class to initialize object.  
        """
    def __init__ (self, position: Vector, velocity: Vector, radius: int) -> None:
        super().__init__(position, velocity, radius) # Use the initializer from super-class
        self.type: str = "Player"
        self.colour: str = "Green"
        self.alive: bool = True
        self.move: bool = True
        self.power_up: str = "None" # (None / Speed). More can be added

    def can_move(self) -> None:
        """Checks if there is enough mass to move. 
            Since the player loses mass to change direction manually, 
            an if statement is used to check if there is enough mass. 
            If there is not, the player cannot change direction until it has enough mass. 
            The radius is checked for this operation. 
            """
        radius_limit: int = 10
        if (self.radius <= radius_limit): # Less than 6 means that there is no enough mass to move manually
            self.move = False # Indicates that cannot manually move
        elif (self.radius > radius_limit): # Greater than 5 means that the player can move manually
            self.move = True # Indicates that the player can move