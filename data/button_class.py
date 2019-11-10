import os
import sys

with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f

    import pygame as pg

    # enable stdout
    sys.stdout = oldstdout

class button(object):

    def __init__(self, surface, image_path, pos, text, font = "Calibri"):
        self.surface = surface
        self.image_path = image_path
        self.pos = pos
        self.text = text
        self.pressable = True
        self.pressed = False
        self.font = font

        self.image_not_pressed =  pg.image.load(self.image_path[0])
        self.width = self.image_not_pressed.get_rect().size[0]
        self.height = self.image_not_pressed.get_rect().size[1]
        self.image_not_pressed.convert()
        self.image_pressed =  pg.image.load(self.image_path[1])
        self.image_pressed.convert()
        self.hitbox = pg.draw.rect(self.surface, (0,0,0), [self.pos[0], self.pos[1], self.width, self.height], 0)

    def draw(self):
        self.hitbox = pg.draw.rect(self.surface, (0,0,0), [self.pos[0], self.pos[1], self.width, self.height], 0)
    	if self.pressed == True:
    		self.surface.blit(self.image_pressed, self.image_pressed.get_rect(center = (self.pos[0]+self.width/2, self.pos[1]+self.height/2) ) )
    		wrnfont = pg.font.SysFont(self.font, 50)
    		self.textbox = wrnfont.render(self.text[1], True, (255,255,255), None)
        	self.surface.blit(self.textbox, self.textbox.get_rect(center = (self.pos[0]+self.width/2, self.pos[1]+self.height/2) ) )
    	else:
    		self.surface.blit(self.image_not_pressed, self.image_not_pressed.get_rect(center = (self.pos[0]+self.width/2, self.pos[1]+self.height/2) ) )
    		wrnfont = pg.font.SysFont(self.font, 50)
    		self.textbox = wrnfont.render(self.text[0], True, (255,255,255), None)
        	self.surface.blit(self.textbox, self.textbox.get_rect(center = (self.pos[0]+self.width/2, self.pos[1]+self.height/2) ) )

    def detect(self, event_pos):
    	if self.hitbox.collidepoint(event_pos) and self.pressable == True:
            if self.pressed == False:
                self.pressed = True
                return "pressed"
            else:
                self.pressed = False
                return "unpressed"