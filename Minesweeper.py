import ZedLib
import PlayingState


class Minesweeper(ZedLib.Game):
    def __init__(self):
        super().__init__(9*32, 9*32)
        self.playing_state = PlayingState.PlayingState(self)

    def Start(self):
        self.ChangeState(self.playing_state)
        self.Loop()
