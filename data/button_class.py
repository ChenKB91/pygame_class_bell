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

    def __init__(self, surface, image_path, pos, text, font = ["Calibri"], font_size=[50], font_color=[[(40,40,40),(100,100,100)]], text_pos=[[0,0]], pressed=False, offset="middle"):
        self.surface = surface
        self.image_path = image_path
        self.pos = pos
        self.text = text
        self.pressable = True
        self.pressed = pressed
        self.font = font
        self.font_size = font_size
        self.font_color = font_color
        self.text_pos = text_pos
        self.offset = offset

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

            for i in range(len(self.text)):
                wrnfont = pg.font.SysFont(self.font[i], self.font_size[i])
                self.textbox = wrnfont.render(self.text[i][1], True, self.font_color[i][1], None)
                self.text_rect = self.textbox.get_rect(center = (self.pos[0]+self.width/2 + self.text_pos[i][0],self.pos[1]+self.height/2 + self.text_pos[i][1]) ) 
                if self.offset == "left":
                    self.text_rect.left = self.hitbox.left + 9
                self.surface.blit(self.textbox, self.text_rect)
        else:
            self.surface.blit(self.image_not_pressed, self.image_not_pressed.get_rect(center = (self.pos[0]+self.width/2, self.pos[1]+self.height/2) ) )

            for i in range(len(self.text)) :
                wrnfont = pg.font.SysFont(self.font[i], self.font_size[i])
                self.textbox = wrnfont.render(self.text[i][0], True, self.font_color[i][0], None)
                self.text_rect = self.textbox.get_rect(center = (self.pos[0]+self.width/2 + self.text_pos[i][0], self.pos[1]+self.height/2 + self.text_pos[i][1]) ) 
                if self.offset == "left":
                    self.text_rect.left = self.hitbox.left + 9
                self.surface.blit(self.textbox, self.text_rect)

    def detect(self, event_pos):
    	if self.hitbox.collidepoint(event_pos) and self.pressable == True:
            if self.pressed == False:
                self.pressed = True
                return "pressed"
            else:
                self.pressed = False
                return "unpressed"