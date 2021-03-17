class Line:
    def __init__(self, point1, point2):
        """Creates wall object for drawing and managing wall.
            Normal is worked out bt computing line parallel to the wall and finding the perpendicular. 
            Args:
                point1 (Vector): point from which the wall is drawn
                point2 (Vector): point to where the line is drawn
            """
        self.point_a = point1
        self.point_b = point2
        self.unit = self.point_b.copy().subtract(self.point_a).normalize()
        self.normal = self.unit.copy().rotate_anti()
        self.thickness = 30
        
    def draw(self, canvas):
        """Draws line as wall. 
            Takes start point and end point as argument to draw the line between given point. Thickess and colour are also added.  
        Args:
            canvas (Canvas): where the game play takes place
        """
        canvas.draw_line(self.point_a.get_p(),
                         self.point_b.get_p(),
                         self.thickness,
                         "white")

    def distance_vector(self, position):
        """Uses shortest distance from center of ball to wall as Vector object 
            Distance is computed and line projected. 
            Args:
                position (Vector): current position of the ball 

            Returns:
                Vector: projection of the line between ball and wall
            """
        position_to_a = position.copy().subtract(self.point_a) # Shortest distance between ball and wall as vector
        return position_to_a.get_proj(self.normal) # Modulus of the distance 

    def distance(self, ball):
        """Works out distance of the ball from ball as integer. 
            Args:
                ball (Ball): ball object

            Returns:
                int: distance from ball to wall
            """
        return self.distance_vector(ball.position).length() # Shortest distance between ball and wall as length