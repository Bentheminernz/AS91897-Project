import pygame

class ListItem(pygame.sprite.Sprite):
    def __init__(self, text, position, font_size=24, color=(255, 255, 255), bg_color=(0, 0, 0)):
        super().__init__()
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=position)
        self.original_image = self.image.copy()
        self.original_rect = self.rect.copy()
        self.corner_radius = 10

    