import pygame
from pygame.locals import *
import random

#initialize pygame
pygame.init()

#game speed
clock=pygame.time.Clock()
fps=60

#create game wimdow
screen_width=770
screen_height=400
screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('road rush')

#game variables
scroll_speed=4
score=0
game_over=False
driving=True
car_frequency=3000
last_car=pygame.time.get_ticks()-car_frequency

#loading background pictures
road1=pygame.image.load('road.png')
road1_rect = road1.get_rect()
road1_rect.topleft = (0, 0)
road2=pygame.image.load('road.png')
road2_rect = road2.get_rect()
road2_rect.y = (-road1_rect.height)


#create a class for the users car
class Car(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) # to inherit from the sprite function
        self.image=pygame.image.load('maincar.png')
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=3

    def update(self):
        if driving==True:
        #handle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if self.rect.top>0: 
                    self.rect.y -=int(self.vel)
            elif keys[pygame.K_s]:
                if self.rect.bottom<screen_height: 
                    self.rect.y +=int(self.vel)
            elif keys[pygame.K_d]:
                if self.rect.right<650: 
                    self.rect.x +=int(self.vel)
            elif keys[pygame.K_a]:
                if self.rect.left>150: 
                    self.rect.x -=int(self.vel)
                
#create a car class for npc cars that will spawn between 150 and 650 across the x axis
class NpcCar(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(f'cv{random.randint(1,4)}.png')
        self.rect= self.image.get_rect()
        self.rect.center=[x,y]
        


    def update(self):
        self.rect.y+=scroll_speed-2
        if self.rect.top>screen_height:
            self.kill()



#create a group for users car and npc cars
user_car=pygame.sprite.Group()
npc_car=pygame.sprite.Group()
#now create an instance for the users car and place on screen 
mycar=Car(270,screen_height-80)
#add to group
user_car.add(mycar)


#create game loop
run=True
while run:
    #set game speed
    clock.tick(fps)

    

    #draw and scroll
    screen.blit(road1,road1_rect)
    screen.blit(road2,road2_rect)

    #putting car on the screen
    user_car.draw(screen)
    user_car.update()
    npc_car.draw(screen)

    if game_over==False and driving== True:
        #generate new cars
        time_now=pygame.time.get_ticks()
        if time_now-last_car>car_frequency:
            obstacle_car=NpcCar(random.randint(150, 650),-screen_height)
            npc_car.add(obstacle_car)
            last_car=time_now

        #draw and scroll
        road1_rect.y+=scroll_speed
        road2_rect.y+=scroll_speed
        if road1_rect.top >= screen_height:
            road1_rect.y=road2_rect.y-road1_rect.height
        if road2_rect.top >= screen_height:
            road2_rect.y=road1_rect.y-road1_rect.height
        npc_car.update()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        
            
    
    pygame.display.update() #function to make images work