import ZedLib
import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, grid_x, grid_y):
        self.covered_image = ZedLib.LoadImage("Resources/Cell.png")
        self.flagged_image = ZedLib.LoadImage("Resources/FlaggedCell.png")
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
                print("flaggin")
            elif self.flagged and not self.uncovered:
                print("unflagging")
                self.UnFlag()

    def UncoverNearby(self, cells):
        right = (self.grid_x + 1, self.grid_y)
        left = (self.grid_x - 1, self.grid_y)
        up = (self.grid_x, self.grid_y - 1)
        below = (self.grid_x, self.grid_y + 1)
        nearby = [right, left, up, below]
        for direction in nearby:
            for cell in cells:
                if cell.grid_x == direction[0] and cell.grid_y == direction[1]:
                    if not isinstance(cell, MineCell):
                        if not cell.uncovered:
                            cell.Reveal()
                            if isinstance(cell, EmptyCell):
                                cell.UncoverNearby(cells)

    def Flag(self):
        self.image = self.flagged_image.copy()
        self.flagged = True

    def UnFlag(self):
        self.image = self.covered_image.copy()
        self.flagged = False


class EmptyCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)


class MineCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.uncovered_image = ZedLib.LoadImage("Resources/Mine.png")


class NumberCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.number_font = pygame.font.SysFont("Arial", 500)
        self.number_of_nearby_mines = 1
        self.original_uncovered = self.uncovered_image.copy()
        self.uncovered_image = self.GetNumberImage()

    def Increment(self):
        self.number_of_nearby_mines += 1
        self.uncovered_image = self.GetNumberImage()

    def GetNumberImage(self):
        number_image = self.number_font.\
            render(str(self.number_of_nearby_mines), 5, (0, 0, 255))
        number_image = pygame.transform.scale(number_image, (self.rect.width,
                                                             self.rect.height))
        base_image = self.original_uncovered.copy()
        base_image.blit(number_image, (0, 0))
        return base_image
