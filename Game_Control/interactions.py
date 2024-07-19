from math import floor
from Entities.ball import Ball
from Entities.enemy import Enemy
from Entities.player import Player
from Game_Control.Vector import Vector
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Entities.power_ups import Power_Up
from Entities.mass import Mass
import random
from Game_Control.keyboard import Keyboard
from SimpleGUICS2Pygame.simpleguics2pygame import Canvas, Timer
from typing import cast


from Maps.line import Line


class Interaction:
    """Handles the interactions between game objects. 
        """
    def __init__(self, lines: list[Line], player: Player, enemies: list[Enemy], time: int, keyboard: Keyboard, frame:simplegui.Frame) -> None:
        """Initializes interaction object to handle interactions between game objects.
            
            Args:
                `lines (Line)`: walls of the game where balls bounce.
                `player (Ball)`: player of the game.
                `enemy (Ball)`: enemy that move around the map (enemies).
                `time (int)`: time limit for the game.
                `keyboard (Keyboard)`: handles keyboard input to make the player move.
                `frame (Frame)`: interactive window where game play takes place.
            """
        #^ Entities:
        self.enemy: list[Enemy] = enemies
        self.player: Player = player
        self.power_ups: list[Power_Up] = []
        self.mass: list[Mass] = []
        self.lines: list[Line] = lines

        #^ Environment:
        self.keyboard: Keyboard = keyboard 
        self.kill_counter: int = 0
        self.frame: simplegui.Frame = frame
        
        #^ Timers:
        self.time_limit: int = time # The limit for which the game will run 
        self.time_count: Timer = simplegui.create_timer(1000, self.countdown) # Counts how many times method is called. Used for computing one second. 
        self.time_count.start()
        self.player_power_up_timer: Timer = simplegui.create_timer(10_000, self.reset_player_power_up) # How long the power up will last
        self.power_up_timer_create: Timer = simplegui.create_timer(15_000, self.add_power_up) # Create a power up object every set time
        self.power_up_timer_create.start()
        self.enemy_split_timer: Timer = simplegui.create_timer(30_000, self.enemy_split) # Split the enemy every minute
        self.enemy_split_timer.start()

    #^ Draw:  
    def draw(self, canvas) -> None:
        """Draws each element in list of objects. 
            Method calls other draw methods for the specific objects. 
            
            Args:
                `canvas (Canvas)`: where the gameplay takes place. 
            
            Calls:
                `self.update()`: used to update the state and position of the balls. 
                `self.draw_player(canvas)`: draws the player in the canvas
                `self.draw_enemy(canvas)`: draws the enemies in the canvas
                `self.draw_mass(canvas)`: draws the mass in the canvas
                `self.draw_power_ups(canvas)`: draw the powerups in the canvas
                `self.draw_map(canvas)`: draws game map in the canvas
                `self.draw_store(canvas)`: draws player scores in the canvas
            """
        self.update() # Update method called to update the ball objects
        self.draw_player(canvas)
        self.draw_enemy(canvas)
        self.draw_mass(canvas)
        self.draw_power_ups(canvas)
        self.draw_map(canvas)
        self.draw_score(canvas)
    
    def draw_player(self, canvas) -> None:
        """Draws the player in the canvas.
            The player is drawn only if the it is alive. 
            If the player is not alive, then the it will not be drawn. 
            An if statement is used to check whether the player is alive. 
            
            Args:
                `canvas (Canvas)`: where the game play takes place.

            Calls:
                `Player.draw(canvas)`: calls the draw method from Player object to draw player object. 
            """
        if (self.player.alive): # Check whether player object drawn if alive
            self.player.draw(canvas)

    def draw_enemy(self, canvas: Canvas) -> None:
        """Draws the enemies. 
            There are multiple enemy objects stored in the list. 
            A for loop is used to iterate over each enemy in the list. 
            For each enemy, the draw method of the current enemy object is called. 

            Args:
                `canvas (Canvas)`: where the game play takes place

            Calls:
                `Enemy.draw(canvas)`: calls the draw method from Enemy object to draw player object.
            """
        for enemy in self.enemy: # For each ball stored in the ball list
            enemy.draw(canvas) # Draw the current ball

    def draw_mass(self, canvas: Canvas) -> None:
        """Draws the enemies. 
            There are multiple mass objects stored in the list. 
            A for loop is used to iterate over each mass in the list. 
            For each mass, the draw method of the current mass object is called. 

            Args:
                `canvas(Canvas)`: where the game play takes place. 

            Calls:
                `Mass.draw(canvas)`: calls the draw method from Mass object to draw mass object.
            """
        for mass in self.mass: # Iterates over each mass in the list
            mass.draw(canvas)

    def draw_power_ups(self, canvas: Canvas) -> None:
        """Draws the power ups.
            There are multiple power ups objects stored in the list. 
            A for loop is used to iterate over each power up in the list. 
            For each power up, the draw method of the current power up object is called. 

            Args:
                `canvas (Canvas)`: where the game play takes place. 

            Calls:
                `Power_Up.draw(canvas)`: calls the draw method from Power_Up object to draw power up object.
            """
        for power_up in self.power_ups:
            power_up.draw(canvas)    

    def draw_map(self, canvas: Canvas) -> None:
        """Draws the walls around the canvas. 
            The walls (thick lines) are used to as boundaries for ball objects. 
            The ball objects bounce upon collision with the wall. 
            There are multiple walls which are stored in the list. 
            A for loop is used to iterate over the walls stored in the list. 
            For each wall object, the draw method of the wall is called. 

            Args:
                `canvas (Canvas)`: where the game play takes place. 

            Calls:
                `Line.draw(canvas)`: calls the draw method from Line object to draw line object.
            """
        for line in self.lines: # For each line stored in the line list
            line.draw(canvas) # Draw the current line 

    def draw_score(self, canvas: Canvas) -> None:
        """Draws score as text. 
            Draws the number of enemies killed (engulfed) by the player. 
            Draws the size of the player by using the radius of the player. 
            Draws the time remaining. 
            Draws the type of the power up currently being used. 

            If the time limit is unlimited or greater than 10, then the text will be green indicating that there is plenty of time. 
            If the time is less than 10, then the text will be red indicating that the time is running out. 

            These are all drawn in on line along the top wall. 

            Args:
                `canvas (Canvas)`: where the game play takes place. 
            """
        #^ Checks Time Limit:
        remaining_time: int | str
        if (self.time_limit < 0): # Decrementing from 0 means that the time limit is never reached
            remaining_time = "Unlimited"
        else: # If there is a time limit then it is displayed
            remaining_time = self.time_limit

        #^ Checks Remaining Time: 
        if (self.time_limit > 10 or self.time_limit < 0): # If the time remaining is unlimited or more than 10 seconds
            colour = "green"
        else:
            colour = "red" # If the time remaining is 0 to 9 seconds
           
        canvas.draw_text(f'Kills: {self.kill_counter}       Size: {round(self.player.radius, 1)}      Time: {remaining_time}      Power Up: {self.player.power_up}', (20, 13), 18, colour)
    
    #^ Update:
    def update(self) -> None:
        """Updates balls in the list. 
            This method handles updating the enemies stored in the enemy list, the single player, the mass stored in a list, and the power ups stored in a list. 
            Each ball (player, enemy and mass) stored is an object. 
            Enemies, players, mass, and power ups are updated by calling their respective update methods. 
            
            Function to check if game is over is called for checking.
            This function checks whether the game is over and executes the appropriate actions. 

            Calls:
                `self.update_player()`: handles updating position and state of the player. 
                `self.update_enemy()`: handles updating position and state of the enemy.
                `self.update_mass()`: handles updating position and state of the mass. 
                `self.update_power_ups()`: handles checking collision with player object. 
                `self.game_finish()`: checks whether the game is over (if player has lost or won). 
            """
        self.update_player()   
        self.update_enemy()
        self.update_mass()
        self.update_power_ups()
        self.game_finish()

    def update_player(self) -> None:
        """Update the player. 
            Method handles updating the position of the player and bouncing upon collision with walls. 
            To update the position of the player, the update method of the player object itself is called. 
            
            Keyboard controls are used to control the player. 
            When a key is pressed, the appropriate velocity according to the direction is incremented. 
            This is handled by the `player_control()` method. 

            Since the player loses mass to change direction manually, 
            `Player.can_move()` is called to check if there is enough mass to move. 

            There is a single player which is updated normally. 

            Calls:
                `Player.update()`: handles updating the position of the player object. 
                `Player.can_move()`: checks whether there is enough mass to move. 
                `self.bounce()`: handles the updating the velocity of the player upon collision with wall. 
                `self.player_control()`: moves the player using keypresses by updating the position. 
            """
        self.player.update()
        self.bounce(self.player)  
        self.player_controls()
        self.player.can_move()

    def player_controls(self) -> None:
        """Moves the player according the key being pressed. 
            Depending the key being pressed, the velocity is incremented on the specific axes. 
            There is a limit for how fast the player can travel. 
            
            Once this speed limit is reached, the statement is not executed. 
            This means that the speed will not longer be increased as velocity will not be incremented and 
            mass will not be ejected. 

            Additionally, if the player runs out of mass, then it cannot change velocity. 
            The method checks whether the player can move using an if statement. 

            When the player object receives a power up, the speed limit is increases. 

            Calls: 
                `self.eject_mass()`: ejects the mass from player when position is updated manually.
            """
        velocity_limit = 5

        #^ Check Power Ups:
        if (self.player.power_up == "Speed"): # Specify the power up received
            velocity_limit = 10

        #^ Keyboard Controls:
        if (self.keyboard.right) and (self.player.velocity.get_p()[0] < velocity_limit) and (self.player.move): #* Right
            self.player.velocity.add(Vector(1, 0))
            self.eject_mass()
        if (self.keyboard.left) and (self.player.velocity.get_p()[0] > -velocity_limit) and (self.player.move): #* Left
            self.player.velocity.add(Vector(-1, 0))
            self.eject_mass()
        if (self.keyboard.up) and (self.player.velocity.get_p()[1] > -velocity_limit) and (self.player.move): #* Up
            self.player.velocity.add(Vector(0, -1))
            self.eject_mass()
        if (self.keyboard.down) and (self.player.velocity.get_p()[1] < velocity_limit) and (self.player.move): #* Down 
            self.player.velocity.add(Vector(0, 1))
            self.eject_mass()

    def eject_mass(self) -> None: 
        """Each time the player manually moves mass is created. 
            Mass will move in the opposite direction to emulate Newton's Laws. 

            The mass is spawned on the opposite side of the direction of the player object. 
            The formula `(player radius + mass radius) × (- player velocity / |player velocity|)` finds the opposite circumference which is the position of mass object. 

            When player moves in the opposite direction, the velocity of the mass could become 0 which will cause error. 
            An if statement checks if the `x` or `y` are 0 and increments if condition is met. #

            Once the calculation is complete, a mass object is added to the list. 
            It takes the position calculated before, the negative velocity of player (opposite direction) and the colour. 
            
            The player loses the mass which.
            Each move will cause the player to lose 1 from the radius. 
            Each mass is 0.2 radii and 5 are created for each movement. 
            """
        mass_velocity: Vector = self.player.velocity.copy().negate() # Velocity of the mass is the opposite direction from the player, therefore velocity is negated. 
        mass_radius: float = 0.2

        if (mass_velocity.get_p()[0] == 0): # Checks if the x component of the velocity is 0
            mass_velocity += Vector(1, 0) # Increment 1 to x component to avoid errors later on
        elif (mass_velocity.get_p()[1] == 0): # Checks if the y component of the velocity is 0
            mass_velocity += Vector(0, 1) # Increment 1 to y component to avoid errors later on

        mass_velocity_unit: Vector = mass_velocity.copy().divide(mass_velocity.length()) # Unit Vector = Vector / |Vector|
        mass_position: Vector = ((self.player.radius + mass_radius) * mass_velocity_unit) + self.player.position.copy() # Computes the actual position of the mass

        self.mass.append(Mass((mass_position), mass_velocity, mass_radius)) # Creates a new mass object which is added to the list
        self.player.set_radius(self.player.radius - mass_radius) # Decrements the radius of the player 

    def update_enemy(self) -> None:
        """Update the enemies. 
            Method handles the updating the position of the enemies and bouncing upon collision with walls. 
            To update the position of the enemy, the update method of the enemy object itself is called. 
            Method also checks the state of the enemies by checking if there have been collisions (`hit()` method) with other enemies, mass or the player. 
            When enemies get close to other enemies or mass, gravity is applied on the two objects. 
            If there have been collisions that the appropriate ball is engulfed. 
            
            Enemies are stored in a list of enemies. 
            This means that each enemy is the list is handles individually by iterating over the list. 
            A for loop is used to iterate over each enemy and carry out the operations and checks mentioned before. 

            Calls:
                `Enemy.update()`: handles updating the position of the enemy object. 
                `self.bounce(enemy)`: handles the updating the velocity of the enemy upon collision with wall. 
                `self.hit(enemy, enemy2)`: detects collision of the enemy with another ball (enemy, player).
                `self.gravity(ball1, ball2)`: attracts two balls together. 
                `self.engulf(enemy, enemy2)`: once there has been a collision, bigger ball will engulf the smaller ball. 
            """
        for enemy in self.enemy: # For each enemy object in the enemy list
            enemy.update() # Update the ball (moves the ball)
            self.bounce(enemy) # Bounce the ball if there is a collision 
            
            #^ Checking Collision with Player
            if self.hit_ball(self.player, enemy): # Check if there has been a collision between player and enemy
                self.engulf(self.player, enemy) # If true, the one of the two objects is engulfed
            
            #^ Checking Collision with other Enemy
            for enemy2 in self.enemy: # Check collision with other enemies for each enemy in the list
                if enemy != enemy2: # Only execute when the two balls are different.#* Same balls are always colliding
                    self.gravity(enemy, enemy2) # Gravity acts on the balls
                    if self.hit_ball(enemy, enemy2): # Check if there has been a collision between 2 enemies
                        self.engulf(enemy, enemy2) # If there has been a collision then engulf method is called

            #^ Checking Collision with Mass:
            for mass in self.mass: # For loop used to iterate over each mass object in the list
                self.gravity(enemy, mass) # Gravity acts on the mass and enemy
                if self.hit_ball(enemy, mass): # Check if there has been a collision between current mass and current enemy
                    self.engulf(enemy, mass) # If true then mass is engulfed by the enemy

    def enemy_split(self) -> None:
        """Splits the enemy objects into smaller ones. 
            When the method is called, a random enemy will be split. 
            This is done by splitting a selecting a random number from the first to last index from list where enemies are stored. 
            If the radius is too small, then the enemy is not split. Otherwise, the enemies will become too small. 

            When splitting, the enemy will become slower. 
            To counter this, the velocity is multiplied. 
            This also means that the new enemy will be faster. 
            The enemies will get exponentially fast. 
            A limiter is implemented so that the velocity is not increased once the speed (not velocity only magnitude) limit is reached. 

            The radius of the new enemy object is random from range `5` to 5 less than the radius of the current enemy. 
            The range cannot be too small otherwise the new enemy will be too small and the current enemy will not decrease that much. 
            Once a radius is picked, the radius of the current enemy will be decreased by the same amount. 

            The new enemy is spawned on the opposite side of the direction of the current enemy object. 
            The formula `(current enemy radius + new enemy radius) × (-current velocity / |current velocity|)` finds the opposite circumference which is the position of new enemy object. 

            When current enemy moves in the opposite direction, the velocity of the new enemy could become 0 which will cause error. 
            An if statement checks if the `x` or `y` are 0 and increments if condition is met. 

            Once the calculation is complete, a new enemy object is added to the list. 
            It takes the position calculated before, the negative velocity of current enemy (opposite direction) and the radius. 
            """
        #^ Random Enemy:
        enemy: Enemy = self.enemy[random.randint(0, len(self.enemy) - 1)]
        
        #^ Splitting Enemy:
        if (enemy.radius >= 15): # Only splits when the radius is less than 15
            if (enemy.velocity.length() < 5): # Checks if the speed is less than 5
                enemy.velocity.multiply(1.5) # Multiply the speed 1.5 to supplement the decrease in speed  
            
            mass_velocity: Vector = enemy.velocity.copy().negate() 
            new_enemy_radius:int = random.randint(5, floor(enemy.radius - 5)) # New enemy radius is random

            if (mass_velocity.get_p()[0] == 0): # Checks if the x component of the velocity is 0
                mass_velocity += Vector(1, 0) # Increment 1 to x component to avoid errors later on
            elif (mass_velocity.get_p()[1] == 0): # Checks if the y component of the velocity is 0
                mass_velocity += Vector(0, 1) # Increment 1 to y component to avoid errors later on

            mass_velocity_unit: Vector = mass_velocity.copy().divide(mass_velocity.length()) # Unit Vector = Vector / |Vector|
            mass_position: Vector = ((enemy.radius + new_enemy_radius) * mass_velocity_unit) + enemy.position.copy() # Computes the actual position of the new enemy

            self.enemy.append(Enemy(mass_position, mass_velocity, new_enemy_radius)) # Creates a new enemy object which is added to the list
            enemy.set_radius(enemy.radius - new_enemy_radius) # Decrements the radius of the player 
        
    def update_mass(self) -> None:
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
    
    def update_power_ups(self) -> None:
        """Checking of the power up object has collided with player object. 
            A for loop is used to iterate over the list of powerups. 
            For each power up object, it is checked whether there has been a collision. 
            If there has a been a collision, then the player object receives a power up and the current power up object is removed from the list. 
            Once the player receives the power up, the timer which defines how long it will last will be created. 
            """
        for power_up in self.power_ups: # Iterate over the power up objects in the list
            if self.hit_ball(self.player, power_up): # Check if the current power up has collided with player
                self.power_ups.remove(power_up) # Remove the power up from the list 
                self.player.power_up = "Speed" # Makes the player faster
                self.player_power_up_timer.start() # Starts the timer for how long the power up lasts for

    def add_power_up(self) -> None:
        """Creates power up objects. 
            This is called from `self.power_up_timer_create` which will create a new power up at a set time interval. 
            The maximum number of power ups is 5 after which point no more power ups will be added. 
            An if statement is used if the number of power ups (in the list) is bellow the maximum limit. 
            If it is bellow the limit, then new power up objects are spawned at random locations within the map. 
            """
        max_number_power_ups: int = 5
        if (len(self.power_ups) < max_number_power_ups): # Checks if the number of power ups in the map is less than the maximum allowed
            self.power_ups.append(Power_Up(Vector(random.randint(5, 790), random.randint(5, 490)))) # Create a new power up at a random place within the map

    def countdown(self) -> None:
        """Counts down the timer set.
            This method decrements the time limit for the game. 
            Each time this is called from `self.time_count` the time limit decreases. 
            Other methods will check this `self.time_limit` to execute the required actions. 
            """
        self.time_limit -= 1

    def reset_player_power_up(self) -> None:
        """Resets player power up. 
            Called from `self.player_power_up_timer` timer. 
            """
        self.player.power_up = "None" # Reset the power up (no more power up)
        self.player_power_up_timer.stop() # Stops the timer (until a new power up is received) 

    #^ Mechanics:
    def gravity(self, ball1: Ball, ball2: Ball) -> None:
        """Gravity method attracts the smaller ball towards the bigger ball. 
            The method compares the radii of the two balls to find out the smaller and larger ball. 
            Gravity will act on the smaller ball when it is within a certain range of the bigger ball. 
            The velocity of both balls changes. 
            However, the velocity of the smaller ball changes more drastically than the bigger one. 
            The gravitation force of the smaller ball on the lager one us 5 times weaker. 

            Gravitational force dictates the strength of the gravity.
            The distance is computed by comparing the centers of the two balls which is used to check if smaller ball is within the range.  

            Args:
                `ball1 (Ball)`: one of the balls on which gravity could act on.
                `ball2 (Ball)`: one of the balls on which gravity could act on.
            """
        gravitational_force: int = 700 # Smaller means stronger
        distance_between_balls: int = int((ball1.position.copy().subtract(ball2.position)).length())
        larger_ball: Ball = ball1 
        smaller_ball: Ball = ball2 # Gravity acts on the smaller ball

        #^ Computing Larger & Smaller Ball
        if (ball1.radius < ball2.radius): # Works out the larger and smaller ball 
            larger_ball = ball2
            smaller_ball = ball2
        gravity_distance: float = larger_ball.radius * 5
        
        #^ Gravity
        if (distance_between_balls < (gravity_distance)): # Gravity acts when the smaller ball is inside the gravitational range of the bigger ball
            smaller_ball.velocity.add((larger_ball.position - smaller_ball.position).divide(gravitational_force)) # Smaller ball velocity changed
            larger_ball.velocity.add((smaller_ball.position - larger_ball.position).divide(gravitational_force * 5)) # Bigger ball velocity changed (5 times weaker)
    
    def hit_ball(self, ball1: Ball , ball2: Ball) -> bool:
        """Detects collision between 2 balls. 
            Method computes the distance between the two centers of the balls. 
            The distance is compared with the sum of the radii of the balls. 
            If the distance between the centers is less than the sum of the radii then there has been a collision. 
            
            Method will call engulf method to so that the larger ball will engulf the smaller ball.  
            
            Args:
                `ball1 (Ball)`: enemy.
                `ball2 (Ball)`: can be enemy, player or mass.
            
            Returns:
                `(Boolean)`: whether a collision has occurred.
            """
        distance: Vector = ball1.position.copy().subtract(ball2.position)
        return (distance.length() < (ball1.radius + ball2.radius)) # Check if the distance from the centres is less than the sum of radii 

    def engulf(self, ball1: Ball, ball2: Ball) -> None:
        """Engulf ball. 
            After collision.
            The sum of the radii is computed and stored in variable to be set later. 
            A fraction of the sum of radii is set to the ball as balls get large to quickly. 
            
            If the second (smaller) ball is the enemy, 
            then it is removed from the list. 
            `self.increment_score()` is called to increment the score, 
            this method checks whether the larger ball was the player and the smaller ball was the enemy. 
            It is possible that both balls were enemies which means that the kill counter cannot be incremented. 

            If the second (smaller) ball is player, 
            then player is dead which means that the game is list. 

            If the second (smaller) ball is the mass, 
            then it is removed from the list. 
            Mass will never eat another entity as mass does not get larger because it does not engulf other mass. 

            Args:
                `ball1 (Ball)`: main ball.
                `ball2 (Ball)`: can be enemy or player.
            
            Calls:
                `Ball.set_radius(sum)`: increases the size of the ball by setting the sum of the two balls to the bigger one. 
                `self.increment_score(larger_ball, smaller_ball)`: increments the score only if the player killed / engulfed the enemy.  
            """
        sum_radii: float = ball1.radius + ball2.radius
        larger_ball: Ball = ball1 
        smaller_ball: Ball = ball2 

        #^ Computing Larger & Smaller Ball
        if (ball1.radius < ball2.radius): # Works out the larger and smaller ball 
            larger_ball = ball2
            smaller_ball = ball1

        #^ Erasing Engulfed Ball
        larger_ball.set_radius(sum_radii) # Fraction of the sum of the balls set to ball 1
        
        if (smaller_ball.type == "Enemy"): # If the ball eaten (smaller ball) was the enemy
            self.enemy.remove(cast(Enemy, smaller_ball)) # The ball is removed from enemy list
            self.increment_score(larger_ball, smaller_ball) # If larger ball is the player and smaller ball is the enemy then the score is incremented
        elif (smaller_ball.type == "Player"): # If the ball eaten (smaller ball) was the player
            self.player.alive = False # A method will check this and terminate the game   
        elif (smaller_ball.type == "Mass"): # Mass is removed from list
            self.mass.remove(cast(Mass, smaller_ball))

    def bounce(self, ball: Ball) -> None:
        """Bounces the ball if there was a collision with the wall. 
            The maximum distance is from the center of the ball to the center of the wall. 
            The distance between the center and wall is computed to check if there was a collision. 
            If the distance between the wall and the ball is less than the maximum distance then there has been a collision. 

            `in_collision` variable keeps track of whether there has been a collision before. 
            This is done to prevent the sticky problem where the ball is stuck in the wall. 
            If there is a previous collision and another one happens at the same time, then collision is not handles therefore no bounce. 
            After the collision takes place and there is no other collision, then the variable is set to false so that the next collision can be handled. 
            
            The ball is the super-class of enemy, player and mass.
            This method will work for any dub-classes of ball. 
            
            Args:
                `ball (Ball)`: ball object which moves.
            
            Calls: 
                `Line.distance(ball)`: works out the distance between the ball object (player, enemy). 
                `Ball.bounce(line.normal)`: reflect the velocity of the ball along normal to simulate a bounce. 
            """
        for line in self.lines: # For each line in the line list
            distance: float = ball.radius + (line.thickness / 2) + 1 # Sum of the wall thickness and wall size (radius)
            if (line.distance(ball) < distance) and (ball.in_collision == False): # Collision: if the current distance of center of ball and wall is less than the minimum distance and collision not dealt with
                ball.bounce(line.normal) # Call the bounce method from ball object
                ball.in_collision = True # Collision already dealt with therefore no sticky problem
            else: # Where there is no collision
                ball.in_collision = False # When there is no collision then set to false so that bounce can happen later

    #^ Game:
    def increment_score(self, larger_ball: Ball, smaller_ball: Ball) -> None:
        """Increments the score if the player engulfs / kills an enemy. 
            This method called from `self.engulf()` where the larger ball engulfs the smaller ball upon collision. 
            The score is incremented if the player kills the enemy. 
            For this to happen, the larger balls must be the player and the smaller ball must be the enemy. 

            An if statement is used to check the type of the two balls. 
            if the larger ball (which engulfed / killed) is the player and 
            smaller ball (which was engulfed / killed) is the enemy then 
            the score is incremented. 

            This check is carried out because it is possible that both balls were enemies. 
            In this case, the kill counter cannot be incremented as the player has not killed any enemies but rather the enemies have merged. 

            Args:
                larger_ball (Ball): larger ball which has engulfed the smaller ball. 
                smaller_ball (Ball): smaller ball which is engulfed / killed by the bigger ball. 
            """
        if (larger_ball.type == "Player") and (smaller_ball.type == "Enemy"): # Only if player engulfed the larger enemy (from `self.engulf()` method)
            self.kill_counter += 1 # Increment kill counter to be displayed on canvas on another method
    
    def game_finish(self) -> None:
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
            For the timer to be unlimited, the timer is set to be less than 0 (-1) which means that the condition is never met. 

            Checks whether the letter 'e' has been pressed. 
            If it has been pressed, the game will be terminated. 

            Calls:
                `stop()`: terminates the game and all the handlers (timer, frame).
            """
        if (len(self.enemy) == 0): # Checks if all the enemies are dead
            self.stop()
            print("You Won")
        elif (self.player.alive == False): # Checks if the player is dead
            self.stop()
            print("Game Over. You Lost.")
        elif (self.time_limit == 0): # Checks if the timer has ran out
            print("Ran Out of Time. You Lost")
            self.stop()
        elif (self.keyboard.e): # Checks if player exited the game by pressing 'e'
            print("Game Exited")
            self.stop()

    def stop(self) -> None:
        """Terminates all the handlers.
            All the timers and the frame are terminated. 
            This terminates the game. 
            """
        self.frame.stop()
        self.power_up_timer_create.stop()
        self.time_count.stop()
        self.player_power_up_timer.stop()
        self.enemy_split_timer.stop()

# A bug is present where the enemies will infinitely get larger if the plater is eaten.
# Terminating the game is a workaround. 