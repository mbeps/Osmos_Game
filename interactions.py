
from Game_Physics.Vector import Vector

class Interaction:
    def __init__(self, lines, player, enemy, keyboard):
        """Manages interaction between objects in the game.
            Args:
                lines (Line): walls of the game where balls bounce 
                player (Ball): player of the game
                enemy (Ball): enemy that move around the map (enemies)
            """
        self.enemy = enemy
        self.lines = lines
        self.player = player
        self.in_collsion = False
        self.keyboard = keyboard
    
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
                #^ Update Player:
        #^ Update Player:
        self.player.update()
        self.bounce(self.player)  
        
        #^ Update Enemy:
        for enemy in self.enemy: # For each ball in the ball list
            enemy.update() # Update the ball (moves the ball)
            self.bounce(enemy) # Bounce the ball if there is a collsion 
            
            self.hit(enemy, self.player) # Check collision with player
            
            for enemy2 in self.enemy: # Check collision with other enemies for each enemy in the list
                if enemy != enemy2: # Only execute when the two balls are different.#* Same balls are always colliding
                    if self.hit(enemy, enemy2): # Check if there has been a collsion between 2 balls
                        self.engulf(enemy, enemy2) # If there has been a collsion then engulf method is called


    def hit(self, ball1, ball2):
        """Detects collision between 2 balls:
            Method computes the distance between the two centers of the balls. 
            The distance is compared with the sum of the radii of the balls. 
            If the distance between the centers is less than the sum of the radii then there has been a collision. 
            
            Method will call engulf method to so that the larger ball will engulf the smaller ball.  
            
            Args:
                ball1 (Ball): enemy
                ball2 (Ball): can be enemy or player
            Returns:
                [Boolean]: whether a collision has occurred
            """
        distance = ball1.position.copy().subtract(ball2.position)
        if distance.length() < (ball1.radius + ball2.radius):
            return True

    def engulf(self, ball1, ball2):
        """Engulf ball. 
            After collision.
            The method checks which ball is larger by comparing the radii.
            The radii of the smaller ball is incremented with the radii of the larger ball. 
            The smaller ball should be removed (not implemented)
            Args:
                ball1 (Ball): main ball 
                ball2 (Ball): can be enemy or player
            """
        # Repetitive code 
        if ball1.radius > ball2.radius:
            ball1.set_radius(ball1.radius + (ball2.radius)) # The sum of the radii is set to the radius of the larger ball using setter method
            #£ Remove ball 2
            if ball2.type == "enemy": # If the smaller ball is an enemy 
                self.enemy.remove(ball2) # The ball is removed from enemy list
        else:
            ball1.set_radius(ball2.radius + ball1.radius) # The sum of the radii is set to the radius of the larger ball using setter method
            #£ Remove ball 1
            if ball1.type == "enemy": # If the smaller ball is an enemy 
                self.enemy.remove(ball1) # The ball is removed from enemy list

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