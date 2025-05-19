import pygame

class AchievementListItem(pygame.sprite.Sprite):
    def __init__(self, achievement, position, font_size=24, color=(255, 255, 255), bg_color=(0, 0, 0), border_radius=10):
        super().__init__()
        self.font = pygame.font.Font(None, font_size)
        self.desc_font = pygame.font.Font(None, int(font_size / 1.5))
        self.achievement = achievement
        self.achievement_title = achievement["name"]
        self.achievement_description = achievement["description"]
        self.color = color
        self.bg_color = bg_color
        self.border_radius = border_radius

        title_text_surface = self.font.render(self.achievement_title, True, self.color)
        description_text_surface = self.desc_font.render(self.achievement_description, True, self.color)

        self.image = pygame.Surface((max(title_text_surface.get_width(), description_text_surface.get_width()) + 10,
                                     title_text_surface.get_height() + description_text_surface.get_height() + 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.bg_color, self.image.get_rect(), border_radius=self.border_radius)

        self.image.blit(title_text_surface, (5, 5))
        self.image.blit(description_text_surface, (5, title_text_surface.get_height() + 10))
        self.rect = self.image.get_rect(center=position)