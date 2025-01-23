import pygame
from pygame.locals import *
import random

#initialize pygame
pygame.init()

#game speed
clock=pygame.time.Clock()
fps=60

#define font fpr score counter
font=pygame.font.SysFont('Bauhaus 93', 60)
white=(255, 255, 255)

#create game wimdow
screen_width=770
screen_height=400
screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('road rush')

#game variables
scroll_speed=4
score=0
game_over=False
driving=False
car_frequency=3000
last_car=pygame.time.get_ticks()-car_frequency
pass_car=False

#loading background pictures
road1=pygame.image.load('images/road.png')
road1_rect = road1.get_rect()
road1_rect.topleft = (0, 0)
road2=pygame.image.load('images/road.png')
road2_rect = road2.get_rect()
road2_rect.y = (-road1_rect.height)
button_image= pygame.image.load('images/restart.png')

#function to reset everything to restart the game
def reset_game():
    #remove all the NPC cars
    npc_car_group.empty()
    #reposition the bird
    mycar.rect.x=270
    mycar.rect.y=screen_height-160
    


#function to show score
def draw_text(text,font,text_col,x ,y):
    img=font.render(text, True, text_col)
    screen.blit(img,(x,y))


#create a class for the users car
class Car(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) # to inherit from the sprite function
        self.image=pygame.image.load('images/maincar.png')
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=3

    def update(self):
        if driving==True and game_over==False:
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
        self.image=pygame.image.load(f'images/cv{random.randint(1,4)}.png')
        self.rect= self.image.get_rect()
        self.rect.center=[x,y]
        


    def update(self):
        self.rect.y+=scroll_speed-2
        if self.rect.top>screen_height:
            self.kill()

#class for button
class Button():
    def __init__(self, x, y, image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x, y)

    def draw(self):
        action=False
        #get mouse position
        pos=pygame.mouse.get_pos()

        #check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1: #shows mouse has been clicked
                action=True

        
        #draw button
        screen.blit(self.image,(self.rect.x, self.rect.y))

        return action



#create a group for users car and npc cars
user_car_group=pygame.sprite.Group()
npc_car_group=pygame.sprite.Group()
#now create an instance for the users car and place on screen 
mycar=Car(270,screen_height-80)
#add to group
user_car_group.add(mycar)

#create restart button instance
button=Button(screen_width//2 - 50, screen_height//2 -100, button_image)


#create game loop
run=True
while run:
    #set game speed
    clock.tick(fps)

    

    #draw and scroll
    screen.blit(road1,road1_rect)
    screen.blit(road2,road2_rect)

    #putting car on the screen
    user_car_group.draw(screen)
    user_car_group.update()
    npc_car_group.draw(screen)
    
    #check if a user car has passed npc cars if so ad 1 to score
    if len(npc_car_group)>0:
        if user_car_group.sprites()[0].rect.top < npc_car_group.sprites()[0].rect.top and user_car_group.sprites()[0].rect.bottom < npc_car_group.sprites()[0].rect.bottom and pass_car==False:
            pass_car=True
        if pass_car== True:
            if user_car_group.sprites()[0].rect.top > npc_car_group.sprites()[0].rect.top:
                score+=1
                pass_car=False
    #display score
    draw_text(str(score),font, white, int(screen_width/2),20)
    
    #check for collision
    if pygame.sprite.groupcollide(user_car_group, npc_car_group,False, False):
        game_over=True
        
    
    if game_over==False and driving== True:
        #generate new cars
        time_now=pygame.time.get_ticks()
        if time_now-last_car>car_frequency:
            obstacle_car=NpcCar(random.randint(150, 650),-screen_height)
            npc_car_group.add(obstacle_car)
            last_car=time_now

        #draw and scroll
        road1_rect.y+=scroll_speed
        road2_rect.y+=scroll_speed
        if road1_rect.top >= screen_height:
            road1_rect.y=road2_rect.y-road1_rect.height
        if road2_rect.top >= screen_height:
            road2_rect.y=road1_rect.y-road1_rect.height
        npc_car_group.update()
    
    if game_over==True:
        if button.draw() == True:
            game_over=False
            reset_game()
            score=0

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and driving==False and game_over==False:
            driving=True 
        
            
    
    pygame.display.update() #function to make images work