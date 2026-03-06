import pygame
from peg import Peg
from ball import Ball
from cannon import Cannon
import math


class Game:
    def __init__(self):
        pygame.init()

        self.START_BALLS = 15
        self.score = 0
        self.chances = self.START_BALLS
        self.game_over = False
        self.victory = False

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

        # Cria canhão
        self.cannon = Cannon(
            self.SCREEN_WIDTH // 2,
            self.offset_y - 40
        )

         # Cria Bola
        self.ball = Ball(
            self.SCREEN_WIDTH // 2,
            self.offset_y - 40
        )

        # Matriz de pegs
        self.ROWS = 12
        self.COLS = 12
        self.PEG_RADIUS = 12
        self.spacing = 40

        # Criar pegs
        self.pegs = []
        self.create_pegs()

        # reset da posição da bola sem gastar tentativa
        self.ball.x = self.cannon.x
        self.ball.y = self.cannon.y + 2
        self.ball.vel_x = 0
        self.ball.vel_y = 0
        self.ball.active = False

    # -----------------------------
    # Criar matriz de pegs
    # -----------------------------
    def create_pegs(self):

        matrix_width = (self.COLS * self.spacing) + (self.spacing // 2)

        start_x = self.offset_x + (self.GAME_WIDTH - matrix_width) // 2
        start_y = self.offset_y + 100

        for row in range(self.ROWS):
            for col in range(self.COLS):

                x = start_x + col * self.spacing
                y = start_y + row * self.spacing

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

        if self.game_over:

            self.screen.fill((0, 0, 0))

            font_big = pygame.font.SysFont(None, 80)
            font_small = pygame.font.SysFont(None, 40)

            game_over_text = font_big.render(
                "GAME OVER", True, (255, 50, 50)
            )
            score_text = font_small.render(
                f"Final Score: {self.score}", True, (255, 255, 255)
            )

            self.screen.blit(
                game_over_text,
                (self.SCREEN_WIDTH//2 - 170, self.SCREEN_HEIGHT//2 - 50)
            )

            self.screen.blit(
                score_text,
                (self.SCREEN_WIDTH//2 - 110, self.SCREEN_HEIGHT//2 + 40)
            )

            button_rect = pygame.Rect(
                self.SCREEN_WIDTH//2 - 100,
                self.SCREEN_HEIGHT//2 + 80,
                200,
                50
            )

            pygame.draw.rect(self.screen, (200, 200, 200), button_rect)

            font_button = pygame.font.SysFont(None, 40)
            button_text = font_button.render("Restart", True, (0, 0, 0))

            self.screen.blit(
                button_text,
                (self.SCREEN_WIDTH//2 - 50, self.SCREEN_HEIGHT//2 + 95)
            )

            self.restart_button = button_rect

            pygame.display.flip()
            return

        if self.victory:

            self.screen.fill((0, 0, 0))

            font_big = pygame.font.SysFont(None, 80)
            font_small = pygame.font.SysFont(None, 40)

            victory_text = font_big.render(
                "  YOU WON!", True, (255, 215, 0)
            )

            score_text = font_small.render(
                f"Final Score: {self.score}", True, (255, 255, 255)
            )

            self.screen.blit(
                victory_text,
                (self.SCREEN_WIDTH//2 - 160, self.SCREEN_HEIGHT//2 - 50)
            )

            self.screen.blit(
                score_text,
                (self.SCREEN_WIDTH//2 - 110, self.SCREEN_HEIGHT//2 + 40)
            )

            button_rect = pygame.Rect(
                self.SCREEN_WIDTH//2 - 100,
                self.SCREEN_HEIGHT//2 + 80,
                200,
                50
            )

            pygame.draw.rect(self.screen, (200, 200, 200), button_rect)

            font_button = pygame.font.SysFont(None, 40)
            button_text = font_button.render("Restart", True, (0, 0, 0))

            self.screen.blit(
                button_text,
                (self.SCREEN_WIDTH//2 - 50, self.SCREEN_HEIGHT//2 + 95)
            )

            self.restart_button = button_rect

            pygame.display.flip()
            return

        # JOGO NORMAL

        self.screen.fill((0, 0, 0))

        for peg in self.pegs:
            peg.draw(self.screen)

        self.cannon.draw(self.screen)
        self.ball.draw(self.screen)

        font = pygame.font.SysFont(None, 36)

        score_text = font.render(
            f"Score: {self.score}", True, (255, 255, 255)
        )

        self.screen.blit(
            score_text,
            (self.cannon.x + 80, self.cannon.y + 10)
        )

        chances_text = font.render(
            f"Balls: {self.chances}", True, (255, 255, 255)
        )

        self.screen.blit(
            chances_text,
            (self.cannon.x + 80, self.cannon.y + 40)
        )

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

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_pos = pygame.mouse.get_pos()

                    if self.game_over or self.victory:
                        if hasattr(self, "restart_button") and self.restart_button.collidepoint(mouse_pos):
                            self.restart_game()

                    else:

                        if not self.ball.active:

                            tip_x, tip_y = self.cannon.get_tip_position()

                            self.ball.x = tip_x
                            self.ball.y = tip_y

                            self.ball.launch(self.cannon.angle, 7)

            self.update()
            self.draw()

        pygame.quit()

    # -----------------------------
    # Colisões
    # -----------------------------
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

                nx = dx / dist
                ny = dy / dist

                dot = self.ball.vel_x * nx + self.ball.vel_y * ny

                gained = peg.hit()
                self.score += gained

                self.check_victory()

                self.ball.vel_x -= 2 * dot * nx
                self.ball.vel_y -= 2 * dot * ny

                overlap = (self.ball.radius + peg.radius) - dist
                self.ball.x += nx * overlap
                self.ball.y += ny * overlap

    # -----------------------------
    # Checar vitória
    # -----------------------------
    def check_victory(self):

        for peg in self.pegs:
            if peg.bonus and peg.active:
                return

        self.victory = True

    # -----------------------------
    # Limites da tela
    # -----------------------------
    def check_bounds(self):

        if self.ball.x - self.ball.radius <= 0:
            self.ball.x = self.ball.radius
            self.ball.vel_x *= -1

        if self.ball.x + self.ball.radius >= self.SCREEN_WIDTH:
            self.ball.x = self.SCREEN_WIDTH - self.ball.radius
            self.ball.vel_x *= -1

        if self.ball.y - self.ball.radius <= 0:
            self.ball.y = self.ball.radius
            self.ball.vel_y *= -1

        if self.ball.y - self.ball.radius > self.SCREEN_HEIGHT:
            self.reset_ball()

    # -----------------------------
    # Reset bola
    # -----------------------------
    def reset_ball(self):

        self.ball.x = self.cannon.x
        self.ball.y = self.cannon.y + 2

        self.ball.vel_x = 0
        self.ball.vel_y = 0
        self.ball.active = False

        self.chances -= 1

        if self.chances <= 0:
            self.game_over = True

    # -----------------------------
    # Restart jogo
    # -----------------------------
    def restart_game(self):

        self.score = 0
        self.chances = self.START_BALLS
        self.game_over = False
        self.victory = False

        self.pegs = []
        self.create_pegs()

        self.ball.x = self.cannon.x
        self.ball.y = self.cannon.y + 2
        self.ball.vel_x = 0
        self.ball.vel_y = 0
        self.ball.active = False


if __name__ == "__main__":
    game = Game()
    game.run()