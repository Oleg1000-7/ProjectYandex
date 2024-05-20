from button import Button
from constants import *


class Settings:
    def __init__(self):
        self.main_surface = pygame.Surface((screen_w, screen_h))
        main_surface_w, main_surface_h = self.main_surface.get_size()
        self.buttons = [Button(self.main_surface, main_surface_w // 2, main_surface_h // 2 + 100, 100, 50, text="MENU", font_size=25)]

    def __call__(self, mouse_pos, mouse_k):
        scene = "SETTINGS"
        screen.blit(self.main_surface, (0, 0))

        for i in self.buttons:
            i.update(mouse_pos)

        if self.buttons[0].is_clicked(mouse_pos, mouse_k):
            scene = "MENU"

        text = pygame.font.SysFont("Arial", 30).render("Здесь пока ничего нет...", True, WHITE)
        screen.blit(text, (self.main_surface.get_size()[0] // 2, 100))

        return scene
