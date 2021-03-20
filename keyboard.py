
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Keyboard:
    def __init__(self):
        """Keyboard will track certain keypresses that can be used to control game entities. 
            Initially, the keys are set to false as no keys are being pressed. 
            Once keypressed are detected, they will return true which can be used to execute certain actions.  
        """
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def keyDown(self, key):
        """Actions when certain keys are down or being pressed (could be held down). 
            The keys that are being pressned are set to true. 
            When true, certain actions can be executed. 
            Args:
                key (Key): key that is currently being pressed. 
            """
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['up']:
            self.up = True
        elif key == simplegui.KEY_MAP['down']:
            self.down = True

    def keyUp(self, key):
        """Actions when certain keys are up or not being pressed (could be held down). 
            The keys are being set to false to indicate that they are no longer being pressed. 
            Args:
                key (Key): key that were being pressed. 
            """
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['up']:
            self.up = False
        elif key == simplegui.KEY_MAP['down']:
            self.down = False