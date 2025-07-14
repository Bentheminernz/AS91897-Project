import pygame
from Utils.loggerConfig import component_logger


# this is a custom text field class that is used to create text fields in the game
# it inherits from the pygame sprite class, so it can be used in sprite groups
# it has a font, initial text, label text, position, max length and padding
class TextField(pygame.sprite.Sprite):
    # initialises the text field and sets its variables
    # it also creates the image and rect for the text field
    def __init__(
        self,
        font,
        initial_text="",
        label_text="",
        position=(0, 0),
        max_length=20,
        padding=5,
    ):
        super().__init__()
        self.font = font
        self.text = initial_text if initial_text else ""
        self.label_text = label_text
        self.max_length = max_length
        self.padding = padding
        self.text_color = (255, 255, 255)
        self.border_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        self.border_width = 2

        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.label_surface = (
            self.font.render(self.label_text, True, self.text_color)
            if label_text
            else None
        )

        self.image = pygame.Surface(
            (
                self.text_surface.get_width() + 2 * self.padding,
                self.text_surface.get_height() + 2 * self.padding,
            )
        )

        self.rect = self.image.get_rect(topleft=position)
        self.active = False
        self.update()

    # this function is called every frame to update the text field
    # it checks if the text field is active, and if so, it updates the text field
    def update(self):
        text_surface = self.font.render(
            self.text if self.text else " ", True, self.text_color
        )
        label_surface = (
            self.font.render(self.label_text, True, self.text_color)
            if self.label_text
            else None
        )

        text_width = text_surface.get_width() + 2 * self.padding
        label_width = (
            label_surface.get_width() + 2 * self.padding if label_surface else 0
        )
        width = max(200, text_width, label_width)

        height = text_surface.get_height() + 2 * self.padding

        total_height = height
        label_offset = 0
        if label_surface:
            label_offset = label_surface.get_height() + 5
            total_height += label_offset

        self.image = pygame.Surface((width, total_height))
        self.image.fill(self.bg_color)

        self.input_rect = pygame.Rect(0, label_offset, width, height)

        pygame.draw.rect(
            self.image, self.border_color, self.input_rect, self.border_width
        )

        self.image.blit(text_surface, (self.padding, label_offset + self.padding))

        if label_surface:
            self.image.blit(label_surface, (self.padding, 0))

        if self.active:
            pygame.draw.rect(
                self.image, (100, 200, 255), self.input_rect, self.border_width
            )

    # this function is called when the text field is clicked
    # it checks if the text field is active, and if so, it updates the text field
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)

            if self.input_rect.collidepoint(local_pos):
                self.active = not self.active
            else:
                self.active = False

        # handles key events for the text field
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                component_logger.info(f"Text entered: {self.text}")
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length:
                self.text += event.unicode

            self.update()

    def return_text(self):
        return self.text
