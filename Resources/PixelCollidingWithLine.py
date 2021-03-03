
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

class Particle:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), 10, 1, "red", "black")
        canvas.draw_point(self.pos.get_p(), "yellow")
    
    def bounce(self, normal):
        return self.vel.reflect(normal)
    
    def update(self):
        self.pos.add(self.vel)

class Line:
    def __init__(self, point1, point2):
        self.pa = point1
        self.pb = point2
        self.unit = self.pb.copy().subtract(self.pa).normalize()
        self.normal = self.unit.copy().rotate_anti()
        
    def draw(self, canvas):
        canvas.draw_line(self.pa.get_p(),
                         self.pb.get_p(),
                         1,
                         "red")

    def distance_vector(self, pos):
        pos_to_a = pos.copy().subtract(self.pa)
        return pos_to_a.get_proj(self.normal)

    def distance(self, particle):
        return self.distance_vector(particle.pos).length()

class Interaction:
    def __init__(self, particle, line):
        self.particle = particle
        self.line = line
    
    def draw(self, canvas):
        self.update()
        self.line.draw(canvas)
        self.particle.draw(canvas)
    
    def update(self):
        self.particle.update()
        if self.line.distance(self.particle) < 1:
            self.particle.bounce(self.line.normal)

particle = Particle(Vector(400, 100), Vector(2, 1))
line = Line(Vector(CANVAS_WIDTH, 0), Vector(CANVAS_WIDTH -10, CANVAS_HEIGHT))
interaction = Interaction(particle, line)

frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)

frame.start()