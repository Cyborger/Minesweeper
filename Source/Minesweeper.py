import ZedLib
import PlayingState


class Minesweeper(ZedLib.Game):
    def __init__(self):
        num_of_cells_wide = 9
        num_of_cells_high = 9
        super().__init__(num_of_cells_wide*32 + num_of_cells_wide + 1,
                         num_of_cells_high*32 + num_of_cells_high + 1)
        self.playing_state = PlayingState.PlayingState(self, num_of_cells_wide,
                                                       num_of_cells_high)

    def Start(self):
        self.ChangeState(self.playing_state)
        self.Loop()
