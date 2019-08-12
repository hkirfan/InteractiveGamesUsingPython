# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas,rock_group):  
    for each_rock in rock_group:  
        each_rock.draw(canvas)
        if each_rock.update():  
            rock_group.remove(each_rock)

def group_collide(group,other_object):  
    collision_number = 0  
    for each_object in set(group):  
        if each_object.collide(other_object):  
            group.remove(each_object)  
            collision_number += 1  
    return collision_number 

def group_group_collide(group1,group2):  
    collision_number = 0  
    for each_object in set(group1):  
        each_object_number =group_collide(group2,each_object)  
        if each_object_number:  
            collision_number += each_object_number  
            group1.remove(each_object)  
    return collision_number


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:  
            self.image_center[0]=135  
        else:  
            self.image_center[0]=45  
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle) 

    def update(self):
        self.vel[0] *= 0.97
        self.vel[1] *= 0.97
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        if self.thrust:
            ship_thrust_sound.play()  
        else:  
            ship_thrust_sound.rewind() 
            
        
        
        if self.thrust:  
            forward_acceleration = angle_to_vector(self.angle)  
            self.vel[0] += forward_acceleration[0]/5  
            self.vel[1] += forward_acceleration[1]/5  
              
    def launch_missile(self):
        global a_missile,missile_group
        forward_acceleration = angle_to_vector(self.angle)  
        missile_pos=[self.pos[0] + 45 * forward_acceleration[0],self.pos[1] + 45 * forward_acceleration[1]]  
        missile_vel=[self.vel[0] + forward_acceleration[0] * 3,self.vel[1] + forward_acceleration[1] * 3]  
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)  
        missile_sound.play()
        missile_group.append(a_missile)
        #missile_group.append(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

    def get_position(self):  
        return self.pos  
      
    def get_radius(self):  
        return self.radius    
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):  
        if self.animated:  
            tmpcenter=[self.image_center[0]+self.age*self.image_size[0],self.image_center[1]]  
            canvas.draw_image(self.image, tmpcenter, self.image_size, self.pos, self.image_size,self.angle)  
        else:  
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
    
    def update(self):
        self.pos[0]  += self.vel[0]
        self.pos[0]  %=WIDTH
        self.pos[1]  += self.vel[1]
        self.pos[1]  %= HEIGHT
        self.angle   += self.angle_vel
        self.age += 1  
        if self.age > self.lifespan:  
            return True 
        else:  
            return False
        
    def get_position(self):  
        return self.pos  
      
    def get_radius(self):  
        return self.radius
   
    def collide(self,other_object):  
        #global explosion_group  
        if dist(self.get_position(),other_object.get_position())<self.get_radius()+other_object.get_radius():  
            foward=angle_to_vector(self.angle)  
            new_pos=[self.pos[0]+self.get_radius(),self.pos[1]+self.get_radius()]  
            a_explosion=Sprite(new_pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)  
            explosion_group.append(a_explosion)  
            return True  
        else:  
            return False  
    
           
def draw(canvas):
    global time,a_rock,rock_group,lives,score,missile_group,explosion_group,started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas,rock_group)
    process_sprite_group(canvas,missile_group)  
    process_sprite_group(canvas,explosion_group)
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    
    canvas.draw_text("Lives remaining:" +str(lives), (50, 50), 32, "Green")  
    canvas.draw_text("Score:" +str(score), (650, 50), 32, "Red")
    canvas.draw_text("RICE ROCKS!",(380,50),24,"Yellow")
    # update ship and sprites
    my_ship.update()
    for each_rock in rock_group:
     each_rock.update()
    for each_missile in missile_group:
     each_missile.update()
    for each_explosion in explosion_group:
     each_explosion.update()        
    #a_missile.update()
    
    
    if not started:  
        canvas.draw_image(splash_image, splash_info.get_center(),   
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],   
                          splash_info.get_size())  
        return  
    
    if group_collide(rock_group,my_ship):  
        lives -= 1
            
    if lives == 0:  
        started=False  
        rock_group=[]  
        explosion_group=[]  
          
    if group_group_collide(rock_group,missile_group):  
        score += 10  

        
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group,started,rock_thrust
    rock_thrust *= 1.01
    
    
    if len(rock_group) >= 12 or not started:
        return
    
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    while dist(my_ship.get_position(),rock_pos)<200:  
            rock_pos=[random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]  
    rock_vel = [rock_thrust*random.random() * .6 - .3, rock_thrust*random.random() * .6 - .3]  
    rock_avel = random.random() * .2 - .1  
    rock_group.append( Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))
        

def keyup_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        
def keydown_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = - 0.15
    if key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0.15
    if key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
    if key == simplegui.KEY_MAP['space']:
        my_ship.launch_missile()
    
def click(pos):  
    global started,lives,score,my_ship,rockth  
    center = [WIDTH / 2, HEIGHT / 2]  
    size = splash_info.get_size()  
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)  
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)  
    if (not started) and inwidth and inheight:  
        started = True  
        lives = 3  
        score = 0  
        rock_thrust = 1  
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)  
        soundtrack.rewind()  
        soundtrack.play()
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = []
missile_group = []
explosion_group = []
rock_thrust = 1

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)    
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(click)
label1 = frame.add_label("Welcome to Asteroids. The rules of the game are simple")
label4 = frame.add_label("Your aim is to destroy the rocks before they hit your spaceship")
label2 = frame.add_label("Press the up arrow key to accelerate your ship")
label3 = frame.add_label("Press the left and right arrow keys to rotate anticlockwise and clockwise respectively")
label5 = frame.add_label("Press the space key to launch the missile")
                         


timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()


