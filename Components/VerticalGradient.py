import pygame


class VerticalGradient:
    # initializes the vertical gradient with two colors and dimensions
    def __init__(self, color1, color2, width, height):
        self.color1 = color1
        self.color2 = color2
        self.width = width

        self.height = height

        self.gradient_surface = pygame.Surface((width, height))
        self.create_gradient()

    # creates the vertical gradient by interpolating between the two colors
    # it draws horizontal lines from the top to the bottom of the surface
    def create_gradient(self):
        for y in range(self.height):
            ratio = y / self.height
            r = int(self.color1[0] * (1 - ratio) + self.color2[0] * ratio)
            g = int(self.color1[1] * (1 - ratio) + self.color2[1] * ratio)
            b = int(self.color1[2] * (1 - ratio) + self.color2[2] * ratio)
            pygame.draw.line(self.gradient_surface, (r, g, b), (0, y), (self.width, y))
