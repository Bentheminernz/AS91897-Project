import pygame
from Utils import PlayerDataContext


# this is a custom checkbox class that is used to create checkboxes in the game
# it inherits from the pygame sprite class, so it can be used in sprite groups
class Checkbox(pygame.sprite.Sprite):
    # initialises the checkbox and sets its variables
    def __init__(
        self,
        text,
        position,
        size=20,
        font_size=24,
        text_color=(255, 255, 255),
        border_color=(255, 255, 255),
        check_color=(0, 255, 0),
        bg_color=(0, 0, 0),
        initial_state=False,
        on_toggle=None,
    ):
        # initialize the parent class
        super().__init__()

        self.text = text
        self.position = position
        self.size = size

        self.font_size = font_size
        self.text_color = text_color
        self.border_color = border_color
        self.check_color = check_color

        self.bg_color = bg_color
        self.is_checked = initial_state

        self.on_toggle = on_toggle
        self.font = pygame.font.Font(None, font_size)
        self.sound_enabled = PlayerDataContext.is_sound_enabled()
        self.button_sound = pygame.mixer.Sound("Assets/Audio/SelectSound.wav")
        self.button_sound.set_volume(1.0 if self.sound_enabled else 0.0)

        # creates the initial image and rect for the checkbox
        self.update_image()
        self.is_pressed = False

    def update_image(self):
        # calculate the size of the checkbox and text
        text_surface = self.font.render(self.text, True, self.text_color)
        total_width = self.size + 10 + text_surface.get_width()
        total_height = max(self.size, text_surface.get_height())

        # creates the surface for the checkbox
        self.image = pygame.Surface((total_width, total_height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # draw time!
        pygame.draw.rect(
            self.image,
            self.border_color,
            (0, (total_height - self.size) // 2, self.size, self.size),
            2,
        )

        # if it is checked then draw the check mark
        if self.is_checked:
            pygame.draw.rect(
                self.image,
                self.check_color,
                (3, (total_height - self.size) // 2 + 3, self.size - 6, self.size - 6),
            )

        # draw the checkbox label text
        self.image.blit(
            text_surface,
            (self.size + 10, (total_height - text_surface.get_height()) // 2),
        )

        self.rect = self.image.get_rect(center=self.position)

    # toggles the checkbox state and calls the on_toggle callback if it exists
    def toggle(self):
        self.is_checked = not self.is_checked
        self.update_image()
        if self.on_toggle:
            self.on_toggle(self.is_checked)

    # updates the checkbox based on mouse events
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                self.is_pressed = True
            elif self.is_pressed:
                self.toggle()
                self.is_pressed = False
        elif not mouse_pressed:
            self.is_pressed = False

    # handles mouse events for the checkbox
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.is_pressed:
                self.toggle()
                self.is_pressed = False
                self.button_sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
