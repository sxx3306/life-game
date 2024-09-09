import pygame
import numpy as np


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color: tuple, width: float, height: float, position: tuple):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.color = color
        self.width = width
        self.height = height
        self.start = False

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            self.on_click()

    def on_click(self):
        if self.start: 
            self.start = False
            self.image.fill('GREEN')
            self.image.set_alpha(255)
        else:
            self.start = True
            self.image.set_alpha(0)
        return True

    def blit(self, screen):
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self, grid: tuple[int, int], resolution: tuple[float, float] = (800.0, 600.0), cell_size: int = 10):
        pygame.init()

        self.res = resolution
        self.grid = np.zeros(grid, dtype=int)
        self.rules = [[2, 3], [3]]  # Survival: 2, 3. Birth: 3.

        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()

        self.start_button = Sprite('GREEN', self.res[0] / len(self.grid) * 2, self.res[0], (self.res[0] / len(self.grid) * (len(self.grid) - 2), 0))
        self.running = False

    def check(self, index: list[int, int]):
        count = 0
        rows, cols = len(self.grid), len(self.grid[0])

        for i in range(index[0] - 1, index[0] + 2):
            for j in range(index[1] - 1, index[1] + 2):
                if (i == index[0] and j == index[1]) or i < 0 or i >= rows or j < 0 or j >= cols:
                    continue
                count += self.grid[i][j]

        return count

    def update_grid(self):
        rows, cols = len(self.grid), len(self.grid[0])
        new_grid = np.copy(self.grid)  # Create a copy of the grid to store updates.

        for row in range(rows):
            for col in range(cols):
                neighbors = self.check([row, col])

                if self.grid[row][col] == 1 and neighbors not in self.rules[0]:
                    new_grid[row][col] = 0  # Клетка умирает
                elif self.grid[row][col] == 0 and neighbors in self.rules[1]:
                    new_grid[row][col] = 1  # Клетка рождается

        self.grid = new_grid

    def run(self):
        while True:
            self.running = self.start_button.start

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.start_button.handle_click(event):
                        pass
                    else:
                        pos = event.pos
                        row, col = int(pos[1] / (self.res[1] / len(self.grid[0]))), int(pos[0] / (self.res[0] / len(self.grid)))

                        if self.grid[row][col] == 1:
                            self.grid[row][col] = 0
                        else:
                            self.grid[row][col] = 1

            self.screen.fill('black')

            for i in range(1, len(self.grid)):
                pygame.draw.line(self.screen, 'white', (i * (self.res[0] / len(self.grid)), 0), (i * (self.res[0] / len(self.grid)), self.res[1]))
                pygame.draw.line(self.screen, 'white', (0, i * (self.res[1] / len(self.grid))), (self.res[0], i * (self.res[1] / len(self.grid))))

            width, height = self.res[0] / len(self.grid), self.res[1] / len(self.grid[0])

            if self.running:
                self.update_grid()

            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] == 1:
                        rect_x = col * width
                        rect_y = row * height
                        pygame.draw.rect(self.screen, 'white', pygame.Rect(rect_x, rect_y, width, height))

            self.start_button.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game((30, 30))
    game.run()
