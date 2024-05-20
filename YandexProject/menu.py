from button import Button
from constants import *


class Menu:
    def __init__(self):
        self.main_surface = pygame.Surface((screen_w, screen_h))
        main_surface_w, main_surface_h = self.main_surface.get_size()
        self.buttons = [
            Button(self.main_surface, main_surface_w // 2, main_surface_h // 2, 150, 50, text="Play"),
            Button(self.main_surface, main_surface_w // 2, main_surface_h // 2 + 60, 150, 50, text="Settings"),
            Button(self.main_surface, main_surface_w // 2, main_surface_h - 100, 100, 50, text="Exit", font_size=25)]

    def __call__(self, mouse_pos, mouse_k):
        scene = "MENU"
        screen.blit(self.main_surface, (0, 0))

        for i in self.buttons:
            i.update(mouse_pos)

        if self.buttons[0].is_clicked(mouse_pos, mouse_k):
            scene = "GAME"

        if self.buttons[1].is_clicked(mouse_pos, mouse_k):
            scene = "SETTINGS"

        if self.buttons[2].is_clicked(mouse_pos, mouse_k):
            scene = "EXIT"

        return scene
