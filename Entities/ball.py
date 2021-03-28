
class Ball:
    """Ball object are the entities in the game such as player, enemies and mass.
        Ball class is the super class of player, enemies and mass class. 
        Ball objects move around the canvas and bounce against walls. 
        """
    def __init__(self, position, velocity, radius):
        """Initializes ball object.
            
            Args:
                position (Vector): initial position of the ball
                velocity (Vector): direction of the ball
                radius (int): size of the radius 
            """
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.colour = "blue"

    def draw(self, canvas):
        """Draws ball and ball center.
            Draws circles to represent ball, it takes the initial position, radius and colour. 
            Draws point which represents center of the circle for easier compuration later. It takes initial position and colour as argument. 
            Initial position is given as Vector type for computation. Vector is converted to tuple. 
            
            Args:
                canvas (canvas): where the game play takes place.
            """
        canvas.draw_circle(self.position.get_p(), self.radius, 1, self.colour, self.colour) # Draws ball as circle
        canvas.draw_point(self.position.get_p(), self.colour) # Draws point as the center of the ball
        """Adding sprites by overlay. 
            This is more easily implemented as the removing circle will not break any dependencies. 
            The image will dynamically change size as the circle size changes. 
            """
    
    def bounce(self, normal):
        """Bounces the ball when wall is hit. 
            The ball bounces on the wall by reflecting velocity componenets along normal of the wall. 
            
            Args:
                normal (int): perpendicular of wall

            Returns:
                (Vector): components reflected on normal.
            """
        return self.velocity.reflect(normal) # Reflect velocity of ball along the normal of the wall
    
    def update(self):
        """Called by draw methods to update the position of the ball.
            Position is update by repeately adding velocity to current position.
            
            Calls: 
                add(): add the velocity to the current position to make the ball move. 
            """
        self.position.add(self.velocity) # Add the velocity to the current position to make the ball move

    def set_radius(self, radius):
        """Set a new radius size for current object. 

            Args:
                radius (int): new radius size that needs to be assigned. 
            """
        self.radius = radius