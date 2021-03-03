class Ball:
    def __init__(self, position, velocity, radius, color):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = color
        
    def update(self):
        self.position.add(self.velocity)
        
    def draw(self, canvas):
        canvas.draw_circle(self.position.get_p(),
                           self.radius,
                           1,
                           self.color,
                           self.color)
        