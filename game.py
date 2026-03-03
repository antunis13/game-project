import pygame
from peg import Peg
from ball import Ball
from cannon import Cannon
import math


class Game:
    def __init__(self):
        pygame.init()

        self.score = 0

        # Tela
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 900
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Mini Peggle")

        self.clock = pygame.time.Clock()
        self.running = True

        # Área central
        self.GAME_WIDTH = 600
        self.GAME_HEIGHT = 700

        self.offset_x = (self.SCREEN_WIDTH - self.GAME_WIDTH) // 2
        self.offset_y = (self.SCREEN_HEIGHT - self.GAME_HEIGHT) // 2

        # Matriz
        self.ROWS = 12
        self.COLS = 12
        self.PEG_RADIUS = 12
        self.spacing = 40

        self.pegs = []
        self.create_pegs()

        # Bola (começa parada no topo da área)
        self.ball = Ball(
            self.SCREEN_WIDTH // 2,
            self.offset_y + 40
        )

        self.cannon = Cannon(
        self.SCREEN_WIDTH // 2,
        self.offset_y + 40
)


    # -----------------------------
    # Criação dos pegs
    # -----------------------------
    def create_pegs(self):
        matrix_width = (self.COLS * self.spacing) + (self.spacing // 2)
        start_x = self.offset_x + (self.GAME_WIDTH - matrix_width) // 2
        start_y = self.offset_y + 100

        for row in range(self.ROWS):
            for col in range(self.COLS):

                x = start_x + col * self.spacing
                y = start_y + row * self.spacing

                # Alternância horizontal
                if row % 2 == 1:
                    x += self.spacing // 2

                self.pegs.append(Peg(x, y, self.PEG_RADIUS))

    # -----------------------------
    # Atualização
    # -----------------------------
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.cannon.update(mouse_pos)

        self.ball.update()

        if self.ball.active:
            self.check_collisions()
            self.check_bounds()


    # -----------------------------
    # Desenho
    # -----------------------------
    def draw(self):
        self.screen.fill((0, 0, 0))

        # Desenhar pegs
        for peg in self.pegs:
            peg.draw(self.screen)


        self.cannon.draw(self.screen)
        # Desenhar bola
        self.ball.draw(self.screen)

        font = pygame.font.SysFont(None, 36)

        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.cannon.x + 80, self.cannon.y - 20))

        pygame.display.flip()


    # -----------------------------
    # Loop principal
    # -----------------------------
    def run(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Clique para lançar
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.ball.active:
                        tip_x, tip_y = self.cannon.get_tip_position()
                        self.ball.x = tip_x
                        self.ball.y = tip_y
                        self.ball.launch(self.cannon.angle, 10)

            self.update()
            self.draw()

        pygame.quit()
    
    def check_collisions(self):
        for peg in self.pegs:
            if not peg.active:
                continue

            dx = self.ball.x - peg.x
            dy = self.ball.y - peg.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < self.ball.radius + peg.radius:

                if dist == 0:
                    dist = 0.01

                # Normal da colisão
                nx = dx / dist
                ny = dy / dist

                # Produto escalar
                dot = self.ball.vel_x * nx + self.ball.vel_y * ny

                gained = peg.hit()
                self.score += gained    # soma no total

                # Reflexão
                self.ball.vel_x -= 2 * dot * nx
                self.ball.vel_y -= 2 * dot * ny

                # Pequeno empurrão para fora do peg
                overlap = (self.ball.radius + peg.radius) - dist
                self.ball.x += nx * overlap
                self.ball.y += ny * overlap

                peg.hit()

    def check_bounds(self):

        # parede esquerda
        if self.ball.x - self.ball.radius <= 0:
            self.ball.x = self.ball.radius
            self.ball.vel_x *= -1

        # parede direita
        if self.ball.x + self.ball.radius >= self.SCREEN_WIDTH:
            self.ball.x = self.SCREEN_WIDTH - self.ball.radius
            self.ball.vel_x *= -1

        # teto
        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = self.ball.radius
            self.ball.vel_y *= -1

        # saiu por baixo
        if self.ball.y - self.ball.radius > self.SCREEN_HEIGHT:
            self.reset_ball()

    def reset_ball(self):
        tip_x, tip_y = self.cannon.get_tip_position()

        self.ball.x = self.cannon.x
        self.ball.y = self.cannon.y
        self.ball.vel_x = 0
        self.ball.vel_y = 0
        self.ball.active = False    

if __name__ == "__main__":
    game = Game()
    game.run()