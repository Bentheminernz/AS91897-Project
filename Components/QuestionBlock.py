import pygame

class QuestionBlock(pygame.sprite.Sprite):
    def __init__(self, image_path, position, text):
        # creates the question block
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)
        self.text = text
        self.image = pygame.transform.scale(self.image, (200, 200))

    def update(self, screen):
        # draw the question block
        screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)