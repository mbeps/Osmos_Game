
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from Vector import Vector

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                self.radius ,
                self.border,
                self.color,
                self.color)

    def update(self):
        self.pos.add(self.vel)
    
    def bounce(self, normal):
        self.vel.reflect(normal)
        
class Domain:
    def __init__(self, pos, rad, border, color, border_col):
        self.pos = pos
        self.radius = rad
        self.border = border
        self.color = color
        self.border_color = border_col
        self.edge = self.radius - self.border

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border*2+1,
                           self.border_color,
                           self.color)

    def hit(self, ball):
        distance = self.pos.copy().subtract(ball.pos).length()
        return distance + ball.radius >= self.edge

    def normal(self, ball):
        perpendicular = self.pos.copy().subtract(ball.pos)
        return perpendicular.normalize()

class Interaction:
    def __init__(self, domain, ball):
        self.ball = ball
        self.domain = domain
        self.in_collision = False
        
    def draw(self, canvas):
        self.update()
        self.domain.draw(canvas)
        self.ball.draw(canvas)

    def update(self):
        self.ball.update()
        if self.domain.hit(self.ball):
            if not self.in_collision:
                normal = self.domain.normal(self.ball)
                self.ball.bounce(normal)
                self.in_collision = True
        else:
            self.in_collision = False

ball = Ball(Vector(2/3 * CANVAS_WIDTH, 1/2 * CANVAS_HEIGHT),
            Vector(-2, 1),
            10,
            "blue")
domain = Domain(Vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2),
                100,
                5,
                "black",
                "red")
interaction = Interaction(domain, ball)

frame = simplegui.create_frame("Domain", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(interaction.draw)

frame.start()