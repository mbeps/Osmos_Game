
#^ CLASSES:
class Line:
    def __init__(self, point1, point2):
        self.point_a = point1
        self.point_b = point2
        
    def draw(self, canvas):
        #& Dependencies 
        canvas.draw_line(self.point_a.get_p(), self.point_b.get_p(), 10, "red") # line(pointA, pointB, line thinkness, colour)