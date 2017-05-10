import ZedLib
import random
import Cell

class PlayingState(ZedLib.GameState):
    def __init__(self, game):
        super().__init__(game)
        self.mines = []
        self.max_mines = 8

    def CreateBoard(self):
        self.CreateMines()
        self.CreateNumberCells()

    def CreateMines(self):
        for i in range(self.max_mines):
            new_pos = self.GetMinePosition()
            new_mine = Cell.MineCell(new_pos[0], new_pos[1])
            self.mines.append(new_mine)

    def GetMinePosition(self):
        x = 0
        y = 0
        found_valid_pos = False
        while not found_valid_pos:
            max_x = self.game.screen_width
            max_y = self.game.screen_height
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            for mine in self.mines:
                if mine.rect.x != x and mine.rect.y != y:
                    found_valid_pos = True
        return (x, y)

    def CreateNumberCells(self):
        for mine in self.mines:
            pass
