import pygame
import math


class Cannon:
    def __init__(self, x, y, length=60):
        self.x = x
        self.y = y
        self.length = length

        self.angle = 0  # em graus

        # Limite de rotação (meia lua)
        self.min_angle = -90
        self.max_angle = 90

    # -------------------------
    # Atualiza ângulo baseado no mouse
    # -------------------------
    def update(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos

        dx = mouse_x - self.x
        dy = mouse_y - self.y

        angle_rad = math.atan2(-dy, dx)
        angle_deg = math.degrees(angle_rad)

        # Limitar rotação
        self.angle = max(self.min_angle, min(self.max_angle, angle_deg))

    # -------------------------
    # Retorna ponta do canhão
    # -------------------------
    def get_tip_position(self):
        angle_rad = math.radians(self.angle)

        tip_x = self.x + self.length * math.cos(angle_rad)
        tip_y = self.y - self.length * math.sin(angle_rad)

        return tip_x, tip_y

    # -------------------------
    # Desenho
    # -------------------------
    def draw(self, surface):
        angle_rad = math.radians(self.angle)

        end_x = self.x + self.length * math.cos(angle_rad)
        end_y = self.y - self.length * math.sin(angle_rad)

        # corpo do canhão
        pygame.draw.line(
            surface,
            (200, 200, 200),
            (self.x, self.y),
            (end_x, end_y),
            6
        )

        # base
        pygame.draw.circle(surface, (100, 100, 100), (self.x, self.y), 12)