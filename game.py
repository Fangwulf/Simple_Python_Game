###########################################################################
#   Shooting Game
#
#   Programmed by Josh Follett 2017-11-07
#
#   Dependancies: Python 3.6 and Pygame 1.9.3
#   
###########################################################################

import pygame as pg # shorthands pygame.X to pg.X
import sys, random, time, math
from pygame.locals import * # instead of typing pygame.locals.X everytime

FPS = 60 # frames per second the screen updates

windowx = 500 # set width of game window
windowy = 500 # set height of game window

# defines RGB values for colors
black = (0, 0, 0)
white = (255, 255, 255)

# keyboard button assignments
quitKey = K_ESCAPE
moveUpKey = K_w
moveDownKey = K_s
moveLeftKey = K_a
moveRightKey = K_d

enemiesSpawn = 1

def main ():
    global fpsClock, window, enemyImg, bulletImg, heroImg# global use variables

    pg.init() # initialize pygame
    fpsClock = pg.time.Clock()

    window = pg.display.set_mode((windowx, windowy), 0, 32) # create game window
    pg.display.set_caption('Shooting Game') # set game window title

    enemyImg = pg.image.load('enemy.png') # load enemy image file
    bulletImg = pg.image.load('bullet.png') # load bullet projectile image file
    heroImg = pg.image.load('hero.png') # load player image file

    while True: # run game
        game()

def game ():
    global heroWidth, heroHeight
    
    # dimensions of player image
    heroWidth = heroImg.get_width()
    heroHeight = heroImg.get_height()
    enemyWidth = enemyImg.get_width()
    enemyHeight = enemyImg.get_height()

    # starting x and y position of player
    herox = 0
    heroy = (windowy / 2) - (heroHeight / 2)
    
    # player speed
    heroSpeed = 5

    # stores objects
    enemyObj = []
    bulletObj = []
    
    # main loop
    while True:
        
        window.fill(black) # window background

        mousePos = pg.mouse.get_pos()

        bChangex = 0
        bChangey = 0

        for bObj in bulletObj: # move bullet(s)
            #budx, budy = bObj['x'] - mousePos[0], bObj['y'] - mousePos[1]
            #budist = math.hypot(budx, budy)
            #budx, budy = budx / budist, budy / budist
            #bObj['x'] -= budx * bObj['speed']
            #bObj['y'] -= budy * bObj['speed']
            
            bVx = mousePos[0] - herox
            bVy = mousePos[1] - heroy
            vLength = math.sqrt(bVx**2 + bVy**2)
            bVx = (bVx / vLength) * 5
            bVy = (bVy / vLength) * 5
            bObj['x'] += bVx
            bObj['y'] += bVy
            

        for eObj in enemyObj: # move enemy towards player
            endx, endy = eObj['x'] - herox, eObj['y'] - heroy
            endist = math.hypot(endx, endy)
            endx, endy = endx / endist, endy / endist
            eObj['x'] -= endx * eObj['speed']
            eObj['y'] -= endy * eObj['speed']
        
        for bObj in bulletObj: # draw bullet(s)
            bObj['rect'] = pg.Rect((bObj['x'], bObj['y'], bObj['width'], bObj['height']))
            window.blit(bulletImg, bObj['rect'])

        for eObj in enemyObj: # draw enemy
            eObj['rect'] = pg.Rect((eObj['x'], eObj['y'], eObj['width'], eObj['height']))
            window.blit(enemyImg, eObj['rect'])

        if len(enemyObj) < enemiesSpawn: # spawn new enemy
            enemyObj.append(spawnEnemy(enemyWidth, enemyHeight, windowx))

        for i in range(len(bulletObj) -1, -1, -1): # delete bullet once outside game window
            if offScreen(windowx, windowy, bulletObj[i]):
                del bulletObj[i]

        for i in range(len(enemyObj) -1, -1, -1): # delete enemy once outside game window
            if offScreen(windowx, windowy, enemyObj[i]):
                del enemyObj[i]

        #for i in range(len(enemyObj) -1, -1, -1):
            #enObj = enemyObj[i]
            #buObj = bulletObj[i]
            #if 'rect' in enObj and 'rect' in buObj:#bulletObj['rect'].colliderect(enObj['rect']):
                #del enemyObj[i]
        for eObj in enemyObj: # delete enemy on bullet collision
            enemyOb = pg.Rect((eObj['x'], eObj['y'], eObj['width'], eObj['height']))
            for bObj in bulletObj:
                bulletOb = pg.Rect((bObj['x'], bObj['y'], bObj['width'], bObj['height']))
                if bulletOb.colliderect(enemyOb):
                    del enemyObj[i]
                    del bulletObj[i]

        # check for keyboard input
        keys = pg.key.get_pressed()
        if keys[moveUpKey]: # move player up
            heroy -= heroSpeed
            if heroy < 0: # prevent player leaving screen upwards
                heroy = 0
        if keys[moveDownKey]: # move player down
            heroy += heroSpeed
            if (heroy + heroHeight) > windowy: # prevent player leaving screen down
                heroy = windowy - heroHeight
        if keys[moveLeftKey]:
            herox -= heroSpeed
            if herox < 0:
                herox = 0
        if keys[moveRightKey]:
            herox += heroSpeed
            if (herox + heroWidth) > windowx:
                herox = windowx - heroWidth

        window.blit(heroImg, (herox, heroy)) # draw player

        if keys[quitKey]: # exit game on key press
            pg.quit()
            sys.exit()
        for event in pg.event.get(): # exit game loop
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # create bullet on mouse click
                bulletObj.append(shootBullet(herox, heroy, mousePos))

        pg.display.update() # update the window
        fpsClock.tick(FPS)

def spawnEnemy (enemyWidth, enemyHeight, windowx):
    en = {}
    en['width'] = enemyImg.get_width()
    en['height'] = enemyImg.get_height()
    en['x'] = windowx - en['width']
    en['y'] = random.randint(0, (windowy - en['width']))
    en['speed'] = random.randint(1, 1)
    return en
    
def shootBullet (herox, heroy, mousePos): # define and store bullet parameters
    bu = {}
    bu['width'] = bulletImg.get_width()
    bu['height'] = bulletImg.get_height()
    bu['x'] = herox + heroWidth
    bu['y'] = heroy + (heroHeight/2)
    bu['speed'] = 15 # bullet speed
    return bu

#def bulletHit (enemyx, enemyy, enemyWidth, enemyHeight, obj):
    #enemyRect = pg.Rect(enemyx, enemyy, enemyWidth, enemyHeight)
    #objRect = pg.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    #return enemyRect.colliderect(objRect)

def offScreen (windowx, windowy, obj): # define when object is outside game window
    screenRect = pg.Rect(0, 0, windowx, windowy)
    objRect = pg.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not screenRect.colliderect(objRect)

if __name__ == '__main__': # run main
    main()

