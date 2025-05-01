import pygame

# this is a custom question block class that is used to create question blocks in the game
# it inherits from the pygame sprite class, so it can be used in sprite groups
# it has an image, a position, a text, a color, a background color and a button action
class QuestionBlock(pygame.sprite.Sprite):
    # initialises the question block and sets its variables
    def __init__(
        self, image_path, position, text, is_correct, player_data, on_correct_answer, question_id
    ):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.text = str(text)
        self.is_killed = False
        self.is_correct = is_correct
        self.player_data = player_data
        self.on_correct_answer = on_correct_answer
        self.question_id = question_id

        self.image = self.original_image.copy()
        font = pygame.font.Font(None, 18)
        text_color = (0, 255, 0) if is_correct else (255, 255, 255)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(50, 50))
        self.image.blit(text_surface, text_rect)
        self.rect = self.image.get_rect(topleft=position)

    # this function is called upon every frame to check for collisions
    # if the player is colliding with the question block, it kills the block
    # and adds the score to the player data, if the answer is correct
    def on_collision(self, player):
        if self.rect.colliderect(player.rect) and not self.is_killed:
            print("Collision detected!")
            print(f"The answer was {self.is_correct}")
            if self.is_correct:
                print("Correct answer!")
                self.player_data["score"] += 1

                if self.on_correct_answer:
                    self.on_correct_answer()

            self.is_killed = True
            self.kill()
