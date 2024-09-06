import pygame
import numpy as np

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color: str, width: float, height: float):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

class Game():
    """

    

    """
    def __init__(self, grid: tuple[int, int], resolution: tuple[float, float] = (800.0, 600.0)):
        pygame.init()

        self.res = resolution
        self.grid = np.zeros(grid, dtype=int)

        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()

        self.start_button = Sprite('GREEN', self.res[0] / 6, self.res[1] / 6)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = event.pos