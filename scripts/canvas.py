import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import numpy as np

import cv2
from scripts.core_funcs import vec

    ##############################################################################################

#gonna be the actual drawing surface eventually
class Canvas(pygame.sprite.Sprite):
    def __init__(self):
        pass