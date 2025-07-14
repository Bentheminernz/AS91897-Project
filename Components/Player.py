import pygame
from Utils import PlayerDataContext


# this is the player class, it inherits from the pygame sprite class, so it can be used in sprite groups
# it has an image, a rect, a speed and a gravity force
# it also has a function to update the players movement and a function to handle the players gravity
class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        # creates the player
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 350
        self.gravity_force = 0
        self.jump_audio = pygame.mixer.Sound("./Assets/Audio/Jump.ogg")
        self.jump_audio.set_volume(1.0 if PlayerDataContext.is_sound_enabled() else 0.0)

    # this is the function that updates the players movement
    def update(self, *args):
        screen = args[0]
        delta_time = args[1]

        keys = pygame.key.get_pressed()
        movement = self.speed * delta_time
        is_jump = False

        # handles player movement
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1
        if (
            (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w])
            and not is_jump
            and self.rect.bottom >= screen.get_height()
        ):
            is_jump = True
            direction.y -= 1.0
            self.gravity_force = -self.speed
            self.jump_audio.play()

        # normalises the players movement so diagonal movement is not faster
        if direction.length() > 0:
            direction.normalize_ip()

        if self.rect.bottom >= screen.get_height():
            is_jump = False

        # updates the players position
        self.rect.x += direction.x * movement
        self.rect.y += direction.y * movement

        # this makes sure the player cant leave the boundaries of the window
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()

        # draw the player
        screen.blit(self.image, self.rect)

    # this function handles the players gravity
    def gravity(self, delta_time, screen):
        gravity_constant = 750

        # this increases the gravity force over time, multiplied by delta_time (delta time is just time since last frame, so it behaves nicely on all different frame rates (this is so i dont forget))
        self.gravity_force += gravity_constant * delta_time

        # actually update the players position
        self.rect.y += self.gravity_force * delta_time

        # player can't fall off the screen
        if self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
            self.gravity_force = 0

        # they also can't go above the screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.gravity_force = 0
