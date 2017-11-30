###########################################################################
#   Simple Shooting Game
#
#   Programmed by Fangwulf 2017-11-07
#
#   Dependancies: Python 3 and Pygame 1.9.3
#
###########################################################################

import pygame, sys, random, time, math
from pygame.locals import * # instead of typing pygame.locals.X everytime

FPS = 60 # frames per second the screen updates

WINDOW_WIDTH = 500 # set width of game window
WINDOW_HEIGHT = 500 # set height of game window

# defines RGB values for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# keyboard button assignments
KEY_QUIT = K_ESCAPE
KEY_UP = K_w
KEY_DOWN = K_s
KEY_LEFT = K_a
KEY_RIGHT = K_d

# number of enemies to spawn
NUM_ENEMIES = 1

def main ():
    global fpsClock, window, enemyImg, bulletImg, heroImg # global use variables

    pygame.init() # initialize pygame
    fpsClock = pygame.time.Clock()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32) # create game window
    pygame.display.set_caption('Simple Shooting Game') # set game window title

    enemyImg = pygame.image.load('assets/enemy.png') # load enemy image file
    bulletImg = pygame.image.load('assets/bullet.png') # load bullet projectile image file
    heroImg = pygame.image.load('assets/hero.png') # load player image file

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
    heroX = 0
    heroY = (WINDOW_HEIGHT / 2) - (heroHeight / 2)

    # player speed
    heroSpeed = 5

    # stores objects
    enemyObjs = []
    bulletObjs = []

    # main loop
    while True:
        window.fill(BLACK) # window background
        mousePos = pygame.mouse.get_pos() # get mouse cursor position (x,y)
        keys = pygame.key.get_pressed() # get pressed keyboard keys list

        bChangex = 0
        bChangey = 0

        for bObj in bulletObjs: # move bullet(s)
            #budx, budy = bObj['x'] - mousePos[0], bObj['y'] - mousePos[1]
            #budist = math.hypot(budx, budy)
            #budx, budy = budx / budist, budy / budist
            #bObj['x'] -= budx * bObj['speed']
            #bObj['y'] -= budy * bObj['speed']
            bVx = mousePos[0] - heroX
            bVy = mousePos[1] - heroY
            vLength = math.sqrt(bVx**2 + bVy**2)
            bVx = (bVx / vLength) * 5
            bVy = (bVy / vLength) * 5
            bObj['x'] += bVx
            bObj['y'] += bVy

        for eObj in enemyObjs: # move enemy towards player
            endx, endy = eObj['x'] - heroX, eObj['y'] - heroY
            endist = math.hypot(endx, endy)
            endx, endy = endx / endist, endy / endist
            eObj['x'] -= endx * eObj['speed']
            eObj['y'] -= endy * eObj['speed']

        for bObj in bulletObjs: # draw bullet
            bObj['rect'] = pygame.Rect((bObj['x'], bObj['y'], bObj['width'], bObj['height']))
            window.blit(bulletImg, bObj['rect'])

        for eObj in enemyObjs: # draw enemy
            eObj['rect'] = pygame.Rect((eObj['x'], eObj['y'], eObj['width'], eObj['height']))
            window.blit(enemyImg, eObj['rect'])

        if len(enemyObjs) < NUM_ENEMIES: # spawn new enemy
            enemyObjs.append(spawnEnemy(enemyWidth, enemyHeight, WINDOW_WIDTH))

        for i in range(len(bulletObjs) -1, -1, -1): # delete bullet once outside game window
            if offScreen(WINDOW_WIDTH, WINDOW_HEIGHT, bulletObjs[i]):
                del bulletObjs[i]

        for i in range(len(enemyObjs) -1, -1, -1): # delete enemy once outside game window
            if offScreen(WINDOW_WIDTH, WINDOW_HEIGHT, enemyObjs[i]):
                del enemyObjs[i]

        #for i in range(len(enemyObjs) -1, -1, -1):
            #enObj = enemyObjs[i]
            #buObj = bulletObjs[i]
            #if 'rect' in enObj and 'rect' in buObj:#bulletObjs['rect'].colliderect(enObj['rect']):
                #del enemyObjs[i]
        for eObj in enemyObjs: # delete enemy on bullet collision
            enemyOb = pygame.Rect((eObj['x'], eObj['y'], eObj['width'], eObj['height']))
            for bObj in bulletObjs:
                bulletOb = pygame.Rect((bObj['x'], bObj['y'], bObj['width'], bObj['height']))
                if bulletOb.colliderect(enemyOb):
                    del enemyObjs[i]
                    del bulletObjs[i]

        # check for keyboard input
        if keys[KEY_UP]: # move player up
            heroY -= heroSpeed
            if heroY < 0: # prevent player leaving screen upwards
                heroY = 0
        if keys[KEY_DOWN]: # move player down
            heroY += heroSpeed
            if (heroY + heroHeight) > WINDOW_HEIGHT: # prevent player leaving screen down
                heroY = WINDOW_HEIGHT - heroHeight
        if keys[KEY_LEFT]: # move player left
            heroX -= heroSpeed
            if heroX < 0: # prevent player leaving screen left
                heroX = 0
        if keys[KEY_RIGHT]: # move player right
            heroX += heroSpeed
            if (heroX + heroWidth) > WINDOW_WIDTH: # prevent player leving screen right
                heroX = WINDOW_WIDTH - heroWidth

        window.blit(heroImg, (heroX, heroY)) # draw player

        if keys[KEY_QUIT]: # exit game on key press
            pygame.quit()
            sys.exit()
        for event in pygame.event.get(): # exit game loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # create bullet on mouse click
                bulletObjs.append(shootBullet(heroX, heroY, mousePos))

        pygame.display.update() # update the window
        fpsClock.tick(FPS)

def spawnEnemy (enemyWidth, enemyHeight, WINDOW_WIDTH):
    en = {}
    en['width'] = enemyImg.get_width()
    en['height'] = enemyImg.get_height()
    en['x'] = WINDOW_WIDTH - en['width']
    en['y'] = random.randint(0, (WINDOW_HEIGHT - en['width']))
    en['speed'] = random.randint(1, 1)
    return en

def shootBullet (heroX, heroY, mousePos): # define and store bullet parameters
    bu = {}
    bu['width'] = bulletImg.get_width()
    bu['height'] = bulletImg.get_height()
    bu['x'] = heroX + heroWidth
    bu['y'] = heroY + (heroHeight/2)
    bu['speed'] = 15 # bullet speed
    return bu

#def bulletHit (enemyx, enemyy, enemyWidth, enemyHeight, obj):
    #enemyRect = pygame.Rect(enemyx, enemyy, enemyWidth, enemyHeight)
    #objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    #return enemyRect.colliderect(objRect)

def offScreen (WINDOW_WIDTH, WINDOW_HEIGHT, obj): # define when object is outside game window
    screenRect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not screenRect.colliderect(objRect)

if __name__ == '__main__': # run main
    main()
