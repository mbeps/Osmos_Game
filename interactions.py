
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
        self.in_collision = False
        self.keyboard = keyboard
    
    def draw(self, canvas):
        """Draws each element in list of objects. 
            Multiple objects such as balls and walls are stored in list for better management.
            Each element in the list is iterated over and drawn. 
            Update method called to update objects every second. 
            Args:
                canvas (Canvas): where the gameplay takes place. 
            Calls:
                update(): used to update the state and position of the balls. 
            """
        self.update() # Update method called to update the ball objects
        
        #^ Draw Lines:
        for line in self.lines: # For each line stored in the line list
            line.draw(canvas) # Draw the current line 
        
        #^ Draw Enemy:
        for enemy in self.enemy: # For each ball stored in the ball list
            enemy.draw(canvas) # Draw the current ball
        
        #^ Draw Player
        self.player.draw(canvas)
    
    def update_player(self):
        """Update the player. 
            Method handles updating the position of the player and bouncing upon collision with walls. 
            To update the position of the player, the update method of the player object itself is called. 
            
            Keyboard controls are used to control the player. 
            When a key is pressed, the appropriate velocity according to the direction is incremented. 
            This is handled by the player_control() method. 

            There is a single player which is updated normally. 

            Calls:
                Player.update(): handles updating the position of the player object. 
                bounce(): handles the updating the velocity of the player upon collision with wall. 
                player_control(): moves the player using keypresses by updating the position. 
            """
        self.player.update()
        self.bounce(self.player)  
        self.player_controls()

    def player_controls(self):
        """Moves the player according the key being pressed. 
            Depending the key being pressed, the velocity is incremented on the specific axes. 
            There is a limit for how fast the player can travel. 
            Once this speed limit is reached, the velocity will not be incremented. 
            """
        velocity_limit = 15
        if (self.keyboard.right) and (self.player.velocity.get_p()[0] < velocity_limit): #* Right
            self.player.velocity.add(Vector(1, 0))
        if (self.keyboard.left) and (self.player.velocity.get_p()[0] > -velocity_limit): #* Left
            self.player.velocity.add(Vector(-1,0))
        if (self.keyboard.up) and (self.player.velocity.get_p()[1] > -velocity_limit): #* Up
            self.player.velocity.add(Vector(0,-1))
        if (self.keyboard.down) and (self.player.velocity.get_p()[1] < velocity_limit): #* Down 
            self.player.velocity.add(Vector(0,+1))

    def update_enemy(self):
        """Update the enemies. 
            Method handles the updating the position of the enemies and bouncing upon collision with walls. 
            To update the position of the enemy, the update method of the enemy object itself is called. 
            Method also checks the state of the enemies by checking if there have been collisions (hit() method) with other enemies or the player. 
            If there have been collisions that the appropriate ball is engulfed. 
            
            Enemies are stored in a list of enemies. 
            This means that each enemy is the list is handles individually by iterating over the list. 

            Calls:
                Enemy.update(): handles updating the position of the enemy object. 
                bounce(enemy): handles the updating the velocity of the enemy upon collision with wall. 
                hit(enemy, enemy2): detects collision of the enemy with another ball (enemy, player).
                engult(enemy, enemy2): once there has been a collision, bigger ball will engult the smaller ball. 
            """
        for enemy in self.enemy: # For each ball in the ball list
            enemy.update() # Update the ball (moves the ball)
            self.bounce(enemy) # Bounce the ball if there is a collsion 
            
            self.hit_ball(enemy, self.player) # Check collision with player
            
            for enemy2 in self.enemy: # Check collision with other enemies for each enemy in the list
                if enemy != enemy2: # Only execute when the two balls are different.#* Same balls are always colliding
                    if self.hit_ball(enemy, enemy2): # Check if there has been a collsion between 2 balls
                        self.engulf(enemy, enemy2) # If there has been a collsion then engulf method is called

    def update(self):
        """Updates balls in the list. 
            This method handles updating the enemies stored in the enemy list and the single player. 
            Each ball (player, enemy and mass) stored is an object. 
            To update the player, @update_player() is called. 
            To update the enemies, @update_enemy() is called.  

            Calls:
                update_player(): handles updating position and state of the player. 
                update_enemy(): handles updating position and state of the enemy
            """
        self.update_player()   
        self.update_enemy()

    def hit_ball(self, ball1, ball2):
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
            print("Collided")
            return True

    def engulf(self, ball1, ball2): #! BUG: Engulf not working consistently. Sometimes does not increase size other times it gets huge
        """Engulf ball. 
            After collision.
            The method checks which ball is larger by comparing the radii.
            The radii of the smaller ball is incremented with the radii of the larger ball. 
            The smaller ball should be removed (not implemented)
            Args:
                ball1 (Ball): main ball.
                ball2 (Ball): can be enemy or player.
            Calls:
                Ball.set_radius(sum): increases the size of the ball by setting the sum of the two balls to the bigger one. 
            """
        #! Repetitive code 
        if ball1.radius > ball2.radius:
            ball1.set_radius(ball1.radius + ball2.radius) # The sum of the radii is set to the radius of the larger ball using setter method
            if ball2.type == "enemy": # If the smaller ball is an enemy 
                self.enemy.remove(ball2) # The ball is removed from enemy list
        elif ball1.radius < ball2.radius:
            ball1.set_radius(ball2.radius + ball1.radius) # The sum of the radii is set to the radius of the larger ball using setter method
            #£ Remove ball 1
            if ball1.type == "enemy": # If the smaller ball is an enemy 
                self.enemy.remove(ball1) # The ball is removed from enemy list

    def bounce(self, ball):
        """Bounces the ball if there was a collision with the wall. 
            The maximum distance is from the center of the ball to the center of the wall. 
            The distance between the center and wall is computed to check if there was a collision. 
            If the distance between the wall and the ball is less than the maximum distance then there has been a collision. 

            in_collision variable keeps track of whether there has been a collision before. 
            This is done to prevent the sticky problem where the ball is stuck in the wall. 
            If there is a previous collision and another one happens at the same time, then collision is not handles therefore no bounce. 
            After the collision takes place and there is no other collision, then the variable is set to false so that the next collision can be handled. 
            
            The ball is the super-class of enemy, player and mass.
            This method will work for any dub-classes of ball. 
            
            Args:
                ball (Ball): ball object which moves
            Calls: 
                lines(distance): works out the distance between the ball object (player, enemy). 
                Ball.bounce(line.normal): reflect the velocity of the ball along normal to simulate a bounce. 
            """
        for line in self.lines: # For each line in the line list
            distance = ball.radius + (line.thickness / 2) + 1 # Sum of the wall thickness and wall size (radius)
            if (line.distance(ball) < distance) and (self.in_collision == False): # Collision: if the current distance of center of ball and wall is less than the manimum distance and collision not dealt with
                ball.bounce(line.normal) # Call the bounce method from ball object
                self.in_collision = True # Collision already dealt with therefore no sticky problem
            else: # Where there is no collision
                self.in_collision = False # When there is no collision then set to false so that bounce can happen later