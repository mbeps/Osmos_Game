
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Keyboard:
    """Keyboard class will keep track of the keys being pressed. 
        These keys presses can be used to control game entities such as the player or game setting. 
    """
    def __init__(self):
        """Initializes keyboard object to keep track of key presses. 
            Initially, the keys are set to false as no keys are being pressed. 
            Once keypressed are detected, they will return true which can be used to execute certain actions.  
            """
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.e = False

    def keyDown(self, key):
        """Actions when certain keys are down or being pressed (could be held down). 
            The keys that are being pressned are set to true. 
            When true, certain actions can be executed. 
            
            Args:
                `key (Key)`: key that is currently being pressed. 
            """
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['up']:
            self.up = True
        elif key == simplegui.KEY_MAP['down']:
            self.down = True
        elif key == simplegui.KEY_MAP['e']:
            self.e = True

    def keyUp(self, key):
        """Actions when certain keys are up or not being pressed (could be held down). 
            The keys are being set to false to indicate that they are no longer being pressed. 
            
            Args:
                `key (Key)`: key that were being pressed. 
            """
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['up']:
            self.up = False
        elif key == simplegui.KEY_MAP['down']:
            self.down = False
        elif key == simplegui.KEY_MAP['e']:
            self.e = False