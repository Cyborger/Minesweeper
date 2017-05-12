import ZedLib
import Board
import pygame


class PlayingState(ZedLib.GameState):
    def __init__(self, game, cells_wide, cells_high):
        super().__init__(game)
        self.board = Board.Board(cells_wide, cells_high, 10)  # 10 mines
        self.board.CreateBoard()

    def DrawScreen(self):
        for cell in self.board.cells:
            self.game.screen.blit(cell.image, cell.rect)

    def HandleEvents(self):
        events = pygame.event.get()
        self.HandleBasicEvents(events)
        self.HandleMouseEvents(events)

    def HandleMouseEvents(self, events):
        mouse_pos = self.GetMousePosition()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.board.CheckMineClick(mouse_pos)
                elif event.button == 3:  # Right click
                    self.board.CheckFlagClick(mouse_pos)
