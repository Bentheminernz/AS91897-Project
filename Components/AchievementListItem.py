import pygame


# this is a custom achievement list item class, it is used to create the achievement list items in the achievement menu
# it inherits from the pygame sprite class, so it can be used in sprite groups
class AchievementListItem(pygame.sprite.Sprite):
    def __init__(
        self,
        achievement,
        position,
        font_size=24,
        color=(255, 255, 255),
        bg_color=(0, 0, 0),
        border_radius=10,
    ):
        # initialize the parent class
        super().__init__()
        self.font = pygame.font.Font(None, font_size)
        self.desc_font = pygame.font.Font(None, int(font_size / 1.5))
        self.achievement = achievement
        self.achievement_title = achievement["name"]
        self.achievement_description = achievement["description"]
        self.color = color
        self.bg_color = bg_color
        self.border_radius = border_radius

        # load the corresponding trophy image
        self.img_path = f"Assets/AchievementImgs/{achievement['trophy']}.png"
        trophy_img = pygame.image.load(self.img_path).convert_alpha()
        img_size = int(font_size * 2)
        self.trophy_img = pygame.transform.scale(trophy_img, (img_size, img_size))

        # create the surface for the achievement item
        title_text_surface = self.font.render(self.achievement_title, True, self.color)
        description_text_surface = self.desc_font.render(
            self.achievement_description, True, self.color
        )

        # calculate the size of the item based on the text and image
        text_width = max(
            title_text_surface.get_width(), description_text_surface.get_width()
        )
        text_height = (
            title_text_surface.get_height() + description_text_surface.get_height() + 5
        )

        total_width = self.trophy_img.get_width() + text_width + 20
        total_height = max(text_height, self.trophy_img.get_height()) + 20

        # create the surface and draw the background
        self.image = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image,
            self.bg_color,
            self.image.get_rect(),
            border_radius=self.border_radius,
        )

        img_x = 10
        img_y = (total_height - self.trophy_img.get_height()) // 2

        # calculate the position for the text
        text_x = img_x + self.trophy_img.get_width() + 10
        title_y = (total_height - text_height) // 2
        desc_y = title_y + title_text_surface.get_height() + 5

        # display the trophy image and text on the surface
        self.image.blit(self.trophy_img, (img_x, img_y))
        self.image.blit(title_text_surface, (text_x, title_y))
        self.image.blit(description_text_surface, (text_x, desc_y))

        self.rect = self.image.get_rect(center=position)
