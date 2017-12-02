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
FPS_CLOCK = pygame.time.Clock()
# set width of game screen
SCREEN_WIDTH = 500
# set height of game screen
SCREEN_HEIGHT = 500
# set screen rect object
SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
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
# player speed
PLAYER_SPEED = 5
###########################################################################
# classes
class Player (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect
        #self.rect = self.rect.move(0, 0)
    def update (self):
        # move player up
        if keys[KEY_UP]:
            print('key up')
            self.rect = self.rect.move(0, -PLAYER_SPEED)
        # move player down
        if keys[KEY_DOWN]:
            self.rect = self.rect.move(0, PLAYER_SPEED)
        # move player left
        if keys[KEY_LEFT]:
            self.rect = self.rect.move(-PLAYER_SPEED, 0)
        # move player right
        if keys[KEY_RIGHT]:
            self.rect = self.rect.move(PLAYER_SPEED, 0)

        #if not SCREEN_RECT.colliderect(self.rect):
            #self.rect = self.rect.move(0,0)

        screen.blit(self.image, (0, 0))
###########################################################################
'''class Bullet (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/bullet.png')
        self.rect = self.image.get_rect

    def update (self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                screen.blit(self.image, self.rect)'''
###########################################################################
'''class enemy (pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/enemy.png')
        self.rect = self.image.get_rect'''
###########################################################################
def game ():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Simple Shooting Game')
    keys = pygame.key.get_pressed()
    while True:
        screen.fill(BLACK)
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        all_sprites.draw(screen)

        for event in pygame.event.get():
            # exit game loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
###########################################################################
if __name__ == '__main__':
    game()
