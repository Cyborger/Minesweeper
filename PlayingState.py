import ZedLib
import Board


class PlayingState(ZedLib.GameState):
    def __init__(self, game):
        super().__init__(game)
        self.board = Board.Board(9, 9, 10)  # 8 by 8 board with 10 mines
        self.board.CreateBoard()

    def DrawScreen(self):
        for cell in self.board.GetCellList():
            self.game.screen.blit(cell.image, cell.rect)
