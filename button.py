from constants import *


class Button:
    def __init__(self, surface, x, y, button_w, button_h, color=WHITE, text="", text_color=BLACK, font_size=30):
        self.surface = surface
        self.rect = pygame.Rect(x - button_w // 2, y + button_h // 2, button_w, button_h)
        self.color = color
        self.cur_col = color
        self.txt = text
        self.text_color = text_color
        self.font_size = font_size
        self.text = pygame.font.SysFont("Arial", self.font_size).render(self.txt, True, self.text_color)
        self.dx = (button_w - self.text.get_width()) / 2
        self.dy = (button_h - self.text.get_height()) / 2
        self.dx *= self.dx > 0
        self.dy *= self.dy > 0

    def update(self, mouse_pos):
        pygame.draw.rect(self.surface, self.cur_col, self.rect)
        screen.blit(self.text, (self.rect.x + self.dx, self.rect.y + self.dy))

        if self.rect.collidepoint(mouse_pos):
            pointed = True
            self.cur_col = pygame.Color(self.color.r // 2, self.color.g // 2, self.color.b // 2)

        else:
            pointed = False
            self.cur_col = self.color

        return pointed

    def is_clicked(self, mouse_pos, mouse_k):
        return self.rect.collidepoint(mouse_pos) and mouse_k[0]
