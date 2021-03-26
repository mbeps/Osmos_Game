import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import vector
import random
import array
import math
from playsound import playsound
from threading import Thread

import tkinter as tk
WIDTH = 1200
HEIGHT = 700
def sound(audio):
    playsound(audio)
def randCol():
    r = random.randrange (0, 256)
    g = random.randrange (0, 256)
    b = random.randrange (0, 256)
    return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'
class mote:
    def __init__(self):
        self.radius = (random.randint(10,30))
        self.vel = vector.Vector((random.randint(-100,100)/100),(random.randint(-100,100)/100))
        self.colour = randCol()
        self.aVel = vector.Vector(0,0)
        self.isPlayer = False
        self.pos = vector.Vector(random.randint(30+self.radius,WIDTH-self.radius),random.randint(30+self.radius,HEIGHT-self.radius))
    
    def draw(self,canvas):
        canvas.draw_circle(self.pos.get_p(),self.radius,1,self.colour,self.colour)
        
    def update(self):
        self.aVel.multiply(0.8)
        self.pos = self.pos.add(self.vel + self.aVel)
        
    def bounce(self, normal):
        self.vel.reflect(normal)
        
    def dist_finder(self,mote):
        return(math.sqrt((self.pos - mote.pos).length_squared()))
    def off_screen(self):
        if self.pos.get_p()[0]+self.radius < -100 or self.pos.get_p()[0]+self.radius > WIDTH+100 or self.pos.get_p()[1]+self.radius < -100 or self.pos.get_p()[1]+self.radius > HEIGHT+100:
            return True
        else:
            return False
        
        


class Player(mote):
    def __init__(self,pos):  
        self.isPlayer = True
        self.IMG = simplegui._LocalImage('rimuru.png')
        self.IMG_CENTRE = (303,303)
        self.IMG_DIMS = (606,606)
        self.radius = 20
        self.img_dest_dim = (self.radius*2,self.radius*2)
        self.pos = pos
        self.aVel = 0
        self.img_rot = 0
        self.alive = True
        self.state = 0
        self.stater = 0
        self.stateon = False
        self.vel = vector.Vector()
    def draw(self,canvas):
        canvas.draw_image(self.IMG, (((self.state*606)+303),303), self.IMG_DIMS, self.pos.get_p(), self.img_dest_dim,self.img_rot)
    def update(self):
        if self.stateon == True:
            print(self.stateon,self.state)
            if self.stater % 3 == 0:
                self.state += 1
            if self.state == 5:
                self.stateon = False
                self.state = 0
            else:
                self.stater += 1
        
        self.pos.add(self.vel)
        self.vel = self.vel.multiply(0.85)
        

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.z = False
        self.s = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True
        elif key == simplegui.KEY_MAP['up']:
            self.up = True
        elif key == simplegui.KEY_MAP['down']:
            self.down = True
        elif key == simplegui.KEY_MAP['z']:
            self.z = True
        elif key == simplegui.KEY_MAP['s']:
            self.s = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False
        elif key == simplegui.KEY_MAP['up']:
            self.up = False
        elif key == simplegui.KEY_MAP['down']:
            self.down = False
        elif key == simplegui.KEY_MAP['z']:
            self.z = False
        elif key == simplegui.KEY_MAP['s']:
            self.s = False
            
class Interaction:
    def __init__(self,wheel,keyboard,ballz):
        self.wheel = wheel
        self.keyboard = keyboard
        self.ballz = ballz
        self.ballz.append(self.wheel)
        self.counter = 0
        self.pause = False

    def consume(self):
        kill = []
        for i in range(len(self.ballz)):
            for j in range(len(self.ballz)):
                if  i != j and self.ballz[i].isPlayer == False and self.ballz[i].dist_finder(self.ballz[j]) < self.ballz[i].radius and self.ballz[i].dist_finder(self.ballz[j]) > self.ballz[j].radius  :
                    self.ballz[i].radius += self.ballz[j].radius//10
                    kill.append(j)
                if  i != j and self.ballz[i].isPlayer == True and self.ballz[i].dist_finder(self.ballz[j]) < self.ballz[i].radius and self.ballz[i].dist_finder(self.ballz[j]) > self.ballz[j].radius  :
                    self.ballz[i].radius += self.ballz[j].radius//10
                    t1 = Thread(target=sound,args = ["yum.mp3"])
                    t1.start()
                    self.ballz[i].stateon = True
                    self.ballz[i].img_dest_dim = (self.ballz[i].radius*2,self.ballz[i].radius*2)
                    kill.append(j)
        return kill
                    
    def grav(self):
        for i in range(len(self.ballz)):
            for j in range(len(self.ballz)):
                if i != j and self.ballz[i].dist_finder(self.ballz[j]) < 50:
                    self.ballz[j].vel.add((self.ballz[i].pos - self.ballz[j].pos).divide(900))
                else:
                    pass
                
    def mote_reg(self):
        population = len(self.ballz)
        while population < 10:
            x = mote()
            self.ballz.append(x)
            population = len(self.ballz)
        for i in self.ballz:
            i.update()

    def mote_rem(self,kill):
        for i in self.ballz:
            if i.off_screen():
                kill.append(self.ballz.index(i))
            else:
                pass
        kill = (sorted(kill)[::-1])
        for i in kill:
            if  self.ballz[i].isPlayer == True:
                audio = 'death.mp3'
                t2 = Thread(target=sound,args =[audio])
                t2.start()
                self.pause = True
            if i <= len(self.ballz): 
                self.ballz.pop(i)
            else:
                pass

    def relative_mov(self):
        self.counter += 1
        for i in self.ballz:
            if i.isPlayer == True:
                pass
            else:  
                if self.keyboard.right:
                    i.aVel.add(vector.Vector(-1, 0))   
                if self.keyboard.left:
                    i.aVel.add(vector.Vector(1, 0))
                if self.keyboard.up:
                    i.aVel.add(vector.Vector(0, 1))
                if self.keyboard.down:
                    i.aVel.add(vector.Vector(0, -1))
                if self.keyboard.z:
                    i.aVel.multiply(1.1)
                    if self.ballz[0].radius >= 20:
                        if self.counter % 10: 
                            self.ballz[0].radius -= 1
                        self.ballz[0].img_dest_dim = (self.ballz[0].radius*2,self.ballz[0].radius*2)
           
    def update(self,canvas):
        self.mote_reg()
        self.relative_mov()
        self.grav()
        kill = self.consume()
        self.mote_rem(kill)
    
    def draw(self,canvas):
        self.update(canvas)
        for i in self.ballz:
            i.draw(canvas)

class Game:
    def __init__(self):
        self.ballz = []
        self.pause = True
        self.counter = 0
        self.img = 1
    def start(self):
        
        def draw(canvas):
            if kbd.s == False and self.pause == True and inter.pause == False:
                canvas.draw_image(simplegui._LocalImage('start.png'), (WIDTH/2,HEIGHT/2),(WIDTH,HEIGHT), (WIDTH/2,HEIGHT/2), (WIDTH,HEIGHT),0)
            if kbd.s == True:
                self.pause  = False
            if self.pause == False:
                inter.draw(canvas)
            if inter.pause == True:
                self.pause = True
            if inter.pause == True and self.pause == True:
                self.counter += 1
                if self.counter%15 == 0 :
                    canvas.draw_image(simplegui._LocalImage("end"+str(self.img)+".png"), (WIDTH/2,HEIGHT/2),(WIDTH,HEIGHT), (WIDTH/2,HEIGHT/2), (WIDTH,HEIGHT),0)
                    if self.img < 5:
                        self.img += 1
                    else:
                        pass
                else:
                    canvas.draw_image(simplegui._LocalImage("end"+str(self.img)+".png"), (WIDTH/2,HEIGHT/2),(WIDTH,HEIGHT), (WIDTH/2,HEIGHT/2), (WIDTH,HEIGHT),0)
            else:
                pass
            

        
        kbd = Keyboard()
        player = Player(vector.Vector(WIDTH/2, HEIGHT/2))
        inter = Interaction(player,kbd,self.ballz)


        frame = simplegui.create_frame("OSMOS", WIDTH, HEIGHT,0)
        frame.set_draw_handler(draw)
        frame.set_keydown_handler(kbd.keyDown)
        frame.set_keyup_handler(kbd.keyUp)

        frame.start()
        

x = Game()
x.start()
