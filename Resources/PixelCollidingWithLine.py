
#^ MODULES:
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector

#^ CONSTANTS:
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

#^ CLASSES:
class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def draw(self, canvas):
        canvas.draw_circle(self.position.get_p(), 10, 1, "red", "black")
        canvas.draw_point(self.position.get_p(), "yellow")
    
    def bounce(self, normal):
        return self.velocity.reflect(normal) # Bounce works by reflecting the ball in the normal
    
    def update(self):
        self.position.add(self.velocity) # Everytime this method is called, the velocity will be added to make it move

class Line:
    def __init__(self, point1, point2):
        self.point_a = point1
        self.point_b = point2
        self.unit = self.point_b.copy().subtract(self.point_a).normalize() # Unit Vector = A - B  /  Normal = Unit Vector
        self.normal = self.unit.copy().rotate_anti() # To work out normal, it is easier to rotate than to use dot product
        
    def draw(self, canvas):
        canvas.draw_line(self.point_a.get_p(),
                         self.point_b.get_p(),
                         50,
                         "blue")

    def distance_vector(self, position):
        position_to_a = position.copy().subtract(self.point_a)
        return position_to_a.get_proj(self.normal) # Projection of vector from line to particle projected on normal of line

    def distance(self, particle): # Work out distance between line and ball
        return self.distance_vector(particle.position).length() # Shortest distance from particle

class Interaction:
    def __init__(self, particle, line): 
        self.particle = particle
        self.line = line
    
    def draw(self, canvas): # Can draw from multiple objects 
        self.update()
        self.line.draw(canvas) # Calls draw method from line object
        self.particle.draw(canvas) # Calls draw method from particle object
    
    def update(self): # Calls update method for particle to make it move
        self.particle.update() # Ask the ball object to see if a collision has taken place
        if self.line.distance(self.particle) < 1: # If the distance between line and particle is less than 1 then a collision has happened
            self.particle.bounce(self.line.normal)

#^ MAIN:
#^ Setting Up
particle = Particle(Vector(400, 100), Vector(-2, 1))
line = Line(Vector(0, 0), Vector(0, CANVAS_HEIGHT))
interaction = Interaction(particle, line)

frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)

frame.start()