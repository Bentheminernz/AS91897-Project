import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        # creates the player
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 350
        self.gravity_force = 0

    # this is the function that updates the players movement
    def update(self, delta_time, screen):
        keys = pygame.key.get_pressed()
        movement = self.speed * delta_time

        # handles player movement
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_SPACE]:
            if screen.get_height() - self.rect.bottom < 10:
                direction.y -= 0.75
                self.gravity_force = -self.speed * 0.75

        # normalises the players movement so diagonal movement is not faster
        if direction.length() > 0:
            direction.normalize_ip()

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
        gravity_constant = 500

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