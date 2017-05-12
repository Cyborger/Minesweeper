import ZedLib
import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.covered_image = ZedLib.LoadImage("Resources/Cell.png")
        self.uncovered_image = ZedLib.LoadImage("Resources/EmptyCell.png")
        self.image = self.covered_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x * self.rect.width
        self.rect.y = y * self.rect.height
        self.uncovered = False
        self.flagged = False

    def CheckClick(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.uncovered:
                self.Reveal()
                return True
        return False

    def Reveal(self):
        self.image = self.uncovered_image.copy()
        self.uncovered = True
        print("cell revealed")

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

    def GetCellIndex(self, grid):
        for row in grid:
            for cell in row:
                if cell == self:
                    return row.index(cell)

    def GetCellRowNumber(self, grid):
        for row in grid:
            for cell in row:
                if cell == self:
                    return grid.index(row)

    def UncoverNearby(self, grid):
        current_row = self.GetCellRowNumber(grid)
        current_index = self.GetCellIndex(grid)
        right = grid[current_row][min(current_index+1, len(grid[current_row]) - 1)]
        left = grid[current_row][max(current_index-1, 0)]
        above = grid[min(current_row+1, len(grid) - 1)][current_index]
        below = grid[max(current_row-1, 0)][current_index]
        nearby = [right, left, above, below]
        for cell in nearby:
            if (not cell.uncovered and not isinstance(cell, MineCell)
                    and not isinstance(cell, NumberCell)):
                cell.Reveal()
                cell.UncoverNearby(grid)


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
