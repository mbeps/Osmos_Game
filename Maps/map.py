
#^ CLASSES:
class Line:
    def __init__(self, point1, point2):
        """Map is where the action will take place. 
            4 walls will be drawn around the canvas.
            The walls are drawn dynamically around the canvas depending on the size of the canvas. 
            Balls will bounce here. 
            Args:
            point1 (Vector): starting point of the line
            point2 (Vector): finishing point of the line
            """
        self.point_a = point1
        self.point_b = point2
        
    def draw(self, canvas):
        """Draws line from one point to the other. 
            
            Args:
                canvas (Canvas): where the gameplay takes place. 
            """
        canvas.draw_line(self.point_a.get_p(), self.point_b.get_p(), 10, "red") # line(pointA, pointB, line thinkness, colour)