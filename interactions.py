
class Interaction:
    def __init__(self, balls, lines):
        """Manages interaction between objects in the game.
            Args:
                balls (Ball): balls that move around the map (enemies, player, mass)
                lines (Line): walls of the game where balls bounce 
            """
        self.balls = balls
        self.lines = lines
    
    def draw(self, canvas):
        """Draws each element in list of objects. 
            Multiple objects such as balls and walls are stored in list for better management.
            Each element in the list is iterated over and drawn. 
            Update method called to update objects every second. 
            Args:
                canvas (Canvas): where the gameplay takes place
            """
        self.update()
        #^ Draw Lines:
        for line in self.lines: # For each line stored in the line list
            line.draw(canvas) # Draw the current line 
        #^ Draw Balls:
        for ball in self.balls: # For each ball stored in the ball list
            ball.draw(canvas) # Draw the current ball
    
    def update(self):
        """Updates each ball in the list. 
            Each ball stored is an object. 
            Update class from ball object is called which updates the position. 
            Checks if there was a collision with the wall and bounces. 
            """
        for ball in self.balls: # For each ball in the ball list
            ball.update() # Update the ball (moves the ball)
            self.bounce(ball) # Bounce the ball if there is a collsion 

    def bounce(self, ball):
        """Bounces the ball if there was a collision with the wall. 
            The distance is from the center of the ball to the center of the wall. 
            The distance between the center and wall is computed to check if there was a collision. 
            If the distance is less than the sum of the radius of the ball and the half the thickness of the wall. 
            Args:
                ball (Ball): ball object which moves
            """
        for line in self.lines: # For each line in the line list
            distance = ball.radius + (line.thickness / 2) # Sum of the wall thickness and wall size (radius)
            if line.distance(ball) < distance: # Collision if the current distance of center of ball and wall is less than the manimum distance 
                ball.bounce(line.normal) # Call the bounce method from ball object