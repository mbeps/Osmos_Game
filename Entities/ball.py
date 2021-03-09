class Ball:
    def __init__(self, position, velocity, radius, color):
        """Ball which can move, bounce and engulf. 
            All sub-classes should be able to do the same. 
            Args: 
            position (Vector): initial position of the ball in the canvas
            velocity (Vector): velocity of the ball representing the direction and magnitude of movement
            radius (int): radius of the ball
            color (str): colour of the ball in English or hex
            """
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = color
        
    def update(self):
        """Updates the position of the ball. 
            Position of the ball is updated by adding the velocity vector to the current position. 
            This method is called from draw function therefore executed 60 times per second. 
            """
        self.position.add(self.velocity)
        
    def draw(self, canvas):
        """Draws the ball in the canvas. 
            Args:
            : param: canvas ([type]): canvas where the action takes place
            """
        canvas.draw_circle(self.position.get_p(),
                           self.radius,
                           1,
                           self.color,
                           self.color)
        