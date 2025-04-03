import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        # creates the player
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 350

    # this is the function that updates the players movement
    def update(self, delta_time, screen):
        keys = pygame.key.get_pressed()
        movement = self.speed * delta_time

        # handles player movement
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_DOWN]:
            direction.y += 1

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
