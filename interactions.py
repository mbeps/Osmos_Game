
class Interaction:
    def __init__(self, lines, player, enemy):
        """Manages interaction between objects in the game.
            Args:
                lines (Line): walls of the game where balls bounce 
                player (Ball): player of the game
                enemy (Ball): enemy that move around the map (enemies)
            """
        self.enemy = enemy
        self.lines = lines
        self.player = player
    
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
        
        #^ Draw Enemy:
        for enemy in self.enemy: # For each ball stored in the ball list
            enemy.draw(canvas) # Draw the current ball
        
        #^ Draw Player
        self.player.draw(canvas)
    
    def update(self):
        """Updates balls in the list. 
            This method handles updating the enemies stored in the enemy list and the single player. 
            Each ball (player, enemy and mass) stored is an object. 
            Update class from ball object is called which updates the position. 
            Checks if there was a collision with the wall and bounces. 

            For the the enemies, a loop will interate over the list and update each ball. 
            There is a single player which is updated normally. 
            """
        #^ Update Enemy:
        for enemy in self.enemy: # For each ball in the ball list
            enemy.update() # Update the ball (moves the ball)
            self.bounce(enemy) # Bounce the ball if there is a collsion 
        
        #^ Update Player:
        self.player.update()
        self.bounce(self.player)

    def bounce(self, ball):
        """Bounces the ball if there was a collision with the wall. 
            The distance is from the center of the ball to the center of the wall. 
            The distance between the center and wall is computed to check if there was a collision. 
            If the distance is less than the sum of the radius of the ball and the half the thickness of the wall. 
            
            The ball is the super-class of enemy, player and mass.
            This method will work for any dub-classes of ball. 
            Args:
                ball (Ball): ball object which moves
            """
        for line in self.lines: # For each line in the line list
            distance = ball.radius + (line.thickness / 2) # Sum of the wall thickness and wall size (radius)
            if line.distance(ball) < distance: # Collision if the current distance of center of ball and wall is less than the manimum distance 
                ball.bounce(line.normal) # Call the bounce method from ball object
    #£ Ball movement
    #£ Implement gravity 
    #£ Implement balls engulfing 