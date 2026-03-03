import pygame
import math


class Cannon:
    def __init__(self, x, y, length=60):
        self.x = x
        self.y = y
        self.length = length

        self.angle = 90  # começa apontando para baixo

    def update(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos

        dx = mouse_x - self.x
        dy = mouse_y - self.y

        # só permite mirar para baixo
        if dy > 0:
            angle_rad = math.atan2(dy, dx)
            self.angle = math.degrees(angle_rad)

    def get_tip_position(self):
        angle_rad = math.radians(self.angle)

        tip_x = self.x + self.length * math.cos(angle_rad)
        tip_y = self.y + self.length * math.sin(angle_rad)  # <<< AQUI É +

        return tip_x, tip_y

    def draw(self, surface):
        angle_rad = math.radians(self.angle)

        end_x = self.x + self.length * math.cos(angle_rad)
        end_y = self.y + self.length * math.sin(angle_rad)  # <<< AQUI É +

        pygame.draw.line(
            surface,
            (200, 200, 200),
            (self.x, self.y),
            (end_x, end_y),
            6
        )

        pygame.draw.circle(surface, (100, 100, 100), (self.x, self.y), 12)