import pygame

class QuestionBlock(pygame.sprite.Sprite):
    def __init__(self, image_path, position, text):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.text = str(text)
        self.is_killed = False

        self.image = self.original_image.copy()
        font = pygame.font.Font(None, 18)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(50, 50))
        self.image.blit(text_surface, text_rect)
        
        self.rect = self.image.get_rect(topleft=position)

    def on_collision(self, player):
        # this detects if the player collides with the question block
        if self.rect.colliderect(player.rect) and not self.is_killed:
            print("Collision detected!")
            self.is_killed = True
            self.kill()