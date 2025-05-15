import pygame
from Utils import PlayerDataContext

# this is a custom button class that is used to create buttons in the game
# it inherits from the pygame sprite class, so it can be used in sprite groups
# it has a text, position, font size, color, background color and a button action
class Button(pygame.sprite.Sprite):
    # initialises the button and sets its variables
    # it also creates the image and rect for the button
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
        self.is_pressed = False
        self.sound_enabled = PlayerDataContext.is_sound_enabled()
        self.button_sound = pygame.mixer.Sound("Assets/Audio/SelectSound.wav")
        self.button_sound.set_volume(1.0 if self.sound_enabled else 0.0)

    # this function is called when the button is clicked
    # it checks if a button action is present, and if so, it calls it
    def perform_action(self):
        if self.button_action:
            self.button_action()

    # this function is called every frame to update the button
    # it checks if the mouse is over the button and handles hover/press states
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        if self.rect.collidepoint(mouse_pos):
            self.image = self.font.render(self.text, True, (255, 0, 0))
            
            if mouse_pressed:
                self.is_pressed = True
            elif self.is_pressed:
                self.perform_action()
                self.is_pressed = False
        else:
            self.image = self.original_image.copy()
            if not mouse_pressed:
                self.is_pressed = False
                
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.is_pressed:
                self.perform_action()
                self.button_sound.play()
                self.is_pressed = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True