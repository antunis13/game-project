import pygame
from peg import Peg


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

        # Área central
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 700

        self.offset_x = (self.SCREEN_WIDTH - self.GAME_WIDTH) // 2
        self.offset_y = (self.SCREEN_HEIGHT - self.GAME_HEIGHT) // 2

        # Matriz
        self.ROWS = 8
        self.COLS = 8
        self.PEG_RADIUS = 12
        self.spacing = 80

        self.pegs = []
        self.create_pegs()

        self.clock = pygame.time.Clock()
        self.running = True

    def create_pegs(self):
        matrix_width = self.COLS * self.spacing

        start_x = self.offset_x + (self.GAME_WIDTH - matrix_width) // 2
        start_y = self.offset_y + 100

        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = start_x + col * self.spacing
                y = start_y + row * self.spacing

                if row % 2 == 1:
                    x += self.spacing // 2
                self.pegs.append(Peg(x, y, self.PEG_RADIUS))


    def draw(self):
        self.screen.fill((20, 20, 20))
       
        for peg in self.pegs:
            peg.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()