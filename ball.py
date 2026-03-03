import pygame


class Ball:
    def __init__(self, x, y, radius=8):
        self.x = x
        self.y = y
        self.radius = radius

        self.vel_x = 0
        self.vel_y = 0

        self.gravity = 0.4
        self.active = False  # só começa a cair quando lançada

    def launch(self, angle_deg, power):
        import math

        angle = math.radians(angle_deg)

        self.vel_x = power * math.cos(angle)
        self.vel_y = -power * math.sin(angle)

        self.active = True

    def update(self):
        if not self.active:
            return

        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (100, 200, 255),
            (int(self.x), int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            surface,
            (255, 255, 255),
            (int(self.x), int(self.y)),
            self.radius,
            2
        )