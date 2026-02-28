import pygame
import random


class Peg:
    def __init__(self, x, y, radius=12):
        self.x = x
        self.y = y
        self.radius = radius
        self.points = random.randint(10, 50)
        self.bonus = random.random() < 0.15
        self.active = True

        if self.bonus:
            self.points *= 2

    def draw(self, surface):
        if not self.active:
            return

        border_thickness = 3

        if self.bonus:
            fill_color = (255, 165, 0)
            border_color = (255, 255, 255)
        else:
            fill_color = (0, 0, 255)
            border_color = (255, 255, 255)

        
        pygame.draw.circle(
            surface,
            border_color,
            (self.x, self.y),
            self.radius
        )

        
        pygame.draw.circle(
            surface,
            fill_color,
            (self.x, self.y),
            self.radius - border_thickness
        )