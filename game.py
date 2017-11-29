###########################################################################
#   Shooting Game
#
#   Programmed by Josh Follett 2017-11-07
#
#   Dependancies: Python 3.6 and Pygame 1.9.3
#
###########################################################################

import pygame, sys, random, time, math
from pygame.locals import * # instead of typing pygame.locals.X everytime

FPS = 60 # frames per second the screen updates

windowWidth = 500 # set width of game window
windowHeight = 500 # set height of game window

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
    global fpsClock, window, enemyImg, bulletImg, heroImg # global use variables

    pygame.init() # initialize pygame
    fpsClock = pygame.time.Clock()

    window = pygame.display.set_mode((windowWidth, windowHeight), 0, 32) # create game window
    pygame.display.set_caption('Shooting Game') # set game window title

    enemyImg = pygame.image.load('enemy.png') # load enemy image file
    bulletImg = pygame.image.load('bullet.png') # load bullet projectile image file
    heroImg = pygame.image.load('hero.png') # load player image file

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
    heroy = (windowHeight / 2) - (heroHeight / 2)

    # player speed
    heroSpeed = 5

    # stores objects
    enemyObj = []
    bulletObj = []

    # main loop
    while True:

        window.fill(black) # window background

        mousePos = pygame.mouse.get_pos()

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
            bObj['rect'] = pygame.Rect((bObj['x'], bObj['y'], bObj['width'], bObj['height']))
            window.blit(bulletImg, bObj['rect'])

        for eObj in enemyObj: # draw enemy
            eObj['rect'] = pygame.Rect((eObj['x'], eObj['y'], eObj['width'], eObj['height']))
            window.blit(enemyImg, eObj['rect'])

        if len(enemyObj) < enemiesSpawn: # spawn new enemy
            enemyObj.append(spawnEnemy(enemyWidth, enemyHeight, windowWidth))

        for i in range(len(bulletObj) -1, -1, -1): # delete bullet once outside game window
            if offScreen(windowWidth, windowHeight, bulletObj[i]):
                del bulletObj[i]

        for i in range(len(enemyObj) -1, -1, -1): # delete enemy once outside game window
            if offScreen(windowWidth, windowHeight, enemyObj[i]):
                del enemyObj[i]

        #for i in range(len(enemyObj) -1, -1, -1):
            #enObj = enemyObj[i]
            #buObj = bulletObj[i]
            #if 'rect' in enObj and 'rect' in buObj:#bulletObj['rect'].colliderect(enObj['rect']):
                #del enemyObj[i]
        for eObj in enemyObj: # delete enemy on bullet collision
            enemyOb = pygame.Rect((eObj['x'], eObj['y'], eObj['width'], eObj['height']))
            for bObj in bulletObj:
                bulletOb = pygame.Rect((bObj['x'], bObj['y'], bObj['width'], bObj['height']))
                if bulletOb.colliderect(enemyOb):
                    del enemyObj[i]
                    del bulletObj[i]

        playerMove(herox, heroy, heroWidth, heroHeight, windowWidth, windowHeight)
        window.blit(heroImg, (herox, heroy)) # draw player

        if keys[quitKey]: # exit game on key press
            pygame.quit()
            sys.exit()
        for event in pygame.event.get(): # exit game loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # create bullet on mouse click
                bulletObj.append(shootBullet(herox, heroy, mousePos))

        pygame.display.update() # update the window
        fpsClock.tick(FPS)

def spawnEnemy (enemyWidth, enemyHeight, windowWidth):
    en = {}
    en['width'] = enemyImg.get_width()
    en['height'] = enemyImg.get_height()
    en['x'] = windowWidth - en['width']
    en['y'] = random.randint(0, (windowHeight - en['width']))
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
    #enemyRect = pygame.Rect(enemyx, enemyy, enemyWidth, enemyHeight)
    #objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    #return enemyRect.colliderect(objRect)

def offScreen (windowWidth, windowHeight, obj): # define when object is outside game window
    screenRect = pygame.Rect(0, 0, windowWidth, windowHeight)
    objRect = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
    return not screenRect.colliderect(objRect)

def playerMove (herox, heroy, heroWidth, heroHeight, windowWidth, windowHeight):
    # check for keyboard input
    keys = pygame.key.get_pressed()
    if keys[moveUpKey]: # move player up
        heroy -= heroSpeed
        if heroy < 0: # prevent player leaving screen upwards
            heroy = 0
    if keys[moveDownKey]: # move player down
        heroy += heroSpeed
        if (heroy + heroHeight) > windowHeight: # prevent player leaving screen down
            heroy = windowHeight - heroHeight
    if keys[moveLeftKey]:
        herox -= heroSpeed
        if herox < 0:
            herox = 0
    if keys[moveRightKey]:
        herox += heroSpeed
        if (herox + heroWidth) > windowWidth:
            herox = windowWidth - heroWidth

if __name__ == '__main__': # run main
    main()
