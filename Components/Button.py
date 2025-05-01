import pygame


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        text,
        position,
        font_size=24,
        color=(255, 255, 255),
        bg_color=(0, 0, 0),
        button_action=None,
    ):
        super().__init__()
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=position)
        self.original_image = self.image.copy()
        self.original_rect = self.rect.copy()
        self.button_action = button_action

    def perform_action(self):
        if self.button_action:
            self.button_action()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.image = self.font.render(self.text, True, (255, 0, 0))
            if pygame.mouse.get_pressed()[0]:
                self.perform_action()
        else:
            self.image = self.original_image.copy()
