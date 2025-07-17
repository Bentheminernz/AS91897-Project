import pygame
from Utils.loggerConfig import component_logger
from Utils import PlayerDataContext


# this is a custom question block class that is used to create question blocks in the game
# it inherits from the pygame sprite class, so it can be used in sprite groups
# it has an image, a position, a text, a color, a background color and a button action
class QuestionBlock(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        text,
        is_correct,
        player_data,
        on_correct_answer,
        question_id,
        topic_id,
        max_questions,
    ):
        super().__init__()
        width, height = 280, 120
        border_thickness = 8
        self.text = str(text)
        self.is_killed = False
        self.is_correct = is_correct
        self.player_data = player_data
        self.on_correct_answer = on_correct_answer
        self.question_id = question_id
        self.topic_id = topic_id
        self.max_questions = max_questions
        self.correct_audio = pygame.mixer.Sound("./Assets/Audio/Correct.wav")
        self.incorrect_audio = pygame.mixer.Sound("./Assets/Audio/Incorrect.wav")
        self.audio_volume = 1.0 if PlayerDataContext.is_sound_enabled() else 0.0
        self.correct_audio.set_volume(self.audio_volume)
        self.incorrect_audio.set_volume(self.audio_volume)

        # creates the surface
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 90))
        pygame.draw.rect(
            self.image,
            (255, 255, 255),
            self.image.get_rect(),
            border_thickness,
            border_radius=12,
        )

        # prepare the font and wrap the text
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)
        max_text_width = width - 2 * (border_thickness + 16)
        wrapped_lines = self.wrap_text(self.text, font, max_text_width)

        # render the wrapped text in the horizontal and vertical center of the block
        total_text_height = len(wrapped_lines) * font.get_linesize()
        y_offset = (height - total_text_height) // 2
        for line in wrapped_lines:
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(centerx=width // 2, y=y_offset)
            self.image.blit(text_surface, text_rect)
            y_offset += font.get_linesize()

        self.rect = self.image.get_rect(topleft=position)

    def wrap_text(self, text, font, max_width):
        """wraps the text to fit within the specified max width"""
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    # this function is called upon every frame to check for collisions
    # if the player is colliding with the question block, it kills the block
    # and adds the score to the player data, if the answer is correct
    def on_collision(self, player):
        if self.rect.colliderect(player.rect) and not self.is_killed:
            component_logger.info(f"Player collided with question block: {self.text}")
            component_logger.info(f"The answer was {self.is_correct}")
            
            if self.is_correct:
                component_logger.info("Correct answer!")
                self._update_scores()
                self._check_achievements()
                self.correct_audio.play()
                
                if self.on_correct_answer:
                    self.on_correct_answer()
            else:
                component_logger.info("Incorrect answer!")
                self.incorrect_audio.play()

            self.is_killed = True
            self.kill()

    def _update_scores(self):
        score_entries = self.player_data.get("score", [])
        for score_entry in score_entries:
            if score_entry.get("topic") == self.topic_id:
                score_entry["score"] += 1
                break

        high_scores = self.player_data.get("high_scores", [])
        for high_score in high_scores:
            if high_score.get("topic") == self.topic_id:
                high_score["score"] = min(high_score["score"] + 1, self.max_questions)
                break
        else:
            high_scores.append({"topic": self.topic_id, "score": 1})

        self.player_data["high_scores"] = high_scores

    def _check_achievements(self):
        """Check and grant achievements based on current scores"""
        achievements = self.player_data.get("achievements", [])
        
        if 1 not in achievements:
            component_logger.info("Granting achievement 1 for answering a question")
            PlayerDataContext.achievement_granter(1)

        total_score = sum(entry.get("score", 0) for entry in self.player_data.get("score", []))

        if 2 not in achievements and total_score >= 10:
            component_logger.info(f"Granting achievement 2 for answering 10 questions (total: {total_score})")
            PlayerDataContext.achievement_granter(2)

        if 3 not in achievements and total_score >= 20:
            component_logger.info(f"Granting achievement 3 for answering 20 questions (total: {total_score})")
            PlayerDataContext.achievement_granter(3)
