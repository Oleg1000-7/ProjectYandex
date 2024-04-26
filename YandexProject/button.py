from constants import *
import pygame


class Button:
    def __init__(self, surface, x, y, button_w, button_h, color=WHITE, text="", text_color=BLACK, font_size = 30):
        self.surface = surface
        self.rect = pygame.Rect(x, y, button_w, button_h)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size

    def draw(self):
        from main import screen
        text = pygame.font.SysFont("arial", self.font_size).render(self.text, True, self.text_color)
        pygame.draw.rect(self.surface, self.color, self.rect)
        screen.blit(text, (self.rect.x + self.rect.width / 4, self.rect.y + self.rect.height / 4))

    def isClicked(self, other):
        return self.rect.contains(other)
