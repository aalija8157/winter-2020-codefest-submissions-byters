import math
import random
import pygame
pygame.init()

screen=pygame.display.set_mode((800,700))
#title
pygame.display.set_caption('forest fire')

#background
back = pygame.image.load('background.png')

#game over
game_over=pygame.image.load('gameover.png')

#player
playerimg=pygame.image.load('hero.png')
playerx=310
playery=555
playerx_change=0

#tree
treeimg=pygame.image.load('tree.png')
treex=random.randint(100,600)
treey=random.randint(200,475)
treex_change=4
treey_change=40

#bullet
bulletimg=pygame.image.load('bullet.png')
bulletx=0
bullety=565
bullety_change=15
bullet_state='ready'

#player function
def player(x,y):
    screen.blit(playerimg,(x,y))

#tree function
def tree(x,y):
    screen.blit(treeimg,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletimg,(x+75,y))

font = pygame.font.Font("freesansbold.ttf",25)

def score(score):
    text= font.render("Score: " +str(score),True, (255,255,255))
    screen.blit(text,(0,0))
    
    


points=0
missed=0
run=True
while (run):
    screen.fill((0,0,0))
    screen.blit(back,(0,0))
    if missed>=5:
        screen.blit(game_over,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

        #player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change=-5
            if event.key == pygame.K_RIGHT:
                playerx_change=5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready' and (missed<5):
                    bulletx=playerx
                    fire_bullet(bulletx,bullety)
            if event.key==pygame.K_UP:
                if missed>=5:
                    points=0
                    missed=0
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerx_change=0

    #player movement
    playerx += playerx_change
    if playerx<=-20:
        playerx=-20
    elif playerx>=640:
        playerx=640

    #tree movement
    treex += treex_change
    if treex<=0:
        treex_change=3 
        treey+=treey_change
        if points>=15:
            treex_change=9
        if points>=30:
            treex_change=12
    elif treex>=695:
        treex_change=-3
        treey+=treey_change
        if points>=15:
            treex_change=-9
        if points>=30:
            treex_change=-12

    if bullety<=0:
        bullety=565
        bullet_state='ready'
    if bullet_state is 'fire':
        fire_bullet(bulletx,bullety)
        bullety-=bullety_change

    if(treey>=450):
        missed+=1
        treex=random.randint(100,600)
        treey=random.randint(200,410)
        print('missed')
        print(missed)
        

    if ((bulletx>=treex and bulletx<=treex+128) and (bullety>=treey and bullety<=treey+117)):
        bullety=565
        bullet_state='ready'
        points+=1
        print('points:')
        print(points)
        treex=random.randint(100,600)
        treey=random.randint(200,410)

    if missed<5:
        player(playerx,playery)
        tree(treex,treey)
    score(points)
    pygame.display.update()
    
    
pygame.quit()