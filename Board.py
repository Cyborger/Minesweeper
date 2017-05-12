import Cell
import random


class Board:
    def __init__(self, width, height, mines):
        self.cells = []
        self.mines = []
        self.number_of_mines = mines
        self.cells_high = width
        self.cells_wide = height
        random.seed()

    def CreateBoard(self):
        self.CreateCells()
        self.CreateMines()
        self.CreateNumberCells()

    def CreateCells(self):
        margin = 1
        for x in range(self.cells_wide):
            for y in range(self.cells_high):
                # x_pos and y_pos are for the actual layout
                # while x and y are for determing neighbors
                x_pos = (margin * x) + x * 32 + margin
                y_pos = (margin * y) + y * 32 + margin
                new_cell = Cell.Cell(x, y)
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
        pass

    def CheckMineClick(self, mouse_pos):
        for cell in self.cells:
            if cell.CheckClick(mouse_pos):
                pass
                # cell.UncoverNearby(self.cells)

    def CheckFlagClick(self, mouse_pos):
        for cell in self.cells:
            cell.CheckFlag(mouse_pos)
