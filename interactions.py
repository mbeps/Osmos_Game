
from Game_Physics.Vector import Vector

class Interaction:
    """Handles the interactions between game objects. 
        """
    def __init__(self, lines, player, enemy, keyboard):
        """Initializes interacation object to handle interactions between game objects.
            
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
        self.kill_counter = 0

    #^ Draw:  
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
    
    #^ Update:
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
        velocity_limit = 5
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
                gravity(ball1, ball2): attracts two balls together. 
                engult(enemy, enemy2): once there has been a collision, bigger ball will engult the smaller ball. 
            """
        for enemy in self.enemy: # For each ball in the ball list
            enemy.update() # Update the ball (moves the ball)
            self.bounce(enemy) # Bounce the ball if there is a collision 
            
            #^ Checking Collision with Player
            if self.hit_ball(self.player, enemy):
                self.engulf(self.player, enemy) # Check if there has been a collision between player and enemy
            
            #^ Checking Collision with other Enemy
            for enemy2 in self.enemy: # Check collision with other enemies for each enemy in the list
                if enemy != enemy2: # Only execute when the two balls are different.#* Same balls are always colliding
                    self.gravity(enemy, enemy2) # Gravity acts on the balls
                    if self.hit_ball(enemy, enemy2): # Check if there has been a collision between 2 enemies
                        self.engulf(enemy, enemy2) # If there has been a collision then engulf method is called

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

    #^ Mechanics:
    def gravity(self, ball1, ball2):
        """Gravity method attracts the smaller ball towards the bigger ball. 
            The method compares the radii of the two balls to find out the smaller and larger ball. 
            Gravity will act on the smaller ball when it is within a certain range of the bigger ball. 
            The velocity of both balls changes. 
            However, the velocity of the smaller ball changes more drastically than the bigger one. 
            The gravitation force of the smaller ball on the lager one us 5 times weaker. 

            Gravitational force dictates the strength of the gravity.
            The distance is computed by comparing the centers of the two balls which is used to check if smaller ball is within the range.  

            Args:
                ball1 (Ball): one of the balls on which gravity could act on
                ball2 (Ball): one of the balls on which gravity could act on
            """
        gravitational_force = 700 # Smaller means stronger
        distance_between_balls = int((ball1.position.copy().subtract(ball2.position)).length())
        larger_ball = ball1 
        smaller_ball = ball2 # Gravity acts on the smaller ball

        #^ Computing Larger & Smaller Ball
        if (ball1.radius < ball2.radius): # Works out the larger and smaller ball 
            larger_ball = ball2
            smaller_ball = ball2
        gravity_distance = larger_ball.radius * 5
        
        #^ Gravity
        if (distance_between_balls < (gravity_distance)): # Gravity acts when the smaller ball is inside the gravitational range of the bigger ball
            smaller_ball.velocity.add((larger_ball.position - smaller_ball.position).divide(gravitational_force)) # Smaller ball velocity changed
            larger_ball.velocity.add((smaller_ball.position - larger_ball.position).divide(gravitational_force * 5)) # Bigger ball velocity changed (5 times weaker)
    
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
        if (distance.length() < (ball1.radius + ball2.radius)):
            return True

    def engulf(self, ball1, ball2):
        """Engulf ball. 
            After collision.
            The sum of the radii is computed and stored in variable to be set later. 
            A fraction of the sum of radii is set to the ball as balls get large to quickly. 
            The second ball is removed from the enemies list therefore erased from the game. 
            The size of the balls are compared and assigned to variables to make code more dynamic. 
 
            Args:
                ball1 (Ball): main ball.
                ball2 (Ball): can be enemy or player.
            
            Calls:
                Ball.set_radius(sum): increases the size of the ball by setting the sum of the two balls to the bigger one. 
            """
        sum_radii = ball1.radius + ball2.radius
        larger_ball = ball1 
        smaller_ball = ball2 

        #^ Computing Larger & Smaller Ball
        if (ball1.radius < ball2.radius): # Works out the larger and smaller ball 
            larger_ball = ball2
            smaller_ball = ball1

        #^ Erasing Engulfed Ball
        larger_ball.set_radius(sum_radii / 5) # Fraction of the sum of the balls set to ball 1
        if (smaller_ball.type == "enemy"): # If the second ball is enemy than it is removed from player list
            self.enemy.remove(smaller_ball) # The ball is removed from enemy list
            self.kill_counter += 1
            print(f'Kills: {self.kill_counter}      Size: {self.player.radius}')
        elif (smaller_ball.type == "player"):
            print("Player Lost") #£ Implement the lost method

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
                Line.distance(ball): works out the distance between the ball object (player, enemy). 
                Ball.bounce(line.normal): reflect the velocity of the ball along normal to simulate a bounce. 
            """
        for line in self.lines: # For each line in the line list
            distance = ball.radius + (line.thickness / 2) + 1 # Sum of the wall thickness and wall size (radius)
            if (line.distance(ball) < distance) and (self.in_collision == False): # Collision: if the current distance of center of ball and wall is less than the manimum distance and collision not dealt with
                ball.bounce(line.normal) # Call the bounce method from ball object
                self.in_collision = True # Collision already dealt with therefore no sticky problem
            else: # Where there is no collision
                self.in_collision = False # When there is no collision then set to false so that bounce can happen later