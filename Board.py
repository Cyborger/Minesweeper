import Cell
import random


class Board:
    def __init__(self, width, height, mines):
        self.cells = []
        self.mines = []
        self.number_of_mines = mines
        self.cells_high = width
        self.cells_wide = height
        self.lost = False
        random.seed()

    def CreateBoard(self):
        self.CreateCells()
        self.CreateMines()
        self.CreateNumberCells()

    def CreateCells(self):
        margin = 1
        for y in range(self.cells_wide):
            for x in range(self.cells_high):
                # x_pos and y_pos are for the actual layout
                # while x and y are for determing neighbors
                x_pos = (margin * x) + x * 32 + margin
                y_pos = (margin * y) + y * 32 + margin
                new_cell = Cell.EmptyCell(x, y)
                new_cell.SetPosition(x_pos, y_pos)
                self.cells.append(new_cell)

    def ReplaceCell(self, x, y, new_cell):
        for cell in self.cells:
            if cell.grid_x == x and cell.grid_y == y:
                new_cell.rect.x = cell.rect.x
                new_cell.rect.y = cell.rect.y
                self.cells[self.cells.index(cell)] = new_cell

    def CreateMines(self):
        for i in range(self.number_of_mines):
            found_valid_pos = False
            while not found_valid_pos:
                mine_pos = self.GetRandomMinePosition()
                new_mine = Cell.MineCell(mine_pos[0], mine_pos[1])
                found_valid_pos = True
                for mine in self.mines:
                    if (mine.grid_x == new_mine.grid_x
                            and mine.grid_y == new_mine.grid_y):
                        found_valid_pos = False
            self.AddMine(new_mine)

    def AddMine(self, mine):
        self.mines.append(mine)
        self.ReplaceCell(mine.grid_x, mine.grid_y, mine)

    def GetRandomMinePosition(self):
        x = random.randint(0, self.cells_wide - 1)
        y = random.randint(0, self.cells_high - 1)
        return (x, y)

    def CreateNumberCells(self):
        for mine in self.mines:
            cells_to_increment = self.GetSurroundingNumberOrEmptyCells(mine)
            for cell in cells_to_increment:
                if isinstance(cell, Cell.EmptyCell):
                    new_number_cell = Cell.\
                        NumberCell(cell.grid_x, cell.grid_y)
                    new_number_cell.rect.x = cell.rect.x
                    new_number_cell.rect.y = cell.rect.y
                    self.ReplaceCell(new_number_cell.grid_x,
                                     new_number_cell.grid_y,
                                     new_number_cell)
                elif isinstance(cell, Cell.NumberCell):
                    cell.Increment()

    def GetSurroundingNumberOrEmptyCells(self, center_cell):
        nearby_cells = []
        for cell in self.cells:
            if (cell.grid_x >= center_cell.grid_x - 1
                    and cell.grid_x <= center_cell.grid_x + 1):
                if (cell.grid_y >= center_cell.grid_y - 1
                        and cell.grid_y <= center_cell.grid_y + 1):
                    if (isinstance(cell, Cell.EmptyCell)
                            or isinstance(cell, Cell.NumberCell)):
                        nearby_cells.append(cell)
        return nearby_cells

    def CheckMineClick(self, mouse_pos):
        for cell in self.cells:
            if cell.CheckClick(mouse_pos):
                if isinstance(cell, Cell.EmptyCell):
                    cell.UncoverNearby(self.cells)
                elif isinstance(cell, Cell.MineCell):
                    self.lost = True

    def CheckFlagClick(self, mouse_pos):
        for cell in self.cells:
            cell.CheckFlag(mouse_pos)

    def Reset(self):
        self.cells = []
        self.mines = []
        self.CreateBoard()
        self.lost = False
