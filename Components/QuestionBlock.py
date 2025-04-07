import pygame

class QuestionBlock(pygame.sprite.Sprite):
    def __init__(self, image_path, position, text):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=position)
        self.text = str(text)


    def update(self, *args):
        # draw the question block
        screen = args[0]
        screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 100)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        print(f"Renderinf  text: {self.text}")

    def on_collision(self, player):
        # this detects if the player collides with the question block
        if self.rect.colliderect(player.rect):
            print("Collision detected!")
            self.kill()