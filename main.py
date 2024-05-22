import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    
import sys
import time

from scripts.camera import Camera
from scripts.canvas import Canvas
from scripts.core_funcs import gen_colour, roundline

    ##############################################################################################

#initialising pygame stuff
pygame.init()  #general pygame
pygame.font.init() #font stuff
pygame.event.set_blocked(None) #setting allowed events to reduce lag
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION])
pygame.display.set_caption("")

#initalising pygame window
flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
SIZE = WIDTH, HEIGHT = (1400, 768)
screen = pygame.display.set_mode(SIZE, flags, 16)
screen.fill((20, 20, 20))
clock = pygame.time.Clock()

    ##############################################################################################

last_pos = (0, 0)

cam = Camera()
canvas = Canvas(cam)

    ##############################################################################################

last_time = time.time()

running = True
while cam.recording and running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

        #################################################

    screen.fill((30, 31, 34))
    pygame.draw.rect(screen, (43, 45, 49), [1140, 0, 20, HEIGHT])
    pygame.draw.rect(screen, (49, 51, 56), [0, 0, 1140, HEIGHT])

    result = cam.update()
    if result == "Nothing": running = False

        #################################################

    canvas.draw()
    screen.blit(canvas.surf, (0, 0))
    screen.blit(cam.surf, cam.surf.get_rect(topright=(WIDTH, 0)))

    pos = canvas.tip_to_screen_pos(cam.tip_pos)
    pygame.draw.circle(screen, (175, 31, 55), pos, cam.radius, 1)
    roundline(screen, (175, 31, 55), pos, last_pos if last_pos != (0, 0) else pos, cam.radius, width=1)
    cam.tip_col = gen_colour()
    last_pos = pos

        #################################################

    pygame.display.update()

pygame.quit()
sys.exit()
