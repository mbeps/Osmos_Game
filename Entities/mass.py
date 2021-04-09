from Entities.ball import Ball

class Mass (Ball):
    """Mass is ejected from player and enemy objects when the velocity is changed directly. 
        This is not ejected due to bounce or other external forces. 
        When the object itself chooses to change directions, then mass is ejected making the original ball smaller. 
        Mass is sub-class of Ball which means that it inherits the functionalities such as movement and bounce. 
        """
    def __init__ (self, position, velocity):
        """Initializes Mass object.
            Mass will have the same functionality of Ball but will have some extra.  
            
            Args:
                `Mass (Ball)`: super-class of Player. 
            
            Call:
                `super().__init__(position, velocity, radius)`: calls the constructor of the super class to initialize object.  
            """
        super().__init__(position, velocity, 2) # Use the initializer from super-class
        self.type = "Mass"
        self.colour = "Aqua"