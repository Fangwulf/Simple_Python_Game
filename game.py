###########################################################################
#   Simple Shooting Game
#
#   Programmed by Fangwulf 2017-11-07
#
#   Dependancies: Python 3 and Pygame 1.9.3
#
###########################################################################
# import needed modules
import pygame, sys, random, time, math
from pygame.locals import * # instead of typing pygame.locals.X everytime
###########################################################################
# frames per second the screen updates
FPS = 60
# create clock for FPS
FPS_CLOCK = pygame.time.Clock()
# set game window width and height
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
WINDOW_RECT = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
# defines RGB values for colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# number of enemies to spawn
NUM_ENEMIES = 2
# player values
PLAYER_SPEED = 5
PLAYER_HEALTH_MAX = 99
# enemy values
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 3
ENEMY_IMG = pygame.image.load('assets/enemy.png')
###########################################################################
# defines main function
def main ():
    # global use variables
    global window, enemyImg, bulletImg, playerImg, textFont, textFontSmall
    # initialize pygame
    pygame.init()
    # create game window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    # set game window title
    pygame.display.set_caption('Simple Shooting Game')
    # load enemy image file
    enemyImg = pygame.image.load('assets/enemy.png')
    # load bullet projectile image file
    bulletImg = pygame.image.load('assets/bullet.png')
    # load player image file
    playerImg = pygame.image.load('assets/player.png')
    # creates text font
    textFont = pygame.font.Font('freesansbold.ttf', 32)
    textFontSmall = pygame.font.Font('freesansbold.ttf', 20)
    # runs game function
    while True:
        game()
###########################################################################
# defines game function
def game ():
    # global use variables
    global playerWidth, playerHeight
    # assign game screen boolean
    startGame = False
    gameOver = False
    # dimensions of player image
    playerWidth = playerImg.get_width()
    playerHeight = playerImg.get_height()
    # starting x and y position of player
    playerX = 0
    playerY = (WINDOW_HEIGHT / 2) - (playerHeight / 2)
    playerAngle = 0
    # assign player health
    playerHealth = PLAYER_HEALTH_MAX
    # assign score
    score = 0
    # stores objects
    enemyObjs = []
    bulletObjs = []
    # main loop
    while True:
        # game window background
        window.fill(BLACK)
        # get pressed keyboard keys list
        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        # create player rectangle
        playerRect = pygame.Rect(playerX, playerY,
            playerWidth, playerHeight)
        playerCenter = (playerX + (playerWidth / 2),
            playerY + (playerHeight / 2))
        # draw score
        if (not gameOver) and startGame:
            scoreScreen(score)
            healthScreen(playerHealth)
        # move bullet(s)
        for bullet in bulletObjs:
            #bullet['x'] += bullet['speed']
            bullet['x'] += bullet['moveX']
            bullet['y'] += bullet['moveY']
            bullet['rect'] = pygame.Rect((bullet['x'], bullet['y'],
                bullet['width'], bullet['height']))
        # move enemy towards player
        if  (not gameOver) and startGame:
            for enemy in enemyObjs:
                enemyX = enemy['x'] - playerX
                enemyY = enemy['y'] - playerY
                enemyDist = math.hypot(enemyX, enemyY)
                enemyX = enemyX / enemyDist
                enemyY = enemyY / enemyDist
                enemy['x'] -= enemyX * enemy['speed']
                enemy['y'] -= enemyY * enemy['speed']
        # draw bullet
        for bullet in bulletObjs:
            #bullet['rect'] = pygame.Rect((bullet['x'], bullet['y'],
                #bullet['width'], bullet['height']))

            window.blit(bullet['image'], bullet['rect'])
        # draw enemy facing player
        if (not gameOver) and startGame:
            for enemy in enemyObjs:
                enemyAngle = (360 - ((math.atan2(playerCenter[1] - enemy['y'],
                    playerCenter[0] - enemy['x']) * 180) / math.pi))
                enemyImgRot = pygame.transform.rotate(enemyImg,
                    (enemyAngle + 180))
                enemyRect = enemyImgRot.get_rect(center = (enemy['x'],
                    enemy['y']))
                window.blit(enemyImgRot, enemyRect)
        # replace deleted enemies
        while len(enemyObjs) < NUM_ENEMIES:
            enemyObjs.append(spawnEnemy(WINDOW_WIDTH))
        # delete bullet once outside game window
        for i in range(len(bulletObjs) -1, -1, -1):
            if not collision(WINDOW_RECT, bulletObjs[i]['rect']):
                del bulletObjs[i]
        # delete enemy once outside game window
        for i in range(len(enemyObjs) -1, -1, -1):
            if not collision(WINDOW_RECT, enemyObjs[i]['rect']):
                del enemyObjs[i]
        # delete enemy on bullet collision
        for n in range(len(bulletObjs) -1, -1, -1):
            bulletObj = bulletObjs[n]
            for i in range(len(enemyObjs) -1, -1, -1):
                enemyObj = enemyObjs[i]
                if collision(bulletObj['rect'], enemyObj['rect']):
                    try:
                        del enemyObjs[i]
                        del bulletObjs[n]
                    except:
                        print('Collision exception!')
                        pass
                    score +=1
        # decrease player health if enemy collides with player
        for i in range(len(enemyObjs) -1, -1, -1):
            enemyRect = pygame.Rect(enemyObjs[i]['x'], enemyObjs[i]['y'],
                enemyObjs[i]['width'], enemyObjs[i]['height'])
            if collision(enemyRect, playerRect):
                del enemyObjs[i]
                playerHealth -= 1
        # set game over if player looses all health
        if playerHealth <= 0:
            gameOver = True
        # check for keyboard input
        # move player up
        if (not gameOver) and startGame:
            if keys[K_UP] or keys[K_w]:
                playerY -= PLAYER_SPEED
                # prevent player leaving screen upwards
                if playerY < 0:
                    playerY = 0
            # move player down
            if keys[K_DOWN] or keys[K_s]:
                playerY += PLAYER_SPEED
                # prevent player leaving screen down
                if (playerY + playerHeight) > WINDOW_HEIGHT:
                    playerY = WINDOW_HEIGHT - playerHeight
            # move player left
            if keys[K_LEFT] or keys[K_a]:
                playerX -= PLAYER_SPEED
                # prevent player leaving screen left
                if playerX < 0:
                    playerX = 0
            # move player right
            if keys[K_RIGHT] or keys[K_d]:
                playerX += PLAYER_SPEED
                # prevent player leving screen right
                if (playerX + playerWidth) > WINDOW_WIDTH:
                    playerX = WINDOW_WIDTH - playerWidth
            # rotate player
            playerAngle = (360 - ((math.atan2(mousePos[1] - playerY,
                mousePos[0] - playerX) * 180) / math.pi))
            playerImgRot = pygame.transform.rotate(playerImg, playerAngle)
            playerRect = playerImgRot.get_rect(center = (playerCenter))
            # draw player
            window.blit(playerImgRot, playerRect)
        # show start screen
        elif not startGame:
            startGameScreen()
        # show game over screen
        elif gameOver:
            gameOverScreen(score)
        # start game
        if keys[K_RETURN] and not startGame:
            startGame = True
        # restart game after game over
        if keys[K_RETURN] and gameOver:
            playerX = 0
            playerY = (WINDOW_HEIGHT / 2) - (playerHeight / 2)
            playerHealth = PLAYER_HEALTH_MAX
            score = 0
            gameOver = False
        # exit game on key press
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        # scan pygame events
        for event in pygame.event.get():
            # exit game loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # create bullet on button press or mouse click
            if (not gameOver) and startGame:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    bulletObjs.append(spawnBullet(playerCenter))
                #if event.type == KEYDOWN:
                    #if event.key == K_SPACE:
                        #bulletObjs.append(spawnBullet(playerX, playerY))
        # update the window
        pygame.display.update()
        # add tick to FPS_CLOCK
        FPS_CLOCK.tick(FPS)
###########################################################################
# defines enemy spawn function, takes width of game window
def spawnEnemy (WINDOW_WIDTH):
    enemy = {}
    enemy['width'] = ENEMY_IMG.get_width()
    enemy['height'] = ENEMY_IMG.get_height()
    enemy['x'] = WINDOW_WIDTH - enemy['width']
    enemy['y'] = random.randint(0, (WINDOW_HEIGHT - enemy['width']))
    enemy['speed'] = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
    enemy['rect'] = pygame.Rect(enemy['x'], enemy['y'],
        enemy['width'], enemy['height'] )
    return enemy
###########################################################################
# defines bullet spawn function, takes player x and y
def spawnBullet (playerCenter):
    bullet = {}
    bullet['width'] = bulletImg.get_width()
    bullet['height'] = bulletImg.get_height()
    bullet['x'] = playerCenter[0]
    bullet['y'] = playerCenter[1]
    bullet['speed'] = 15
    mousePos = pygame.mouse.get_pos()
    bulletDistX = mousePos[0] - bullet['x']
    bulletDistY = mousePos[1] - bullet['y']
    vector = math.sqrt(bulletDistX**2 + bulletDistY**2)
    bullet['moveX'] = (bulletDistX / vector) * 5
    bullet['moveY'] = (bulletDistY / vector) * 5

    bullet['angle'] = (360 - ((math.atan2(mousePos[1] - bullet['y'],
        mousePos[0] - bullet['x']) * 180) / math.pi))
    bullet['image'] = pygame.transform.rotate(bulletImg, bullet['angle'])
    bullet['rect'] = bullet['image'].get_rect(center = (bullet['x'],
        bullet['y']))
    #bullet['rect'] = pygame.Rect(bullet['x'], bullet['y'],
        #bullet['width'], bullet['height'] )
    return bullet
###########################################################################
# defines object collision, takes two object rect attributes
def collision (rect1, rect2):
    return rect1.colliderect(rect2)
###########################################################################
# defines screen that shows at start
def startGameScreen ():
    startText1 = textFont.render('Simple Shooter Game', True, WHITE)
    startRect1 = startText1.get_rect()
    startRect1.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 100)
    startText2 = textFont.render('WASD or ARROW keys move.',
        True, WHITE)
    startRect2 = startText2.get_rect()
    startRect2.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 50)
    startText3 = textFont.render('SPACE key shoots.', True, WHITE)
    startRect3 = startText3.get_rect()
    startRect3.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    startText4 = textFont.render('Press ENTER to start.', True, WHITE)
    startRect4 = startText4.get_rect()
    startRect4.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) + 50)
    window.blit(startText1, startRect1)
    window.blit(startText2, startRect2)
    window.blit(startText3, startRect3)
    window.blit(startText4, startRect4)
    return
###########################################################################
# defines game over screen, takes score
def gameOverScreen (score):
    gameOverText1 = textFont.render('GAME OVER', True, WHITE)
    gameOverRect1 = gameOverText1.get_rect()
    gameOverRect1.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 100)
    gameOverText2 = textFont.render(('Your final score is ' +
        str(score) + '.'), True, WHITE)
    gameOverRect2 = gameOverText2.get_rect()
    gameOverRect2.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 50)
    gameOverText3 = textFont.render('Press ENTER to restart.', True, WHITE)
    gameOverRect3 = gameOverText3.get_rect()
    gameOverRect3.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    gameOverText4 = textFont.render('Press ESCAPE to exit.', True, WHITE)
    gameOverRect4 = gameOverText4.get_rect()
    gameOverRect4.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) + 50)
    window.blit(gameOverText1, gameOverRect1)
    window.blit(gameOverText2, gameOverRect2)
    window.blit(gameOverText3, gameOverRect3)
    window.blit(gameOverText4, gameOverRect4)
    return
###########################################################################
# defines score box
def scoreScreen (score):
    scoreText = textFontSmall.render(('Score: ' + str(score)),
        True, WHITE)
    scoreRect = scoreText.get_rect()
    scoreRect.x = 5
    scoreRect.y = 5
    window.blit(scoreText, scoreRect)
    return
###########################################################################
# definse health text box
def healthScreen (playerHealth):
    healthText = textFontSmall.render(('Health: ' + str(playerHealth)),
        True, WHITE)
    healthRect = healthText.get_rect()
    healthRect.x = 5
    healthRect.y = 30
    window.blit(healthText, healthRect)
###########################################################################
# run main function
if __name__ == '__main__':
    main()
###########################################################################
