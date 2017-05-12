import ZedLib
import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        self.covered_image = ZedLib.LoadImage("Resources/Cell.png")
        self.uncovered_image = ZedLib.LoadImage("Resources/EmptyCell.png")
        self.image = self.covered_image.copy()
        self.rect = self.image.get_rect()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.uncovered = False
        self.flagged = False

    def SetPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def CheckClick(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.uncovered:
                self.Reveal()
                return True
        return False

    def Reveal(self):
        self.image = self.uncovered_image.copy()
        self.uncovered = True

    def CheckFlag(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.flagged and not self.uncovered:
                self.Flag()
            elif self.flagged and not self.uncovered:
                self.UnFlag()

    def Flag(self):
        pass

    def UnFlag(self):
        pass


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
