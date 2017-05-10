import ZedLib
import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.covered_image = ZedLib.LoadImage("Resources/Cell.png")
        self.uncovered_image = None
        self.rect = self.covered_image.get_rect()

class MineCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.uncovered_image = ZedLib.LoadImage("Resources/Mine.png")

    def IncrementNearbyCells(self, cells):
        # Create a rect surrounding the mine with a size of 3 cells by 3 cells
        nearby_area = pygame.Rect(self.rect.x - self.rect.width,
                                  self.rect.y - self.rect.height,
                                  self.rect.width * 3,
                                  self.rect.height * 3)
        for cell in cells:
            if cell.rect.colliderect(nearby_area):
                cell.Increment()

class NumberCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.num_of_nearby_mines = 0
        one_nearby_mine = ZedLib.LoadImage("Resources/OneCell.png")
        self.possible_numbers = [one_nearby_cell]

    def Increment(self):
        self.num_of_nearby_mines += 1
        self.uncovered_image = self.GetNumberImage()

    def GetNumberImage(self):
        index_num = self.num_of_nearby_mines - 1
        self.uncovered_image = self.possible_numbers[index_num]
