
from SimpleGUICS2Pygame.simpleguics2pygame import canvas


class Interaction:
    def __init__(self, lines, enemies): 
        self.lines = lines
        self.enemies = enemies
    
    def draw(self, canvas): # Can draw from multiple objects 
    #& Dependencies: Line.draw (ON)
        #^ Draw Lines (could be moved to separate method)
        for line in self.lines: # Iterates over all the lines in the list
            line.draw(canvas) # Calls draw method from line object
        #^ Draw balles (could be moved to separate method)
        for enemy in self.enemies:
           enemy.draw(canvas)
           self.update_ball(enemy)

    def update_ball(self, enemy):
    #& Dependencies: self.draw (ON)
        enemy.update()