from NeighborReasoningAI import *
from Game import *
from Board import *
from AI import *
from GamePresets import *
from Metrics import *

#extends Game to use the NeighborReasoningAI
class NeighborGame(Game):
    def __init__(self, length, bomb_preset=None, is_player_agent=True):
        super().__init__(length, bomb_preset=bomb_preset, is_player_agent=is_player_agent)
        self.agent = NeighborReasoningAI(self.board.board_length)

    def score(self, x, y):
        print("scoring attempted")
        count = 0
        length = self.board.row()
        adjacent_tiles = []
        for i in range(x - 1, x + 2, 1):
            for j in range(y - 1, y + 2, 1):
                if (0 <= i < length) and (0 <= j < length):
                    adjacent_tiles.append(self.board.layout[i][j])
        for tile in adjacent_tiles:
            if tile == -1:
                count += 1
        return count

    @staticmethod
    def agent_game():
        game = NeighborGame(9, "ms-easy", True)
        # game = Game(presets.presets[0][0], presets.presets[0][1], True)
        game.displayGameState()
        print('=======================================================')
        while not game.Over:
            game.agent_turn()
        game.metrics.register_agent(game.agent)
        game.displayGameState()
        game.metrics.end(log=True)

def main():
    for i in range(100):
        NeighborGame.agent_game()

if __name__ == '__main__':
    main()