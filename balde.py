import pygame

class Balde:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 20

        self.speed = 4
        self.direction = 1

    def update(self, screen_width):

        self.x += self.speed * self.direction

        if self.x <= 0 or self.x + self.width >= screen_width:
            self.direction *= -1

    def draw(self, surface):

        pygame.draw.rect(
            surface,
            (255,255,255),
            (self.x, self.y, self.width, self.height)
        )