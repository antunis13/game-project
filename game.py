import pygame
from peg import Peg
from ball import Ball
from cannon import Cannon


class Game:
    def __init__(self):
        pygame.init()

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


if __name__ == "__main__":
    game = Game()
    game.run()