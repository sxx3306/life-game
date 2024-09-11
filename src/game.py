import pygame
import numpy as np


class Button(pygame.sprite.Sprite):
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

    def handle_click(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            self.on_click()

    def on_click(self) -> bool:
        if self.start: 
            self.start = False
            self.image.fill('GREEN')
        else:
            self.start = True
            self.image.fill('RED')
            
        return True

    def blit(self, screen) -> None:
        screen.blit(self.image, self.rect)


class Game:
    def __init__(self, grid: tuple[int, int], resolution: tuple[float, float] = (800.0, 600.0), rules: list[list] = [[2, 3], [3]]):
        pygame.init()
        pygame.font.init()

        self.res = resolution
        self.grid = np.zeros(grid, dtype=int)
        self.rules = rules

        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()

        self.start_button = Button('GREEN', 100, 20, (self.res[0] - 150, 50))
        self.running = False

        # Padding values
        self.padding_top = 50
        self.padding_left = 50
        self.padding_bottom = 50
        self.padding_right = 200

        # Calculate the available space for the grid after applying padding
        self.grid_res = [self.res[0] - self.padding_left - self.padding_right, self.res[1] - self.padding_top - self.padding_bottom]

    def clear_board(self):
        clear_grid = np.zeros_like(self.grid)
        self.grid = clear_grid
        
    def check(self, index: list[int, int]) -> int:
        count = 0
        rows, cols = len(self.grid), len(self.grid[0])

        for i in range(index[0] - 1, index[0] + 2):
            for j in range(index[1] - 1, index[1] + 2):
                if (i == index[0] and j == index[1]) or i < 0 or i >= rows or j < 0 or j >= cols:
                    continue
                count += self.grid[i][j]

        return count

    def update_grid(self) -> np.ndarray:
        rows, cols = len(self.grid), len(self.grid[0])
        new_grid = np.copy(self.grid)

        for row in range(rows):
            for col in range(cols):
                neighbors = self.check([row, col])

                if self.grid[row][col] == 1 and neighbors not in self.rules[0]:
                    new_grid[row][col] = 0
                elif self.grid[row][col] == 0 and neighbors in self.rules[1]:
                    new_grid[row][col] = 1

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
                        row, col = int((pos[1] - self.padding_top) / (self.grid_res[1] / len(self.grid[0]))), int((pos[0] - self.padding_left) / (self.grid_res[0] / len(self.grid)))
                        
                        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                            self.grid[row][col] = 1 - self.grid[row][col]

            self.screen.fill('#ffceb4')

            # Draw grid lines with padding
            for i in range(0, len(self.grid) + 1):
                # Horizontal lines
                pygame.draw.line(self.screen, 'black', 
                                 (self.padding_left, self.padding_top + i * (self.grid_res[1] / len(self.grid))),
                                 (self.res[0] - self.padding_right, self.padding_top + i * (self.grid_res[1] / len(self.grid))))

                # Vertical lines
                pygame.draw.line(self.screen, 'black', 
                                 (self.padding_left + i * (self.grid_res[0] / len(self.grid[0])), self.padding_top),
                                 (self.padding_left + i * (self.grid_res[0] / len(self.grid[0])), self.res[1] - self.padding_bottom))

            width, height = self.grid_res[0] / len(self.grid[0]), self.grid_res[1] / len(self.grid)

            if self.running:
                self.update_grid()

            # Draw cells with padding
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] == 1:
                        rect_x = self.padding_left + col * width
                        rect_y = self.padding_top + row * height
                        pygame.draw.rect(self.screen, 'black', pygame.Rect(rect_x, rect_y, width + 1, height + 1))

            self.start_button.blit(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game((30, 30))
    game.run()
