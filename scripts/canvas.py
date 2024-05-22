import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import numpy as np

import cv2

from scripts.core_funcs import vec
from scripts.core_funcs import vec, gen_colour, roundline

    ##############################################################################################

#gonna be the actual drawing surface eventually
class Canvas(pygame.sprite.Sprite):
    def __init__(self, cam, size=(1140, 768), pos=(0, 0)):
        self.cam = cam

        self.pos = pos
        self.size = size
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.last_pos = vec()

        self.bg_color = (49, 51, 56)
    
    #whether or not the pencil should be drawing rn
    #might change this to some sort of depth calculation, e.g. if the circle radius < 10
    @property
    def drawing(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_e]
    
    @property
    def erasing(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_r]

    def tip_to_screen_pos(self, tip_pos):
        screen_x = (tip_pos[0] / 480) * self.size[0]
        screen_y = (tip_pos[1] / 640) * self.size[1]
        return (screen_x, screen_y)

    def draw(self):
        pos = self.tip_to_screen_pos(self.cam.tip_pos)
        if self.drawing:
            pygame.draw.circle(self.surf, self.cam.tip_col, pos, self.cam.radius)
            roundline(self.surf, self.cam.tip_col, pos, self.last_pos if self.last_pos != (0, 0) else pos, self.cam.radius)
            self.tip_col = gen_colour()
        elif self.erasing:
            pygame.draw.circle(self.surf, self.bg_color, pos, self.cam.radius)
            roundline(self.surf, self.bg_color, pos, self.last_pos if self.last_pos != (0, 0) else pos, self.cam.radius)
            self.tip_col = gen_colour()
        self.last_pos = pos
