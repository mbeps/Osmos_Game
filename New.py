
#^ MODULES:
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Game_Physics.Vector import Vector

#^ CONSTANTS:
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

#^ CLASSES:
class Ball:
    def __init__(self, position, velocity, radius):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.colour = "green"

    def draw(self, canvas):
        canvas.draw_circle(self.position.get_p(), self.radius, 1, self.colour, self.colour)
        canvas.draw_point(self.position.get_p(), self.colour)
    
    def bounce(self, normal):
        return self.velocity.reflect(normal)
    
    def update(self):
        self.position.add(self.velocity)

class Line:
    def __init__(self, point1, point2):
        self.point_a = point1
        self.point_b = point2
        self.unit = self.point_b.copy().subtract(self.point_a).normalize()
        self.normal = self.unit.copy().rotate_anti()
        
    def draw(self, canvas):
        canvas.draw_line(self.point_a.get_p(),
                         self.point_b.get_p(),
                         1,
                         "red")

    def distance_vector(self, position):
        position_to_a = position.copy().subtract(self.point_a)
        return position_to_a.get_proj(self.normal)

    def distance(self, ball):
        return self.distance_vector(ball.position).length()

class Interaction:
    def __init__(self, balls, lines):
        self.balls = balls
        self.lines = lines
    
    def draw(self, canvas):
        self.update()
        #^ Draw Lines:
        for line in self.lines:
            line.draw(canvas)
        #^ Draw Balls:
        for ball in self.balls:
            ball.draw(canvas)
    
    def update(self):
        for ball in self.balls:
            ball.update()
            self.bounce(ball)

    def bounce(self, ball):
        for line in self.lines:
            if line.distance(ball) < ball.radius:
                ball.bounce(line.normal)

#^ MAIN:
#^ Setting Up Environment:
ball = Ball(Vector(400, 100), Vector(-3, -3), 10)
balls = [Ball(Vector(400, 100), Vector(-3, -3), 10),
        Ball(Vector(150, 100), Vector(4, -3), 15)]
lines = [Line(Vector(0, 0), Vector(0, CANVAS_HEIGHT)), # Vertical 1
        Line(Vector(0, 0), Vector(CANVAS_WIDTH, 0)), # Horizontal 1
        Line(Vector(CANVAS_WIDTH, 0), Vector(CANVAS_WIDTH, CANVAS_HEIGHT)), # Vertical 2
        Line(Vector(0, CANVAS_HEIGHT), Vector(CANVAS_WIDTH, CANVAS_HEIGHT))] # Horizontal 2
interaction = Interaction(balls, lines)

#^ Setting Up Backend:
frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)
frame.start()