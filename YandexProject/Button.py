from Constants import *
import pygame

class Button:
    def __init__(self, surface, rect, color=WHITE, text="", text_color=BLACK):
        self.surface = surface
        self.rect = rect
        self.color = color
        self.text = text

    def make_button(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
        # self.surface.blit(button_text, button_rect_center)
