import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import numpy as np

import cv2

from scripts.core_funcs import vec, gen_colour

    ##############################################################################################
    
rgb_color = np.uint8([[[6, 45, 122]]]) #the blue colour of my pencil knob in rgb
hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)
h, s, v = hsv_color[0][0]

lower_color = np.array([h-10, 100, 100])  #lower bound of the blue color in HSV
upper_color = np.array([h+10, 255, 255])  #upper bound of the blue color in HSV

kernel = np.ones((5, 5), np.uint8) #honestly no idea what this is but it was in a stack overflow article

    ##############################################################################################

class Camera:
    def __init__(self):
        #online url using this app on my phone called droidcam
        self.url = f"http://{'IP not doxxing myself lmao'}/video"
        self.cap = cv2.VideoCapture(self.url)
        self.surf = None

        self.tip_pos = (0, 0) #position of the pencil knob | dynamic
        self.radius = 20 # the radius or size of the knob  | dynamic 
        self.tip_col = gen_colour()

    #if the camera is on or not
    @property
    def recording(self) -> bool:
        return self.cap.isOpened()
    
    def update(self):
        ret, frame = self.cap.read() #actual camera footage
        if not ret:
            return "Nothing"
        
        #rotating and converting to a hsv colour map. also a surface to see current camera footage (will remove, just for testing i think)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        surf = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "BGR")
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #create a mask of the colour i want within a range and clean it up a bit
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea) #find the largest blue area
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour) #find is coordinates and rough radius

            if radius > 5:
                pygame.draw.circle(surf, (0, 255, 0), (int(x), int(y)), int(radius), 2)

            #updating brush position and radius
            self.tip_pos = (x, y)
            self.radius = radius

        #updating the camera
        self.surf = surf
        self.surf = pygame.transform.scale(surf, vec(surf.get_size())*1.5)

    #gonna make a threaded function that does the updating in its own thread, hopefully will increase the fps
    def threaded_(self):
        pass
