
class Interaction:
    def __init__(self, lines): 
        self.lines = lines
    
    def draw(self, canvas): # Can draw from multiple objects 
        for line in self.lines:
            line.draw(canvas) # Calls draw method from line object