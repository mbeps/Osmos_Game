
from Game_Control.Vector import Vector
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Entities.power_ups import Power_Up
from Entities.mass import Mass
import random

class Interaction:
    """Handles the interactions between game objects. 
        """
    def __init__(self, lines, player, enemy, time, keyboard, frame):
        """Initializes interacation object to handle interactions between game objects.
            
            Args:
                lines (Line): walls of the game where balls bounce 
                player (Ball): player of the game
                enemy (Ball): enemy that move around the map (enemies)
                time (int): time limit for the game
                keyboard (Keyboard): handles keyboard input to make the player move
                frame (Frame): interactive window where game play takes place
            """
        #^ Entities:
        self.enemy = enemy
        self.player = player
        self.power_ups = []
        # self.mass = [Mass(Vector(500, 300), Vector(2,1), 2)]
        self.mass = []
        self.lines = lines

        #^ Environment:
        self.in_collision = False
        self.keyboard = keyboard 
        self.kill_counter = 0
        self.frame = frame
        
        #^ Timers:
        self.time_limit = time # The limit for which the game will run 
        self.time_count = simplegui.create_timer(1000, self.countdown) # Counts how many times method is called. Used for computing one second. 
        self.time_count.start()
        self.player_power_up_timer = simplegui.create_timer(10_000, self.reset_player_power_up) # How long the power up will last
        self.player_power_up_timer.start()
        self.power_up_timer_create = simplegui.create_timer(20_000, self.add_power_up) # Create a power up object every set time
        self.power_up_timer_create.start()

    #^ Draw:  
    def draw(self, canvas):
        """Draws each element in list of objects. 
            Method calls other draw methods for the specific objects. 
            
            Args:
                canvas (Canvas): where the gameplay takes place. 
            
            Calls:
                update(): used to update the state and position of the balls. 
                draw_player(canvas): draws the player in the canvas
                draw_enemy(canvas): draws the enemies in the canvas
                draw_mass(canvas): draws the mass in the canvas
                draw_power_ups(canvas): draw the powerups in the canvas
                draw_map(canvas): draws game map in the canvas
                draw_store(canvas): draws player scores in the canvas
            """
        self.update() # Update method called to update the ball objects
        self.draw_player(canvas)
        self.draw_enemy(canvas)
        self.draw_mass(canvas)
        self.draw_power_ups(canvas)
        self.draw_map(canvas)
        self.draw_score(canvas)
    
    def draw_player(self, canvas):
        """Draws the player. 
            

            Args:
                canvas (Canvas): where the game play takes place
            """
        self.player.draw(canvas)

    def draw_enemy(self, canvas):
        """Draws the enemies. 
            There are multiple enemy objects stored in the list. 
            A for loop is used to iterate over each enemy in the list. 
            For each enemy, the draw method of the current enemy object is called. 

            Args:
                canvas (Canvas): where the game play takes place
            """
        for enemy in self.enemy: # For each ball stored in the ball list
            enemy.draw(canvas) # Draw the current ball

    def draw_mass(self, canvas):
        """Draws the enemies. 
            There are multiple mass objects stored in the list. 
            A for loop is used to iterate over each mass in the list. 
            For each mass, the draw method of the current mass object is called. 

            Args:
                canvas(Canvas): where the game play takes place
            """
        for mass in self.mass:
            mass.draw(canvas)

    def draw_power_ups(self, canvas):
        """Draws the power ups.
            There are multiple power ups objects stored in the list. 
            A for loop is used to iterate over each power up in the list. 
            For each enemy, the draw method of the current power up object is called. 

            Args:
                canvas (Canvas): where the game play takes place
            """
        for power_up in self.power_ups:
            power_up.draw(canvas)    

    def draw_map(self, canvas):
        """Draws the walls around the canvas. 
            The walls (thick lines) are used to as boundaries for ball objects. 
            The ball objects bounce upon collision with the wall. 
            There are multiple walls which are stored in the list. 
            A for loop is used to iterate over the walls stored in the list. 
            For each wall object, the draw method of the wall is called. 

            Args:
                canvas (Canvas): where the game play takes place
            """
        for line in self.lines: # For each line stored in the line list
            line.draw(canvas) # Draw the current line 

    def draw_score(self, canvas):
        """Draws score as text. 
            Draws the number of enemies killed (engulfed) by the player. 
            Draws the size of the player by using the radius of the player. 
            Draws the time remaining.

            If the time limit is unlimited or greater than 10, then the text will be green indicating that there is plenty of time. 
            If the time is less than 10, then the text will be red indicating that the time is running out. 

            These are all drawn in on line along the top wall. 

            Args:
                canvas (Canvas): where the game play takes place
            """
        if (self.time_limit < 0 ):
            remaining_time = "Unlimited"
        else:
            remaining_time = self.time_limit

        if (self.time_limit > 10 or self.time_limit < 0):
            colour = "green"
        else:
            colour = "red"
           
        canvas.draw_text(f'Kills: {self.kill_counter}      Size: {self.player.radius}      Time: {remaining_time}', (20, 13), 18, colour)
    
    #^ Update:
    def update(self):
        """Updates balls in the list. 
            This method handles updating the enemies stored in the enemy list and the single player. 
            Each ball (player, enemy and mass) stored is an object. 
            Enemies and players are updated by colling their respective update method. 
            
            Function to check if game is over is called for checking.
            This function checks whether the game is over and executes the appropriate actions. 

            Calls:
                update_player(): handles updating position and state of the player. 
                update_enemy(): handles updating position and state of the enemy.
                update_mass(): handles updating position and state of the mass. 
                update_power_ups(): handles checking collision with player object. 
                game_finish(): checks whether the game is over (if player has lost or won). 
            """
        self.update_player()   
        self.update_enemy()
        self.update_mass()
        self.update_power_ups()
        self.game_finish()

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

            When the player object receives a power up, the speed limit is increases. 
            """
        velocity_limit = 5

        if self.player.faster == True: # Set to true when player receives power up
            velocity_limit = 10

        if (self.keyboard.right) and (self.player.velocity.get_p()[0] < velocity_limit): #* Right
            self.player.velocity.add(Vector(1, 0))
            # self.eject_mass()
        if (self.keyboard.left) and (self.player.velocity.get_p()[0] > -velocity_limit): #* Left
            self.player.velocity.add(Vector(-1,0))
            # self.eject_mass()
        if (self.keyboard.up) and (self.player.velocity.get_p()[1] > -velocity_limit): #* Up
            self.player.velocity.add(Vector(0,-1))
            # self.eject_mass()
        if (self.keyboard.down) and (self.player.velocity.get_p()[1] < velocity_limit): #* Down 
            self.player.velocity.add(Vector(0,+1))
            # self.eject_mass()

    def eject_mass(self): #! Not working
        """Each time the player manually moves mass is created. 
            Mass will move in the opposite direction to emulate Newton's Laws. 
            """
        position = Vector(self.player.position.get_p()[0] + self.player.radius + 3, self.player.position.get_p()[1] + self.player.radius + 3)
        angle = position.angle(self.player.velocity)
        position = position.rotate(180 + angle) #! Being spaawned outside the canvas
        velocity = Vector(-self.player.velocity.get_p()[0], -self.player.velocity.get_p()[1])

        self.mass.append(Mass(position, velocity, 2, self.player.colour))

    def update_enemy(self):
        """Update the enemies. 
            Method handles the updating the position of the enemies and bouncing upon collision with walls. 
            To update the position of the enemy, the update method of the enemy object itself is called. 
            Method also checks the state of the enemies by checking if there have been collisions (`hit()` method) with other enemies or the player. 
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
        for enemy in self.enemy: # For each enemy object in the enemy list
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

            #^ Checking Collision with Mass:
            for mass in self.mass: # For loop used to interate over each mass object in the list
                self.gravity(enemy, mass) # Gravity acts on the mass and enemy
                if self.hit_ball(enemy, mass): # Check if there has been a collision between current mass and current enemy
                    self.engulf(enemy, mass) # If true then mass is engulfed by the enemy

    def update_mass(self):
        """Update the mass. 
            Method handles updating the position of the mass and bouncing upon collision with walls. 
            To update the position of the mass, the update method of the mass object itself is called. 
            Method also checks the state of the mass by checking if there have been collisions (`hit()` method) with enemies or the player. 
            Mass cannot engulf another mass to prevent mass from engulfing player and enemies. Mass is always engulfed. 
            If there has been a collision, then the mass object is engulfed. 
            """
        for mass in self.mass: # For each mass object in the mass list
            mass.update() # Move the ball
            self.bounce(mass) # Bounce mass upon collision with wall
            
            if self.hit_ball(mass, self.player): # Check if there has been collision with player
                self.engulf(self.player, mass) # If true, then the player object will engulf the mass
    
    def update_power_ups(self):
        """Checking of the power up object has collided with player object. 
            A for loop is used to iterate over the list of powerups. 
            For each power up object, it is checked whether there has been a collision. 
            If there has a been a collision, then the player object receives a power up and the current power up object is removed from the list. 
            """
        for power_up in self.power_ups:
            if self.hit_ball(self.player, power_up):
                self.power_ups.remove(power_up)
                self.player.faster = True

    def add_power_up(self):
        """Creates power up objects. 
            This is called from `self.power_up_timer_create` which will create a new power up at a set time interval. 
            The maximum number of power ups is 5 after which point no more power ups will be added. 
            An if statement is used if the number of power ups (in the list) has reached the limit. 
            """
        if (len(self.power_ups) < 5):
            self.power_ups.append(Power_Up(Vector(random.randint(5, 790), random.randint(5, 490)), 5))

    def countdown(self):
        """Counts down the timer set.
            Uses the counter to keep track of how many times the method is called. 
            The modulus is used to compute one second based on the counter.
            For every second, the time limit is decremented. 
            """
        self.time_limit -= 1

    def reset_player_power_up(self):
        """Resets player power up. 
            Called from `self.player_power_up_timer` timer. 
            """
        self.player.faster = False

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
            
            If the second (smaller) ball is the enemy, 
            then it is removed from the list 
            and score is incremented. 

            If the second (smaller) ball is player, 
            then player is dead which means that the game is list. 

            If the second (smaller) ball is the mass, 
            then it is removed from the list. 
            Mass will never eat another entity as mass does not get larger because it does not engulf other mass. 
 
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
        larger_ball.set_radius(sum_radii) # Fraction of the sum of the balls set to ball 1
        if (smaller_ball.type == "enemy"): # If the ball eaten (smaller ball) was the enemy
            self.enemy.remove(smaller_ball) # The ball is removed from enemy list
            self.kill_counter += 1 # Increment kill counter to be displayed on canvas on another method
        elif (smaller_ball.type == "player"): # If the ball eaten (smaller ball) was the player
            self.player.alive = False # A method will check this and terminate the game   
        elif (smaller_ball.type == "mass"): # Mass is removed from list
            self.mass.remove(smaller_ball)

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

    #^ Game:
    def game_finish(self):
        """Handles the end of game.
            Detects whether the game is finished. 
            Once the game is finished, the game will be terminated and the appropriate message will be displayed. 
            This is done by checking whether all the enemies are dead or the player is dead. 
            
            To check if all the enemies are dead, the size of the list which contains the enemies us checked.
            If the length of the list is 0 (empty list) then all the enemies are dead and the player has won. 

            To check if the player is dead, the field which keeps track if it alive is checked. 
            If the field 'alive' is false, then the player is dead and therefore has lost. 

            The player will lose if the it has not killed all the enemies by the time the timer runs out. 
            When the timer reaches 0, the timer has run out. 
            For the timer to be unlimited, the timer is set to be less than 0 (-1) which means that the condidion is never met. 

            Checks whether the letter 'e' has been pressed. 
            If it has been pressed, the game will be terminated. 

            Calls:
                `stop()`: terminates the handlers (timer, frame)
            """
        if (len(self.enemy) == 0):
            self.stop()
            print("You Won")
        elif (self.player.alive == False):
            self.stop()
            print("Game Over. You Lost.")
        elif (self.time_limit == 0):
            print("Ran Out of Time. You Lost")
            self.stop()
        elif (self.keyboard.e):
            print("Game Exited")
            self.stop()

    def stop(self):
        """Terminates all the handlers.
            All the timers and the frame are terminated. 
            This terminates the game. 
            """
        self.frame.stop()
        self.power_up_timer_create.stop()
        self.time_count.stop()
        self.player_power_up_timer.stop()

# A bug is present where the enemies will infinitely get larger if the plater is eaten.
# Terminating the game is a workaround. 