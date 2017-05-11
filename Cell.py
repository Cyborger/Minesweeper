import ZedLib
import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.covered_image = ZedLib.LoadImage("Resources/Cell.png")
        self.uncovered_image = None
        self.image = self.covered_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x * self.rect.width
        self.rect.y = y * self.rect.height


class MineCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.uncovered_image = ZedLib.LoadImage("Resources/Mine.png")


class NumberCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.number_of_nearby_mines = 0

    def Increment(self):
        self.num_of_nearby_mines += 1
        self.uncovered_image = self.GetNumberImage()

    def GetNumberImage(self):
        pass
