import pygame
import random
from pygame.locals import *

pygame.init()


screen_width = 864
screen_height = 936

clock = pygame.time.Clock()

Fps = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
font  =pygame.Sysfont("Botsmatic Demo", 60)

white = (255,255,255)

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()-pipe_frequency
score = 0
pass_pipe = False
pipe_gap = 150

#Load images

bg = pygame.image.load("bg.png")
groundimg = pygame.image.load("ground.png")
restartimg = pygame.image.load("restart.png")

def draw_text(text, font, text_col, x, y):
    txt = font.render(text, True, text_col)
    screen.blit(txt, (x, y))

class Pipe(pygame.sprite.Sprite):
    
    def _init_(self, x, y, position):
        pygame.sprite.Sprite._init_(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        #position variable determines if the pipe is coming from the bottom or top
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False


        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True


        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
        
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range (1, 3):
            img = pygame.image.load(f"bird{num}png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        #apply gravity

        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
               self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
               self.clicked == True
               self.vel = -10
            if pygame.mouse. get_pressed()[0] == 0:
               self.clicked == False

            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]            


pipe_group= pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100,int(screen_height / 2))

bird_group.add(flappy)

button = Button(432, 468, restartimg)

run = True
while run:

    clock.tick(Fps)

    screen.blit(bg, (0,0))

    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    screen.blit(groundimg, (ground_scroll, 768))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
            and pass_pipe == False: 
            pass_pipe = True

        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    draw_text(str(score), font, white, 432, 10)
        
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True
    
    if flappy.rect.bottom >= 768:
        game_over = True
        Flying = False


