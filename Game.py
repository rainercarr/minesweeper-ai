import numpy as np
from Board import *
from NeighborReasoningAI import *
from ReasoningWithHeuristicAI import *
from Metrics import *

class Game:
    """
    Class for a playing a game of Minesweeper using a Board object
    """

    def __init__(self, length, bomb_preset=None, is_player_agent=True, heuristics=False):
        self.visited = []
        self.Over = False
        self.board = Board(length, bomb_preset)
        self.agent = None
        self.hidden_space = u"\u25A1"
        self.gameState = np.array([[self.hidden_space for i in range(0, self.board.row())] for j in range(0, self.board.col())])
        if is_player_agent:
            if heuristics:
                self.agent = ReasoningWithHeuristicAI(self.board.board_length)
            else:
                self.agent = NeighborReasoningAI(self.board.board_length)
        self.unrevealed_safe_locations = int(self.board.total_spaces - self.board.total_bombs)

        #initialize metrics
        self.metrics = Metrics()
        self.metrics.board_length = self.board.board_length
        self.metrics.board_bombs = self.board.total_bombs

    def askInput(self):
        try:
            x, y = input('Enter coordinates for move [x y]: ').split()
            x = int(x)
            y = int(y)
            if x <= 0 or y <= 0:
                print('Move is outside of play space')
                self.metrics.record_move()
            else:
                self.move(x - 1, y - 1)
        except ValueError:
            print('Invalid input for coordinates')
            self.metrics.record_move()
        except IndexError:
            print('Move is outside of play space')
            self.metrics.record_move()

    def move(self, x, y):
        self.metrics.record_move()
        if self.board.layout[x][y] == 0:
            print('Successful Move')
            score_at_location = self.score(x, y)
            self.gameState[x][y] = score_at_location
            self.metrics.record_successful_move()
            self.gameState[x][y] = self.score(x, y)
            self.displayGameState()
            print('=================================================================')
            self.unrevealed_safe_locations -= 1
            self.check_if_game_won()
        elif self.board.layout[x][y] == -1:
            print('BOOM!!')
            print('Game Over!!')
            print('=================================================================')
            self.board.display()
            print('=================================================================')
            self.Over = True

    def agent_turn(self):
        # ask agent for move
        # update agent with what's see
        self.metrics.record_move()
        self.agent.make_move(self)

    def agent_input(self, x, y):
        move_result = [0, "Move was successful"]
        print("Making Move: ", x, " ", y)

        if x <= 0 or y <= 0:
            move_result = [-1, "The move was outside of the play area"]
        elif x > self.board.board_length or y > self.board.board_length:
            move_result = [-1, "The move was outside of the play area"]
        else:
            move_result = self.agent_move(x - 1, y - 1)
        self.agent.set_last_seen_value(move_result)

    def agent_move(self, x, y):
        move_result = [0, "Move was successful"]
        if self.gameState[x][y] != self.hidden_space:
            move_result = [-2, "Move already made"]
            return move_result
        elif self.board.layout[x][y] == 0:
            self.metrics.record_successful_move()
            print('Successful Move')
            score_at_location = self.score(x, y)
            self.gameState[x][y] = score_at_location
            move_result = (score_at_location, "Move was successful")
            '''
            # Unsure if this should be added here
            if score_at_location == 0:
                self.reveal_near(x,y)
            # ==================================
            '''
            self.displayGameState()
            print('=================================================================')
            self.unrevealed_safe_locations -= 1
            self.check_if_game_won()
        elif self.board.layout[x][y] == -1:
            print('Game Over!!')
            print('=================================================================')
            self.board.display()
            print('=================================================================')
            self.Over = True
        return move_result

    def score(self, x, y):
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

    def check_if_game_won(self):
        if self.unrevealed_safe_locations == 0:
            self.metrics.outcome = "Win"
            print('You Won!')
            print('=================================================================')
            self.board.display()
            print('=================================================================')
            self.Over = True

    def displayGameState(self):
        for row in range(0, len(self.gameState[0]) ):
            for col in range(0, len(self.gameState)):
                print("{:5}".format(self.gameState[row][col]), end=" ")
            print("")

    @staticmethod
    def human_game():
        game = Game(8, "easy", False)
        game.displayGameState()
        print('=======================================================')
        while not game.Over:
            game.askInput()

        #game.displayGameState()
        game.metrics.end(log=True)

    @staticmethod
    def agent_game(board_size, bombs, heuristic_agent=False):
        game = Game(board_size, bomb_preset=bombs, is_player_agent=True, heuristics=heuristic_agent)
        game.displayGameState()
        print('=======================================================')
        while not game.Over:
            game.agent_turn()
        game.metrics.register_agent(game.agent)
        game.displayGameState()
        game.metrics.end(log=True)

    @staticmethod
    def run_tests(iterations, heuristic_agent=False):
        for i in range(iterations):
            Game.agent_game(4, 2, heuristic_agent)
            Game.agent_game(4, 4, heuristic_agent)
            Game.agent_game(9, 10, heuristic_agent)
            Game.agent_game(9, 32, heuristic_agent)
            Game.agent_game(16, 32, heuristic_agent)
def main():
    game_mode = input("Welcome to Exception Dodgers Minesweeper! Choose P for a human player, A for a single agent game, or T to run tests on the agent: ")
    if game_mode == "P":
        Game.human_game()
    elif game_mode == "A":
        board_size = int(input("Please specify a board size between 4 and 16 (4 is a 4x4 board): "))
        mines = int(input("Please specify a number of mines less than the total number of squares on your board: "))
        heuristic = input("NeighborReasoningAI(N) with no heuristic,  or ReasoningWithHeuristicAI (H)? ")
        if heuristic == "N":
            Game.agent_game(board_size, mines)
        elif heuristic == "H":
            Game.agent_game(board_size, mines, heuristic_agent=True)
    elif game_mode == "T":
        print("Each iteration runs of one test game of each type:")
        print("4x4 with 2 mines, 4x4 with 4 mines, 9x9 with 10 mines, 9x9 with 32 mines, and 16x16 with 32 mines.");
        print("The results are written to metrics.csv.")
        test_iterations = int(input("How many iterations would you like in your test run? "))
        heuristic_agent = input("Would you like to use the NeighborReasoningAI (N) or the ReasoningWithHeuristicAI (H) for the tests? ")
        if heuristic_agent == "N":
            Game.run_tests(test_iterations)
        elif heuristic_agent == "H":
            Game.run_tests(test_iterations, heuristic_agent=True)
        else:
            print("Invalid entry, exiting")
    else:
        print("Invalid entry, exiting")


if __name__ == '__main__':
    main()


