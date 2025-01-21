import pygame
from pygame.locals import *

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
ground_scroll=0
scroll_speed=4
score=0
game_over=False
driving=True

#loading background pictures
road1=pygame.image.load('road.png')
road1_rect = road1.get_rect()
road1_rect.topleft = (0, 0)
road2=pygame.image.load('road.png')
road2_rect = road2.get_rect()
road2_rect.y = (-road1_rect.height)


#create game loop
run=True
while run:
    #set game speed
    clock.tick(fps)

    

    #draw and scroll
    screen.blit(road1,road1_rect)
    screen.blit(road2,road2_rect)

    if game_over==False and driving== True:
        #draw and scroll
        road1_rect.y+=scroll_speed
        road2_rect.y+=scroll_speed
        if road1_rect.top >= screen_height:
            road1_rect.y=road2_rect.y-road1_rect.height
        if road2_rect.top >= screen_height:
            road2_rect.y=road1_rect.y-road1_rect.height
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            
    pygame.display.flip()
    pygame.display.update() #function to make images work