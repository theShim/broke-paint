import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.locals import *
    
import sys
import time

from scripts.camera import Camera

    ##############################################################################################

#initialising pygame stuff
pygame.init()  #general pygame
pygame.font.init() #font stuff
pygame.event.set_blocked(None) #setting allowed events to reduce lag
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION])
pygame.display.set_caption("")

#initalising pygame window
flags = pygame.DOUBLEBUF #| pygame.FULLSCREEN
SIZE = WIDTH, HEIGHT = (1200, 768)
screen = pygame.display.set_mode(SIZE, flags, 16)
clock = pygame.time.Clock()

    ##############################################################################################

def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(int(distance)):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)

def tip_to_screen_pos(tip_pos):
    screen_x = (tip_pos[0] / 480) * WIDTH
    screen_y = (tip_pos[1] / 640) * HEIGHT
    return (screen_x, screen_y)

last_pos = (0, 0)

    ##############################################################################################

cam = Camera()

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

    pos = tip_to_screen_pos(cam.tip_pos)
    if cam.drawing:
        pygame.draw.circle(screen, (255, 0, 255), pos, cam.radius)
        roundline(screen, (255, 0, 255), pos, last_pos if last_pos != (0, 0) else pos, cam.radius)
    last_pos = pos

        #################################################

    result = cam.update()
    if result == "Nothing": running = False

        #################################################

    screen.blit(cam.surf, cam.surf.get_rect(topright=(WIDTH, 0)))

        #################################################

    pygame.display.update()

pygame.quit()
sys.exit()