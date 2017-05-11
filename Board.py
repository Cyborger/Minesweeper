import Cell


class Board:
    def __init__(self, width, height, mines):
        self.grid = []
        self.number_of_mines = mines
        self.cells_high = width
        self.cells_wide = height

    def GetCellList(self):
        cell_list = []
        for row in self.grid:
            for cell in row:
                cell_list.append(cell)
        return cell_list

    def CreateBoard(self):
        self.CreateCells()
        self.CreateMines()
        self.CreateNumberCells()

    def CreateCells(self):
        for x in range(self.cells_wide):
            row_of_cells = []
            for y in range(self.cells_high):
                base_cell = Cell.Cell(x, y)
                row_of_cells.append(base_cell)
            self.grid.append(row_of_cells)

    def CreateMines(self):
        pass

    def CreateNumberCells(self):
        pass
