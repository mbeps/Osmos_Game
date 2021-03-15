import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import vector
import random
import math
from threading import Thread

# Some constants
CANVAS_DIMS = (1200, 700)
WIDTH = 1200
HEIGHT = 700
ballz = []
spc = 0


def randCol ():
    r = random.randrange (0, 256)
    g = random.randrange (0, 256)
    b = random.randrange (0, 256)
    return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'
##class Wall:
##    def __init__(self, x, border,color,side):
##        self.x = x
##        self.side = side
##        self.border = border
##        self.color = color
##        if side == "r" or side == "l":
##            self.normal = vector.Vector(1,0)
##        else:
##            self.normal = vector.Vector(0,1)
##        self.edge_r = x + border
##        
##
##    def draw(self, canvas):
##        if self.side == "r" or self.side == "l":
##            canvas.draw_line((self.x, 0),
##                             (self.x, CANVAS_HEIGHT),
##                             self.border*2+1,
##                             self.color)
##        elif self.side == "t" or self.side == "b":
##            canvas.draw_line((0, self.x),
##                             (CANVAS_WIDTH,self.x ),
##                             self.border*2+1,
##                             self.color)
##            
##
##    def hit(self, ball):
##        if self.side == "r":
##            h = (ball.offset_r()>= self.edge_r)
##        elif self.side == "l":
##            h = (ball.offset_l()<= self.edge_r)
##        elif self.side == "t":
##            h = (ball.offset_t()<= self.edge_r)
##        elif self.side == "b":
##            h = (ball.offset_b()>= self.edge_r)
##        return h

##class Player:
##    def __init__(self,pos):
##        self.IMG = simplegui._LocalImage('circle.png')
##        self.IMG_CENTRE = (910, 607)
##        self.IMG_DIMS = (1820,1214)
##        self.img_dest_dim = (336,240)
##        self.img_pos = pos
##        self.img_rot = 0
##        self.vel = vector.Vector()
##    def draw(self,canvas):
##        canvas.draw_image(self.IMG, self.IMG_CENTRE, self.IMG_DIMS, self.img_pos.get_p(), self.img_dest_dim,self.img_rot)
##    def update(self):  
##        self.img_pos.add(self.vel)
##        self.vel = self.vel.multiply(0.85)

class mote:
    def __init__(self):
        self.radius = (random.randint(10,30))
        self.vel = vector.Vector((random.randint(-100,100)/100),(random.randint(-100,100)/100))
        self.colour = randCol()
        self.isPlayer = False
        self.pos = vector.Vector(random.randint(0+self.radius,WIDTH-self.radius),random.randint(0+self.radius,HEIGHT-self.radius))
    def draw(self,canvas):
        canvas.draw_circle(self.pos.get_p(),self.radius,1,self.colour,self.colour)
    def update(self):
        self.pos = self.pos.add(self.vel)
    def offset_l(self):
        return self.pos.x - self.radius
    def offset_r(self):
        return self.pos.x + self.radius
    def offset_t(self):
        return self.pos.y - self.radius
    def offset_b(self):
        return self.pos.y + self.radius
    def bounce(self, normal):
        self.vel.reflect(normal)

class Player(mote):
    def __init__(self,pos):
        self.isPlayer = True
        self.IMG = simplegui._LocalImage('rimuru.png')
        self.IMG_CENTRE = (303,303)
        self.IMG_DIMS = (606,606)
        self.radius = 30
        self.img_dest_dim = (self.radius,self.radius)
        self.pos = pos
        self.img_rot = 0
        self.alive = True
        self.vel = vector.Vector()
    def draw(self,canvas):
        canvas.draw_image(self.IMG, self.IMG_CENTRE, self.IMG_DIMS, self.pos.get_p(), self.img_dest_dim,self.img_rot)
    def update(self):  
        self.pos.add(self.vel)
        self.vel = self.vel.multiply(0.85)
            
        
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['up']:
            self.up = True
        elif key == simplegui.KEY_MAP['down']:
            self.down = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['up']:
            self.up = False
        elif key == simplegui.KEY_MAP['down']:
            self.down = False

class Interaction:
    def __init__(self, wheel, keyboard,ballz):
        self.wheel = wheel
        self.keyboard = keyboard
        self.ballz = ballz
        self.ballz.append(self.wheel)
        self.start = 0
        
    def ballzup(self,canvas):
            global spc
            for i in range(len(self.ballz)):
                    if self.ballz[i].pos.get_p()[0]+self.ballz[i].radius >= 1200 or self.ballz[i].pos.get_p()[0]-self.ballz[i].radius <= 0:
                        self.ballz[i].bounce(vector.Vector(1,0))
                        self.ballz[i].update()
                    elif self.ballz[i].pos.get_p()[1] >= 700-(self.ballz[i].radius) or self.ballz[i].pos.get_p()[1]-self.ballz[i].radius <= 0:
                        self.ballz[i].bounce(vector.Vector(0,1))
                        self.ballz[i].update()
                    else:
                        self.ballz[i].update()
            kill = []
            for i in range(len(self.ballz)):
                for j in range(len(self.ballz)):
                    if i != j and math.sqrt((ballz[i].pos - ballz[j].pos).length_squared()) < 50:
                        ballz[j].vel.add((ballz[i].pos - ballz[j].pos).divide(900))
                    if  i != j and ballz[i].isPlayer == False and math.sqrt((ballz[i].pos - ballz[j].pos).length_squared()) < ballz[i].radius and math.sqrt((ballz[i].pos - ballz[j].pos).length_squared()) > ballz[j].radius  :
                        ballz[i].radius += ballz[j].radius//10
                        kill.append(j)
                    if  i != j and ballz[i].isPlayer == True and math.sqrt((ballz[i].pos - ballz[j].pos).length_squared()) < ballz[i].radius and math.sqrt((ballz[i].pos - ballz[j].pos).length_squared()) > ballz[j].radius  :
                        ballz[i].radius += ballz[j].radius//10
                        ballz[i].img_dest_dim = (ballz[i].radius,ballz[i].radius)
                        kill.append(j)
                    else:
                        pass
            for i in kill:
                spc -= 1
                ballz.pop(i)
            x = 0
            while x != len(ballz):
                if self.ballz[x].radius == 0:
                    self.ballz.pop(x)
                    x +=1
                else:
                    x += 1
            if spc <= 10:
                b = mote()
                b.draw(canvas)
                self.ballz.append(b)
                spc +=1
            else:
                pass

            
            
        

                    

    def update(self,canvas):
        global spc
        self.ballzup(canvas)
        #RIGHT KEY
        if self.keyboard.right:
            self.wheel.vel.add(vector.Vector(1, 0))
        #UP KEY
        if self.keyboard.up:     
            self.wheel.vel.add(vector.Vector(0,-1))
        #DOWN KEY
        if self.keyboard.down:     
            self.wheel.vel.add(vector.Vector(0,+1))
        #LEFT KEY
        if self.keyboard.left:
            self.wheel.vel.add(vector.Vector(-1,0))
            
    def draw(self,canvas):
        self.update(canvas)
        self.wheel.update()
        for i in self.ballz:
            i.draw(canvas)
        


kbd = Keyboard()
player = Player(vector.Vector(WIDTH/2, HEIGHT-35))
inter = Interaction(player,kbd,ballz)

def draw(canvas):
    inter.draw(canvas)
    player.draw(canvas)
    

frame = simplegui.create_frame("A wheel", CANVAS_DIMS[0], CANVAS_DIMS[1],0)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
