import numpy as np
from Board import *
from AI import *
from GamePresets import *
from Metrics import *

class Game:
    """
    Class for a playing a game of Minesweeper using a Board object
    """
    board = np.array([])
    gameState = np.array([])
    Over = False
    Score = 0
    agent = None
    unrevealed_safe_locations = 0
    visited = []
    def __init__(self, length, bomb_preset=None, is_player_agent=True):
        self.board = Board(length, bomb_preset)
        self.hidden_space = u"\u25A1"
        self.gameState = np.array([[self.hidden_space for i in range(0, self.board.row())] for j in range(0, self.board.col())])
        if is_player_agent:
            self.agent = AI(self.board.board_length)
        self.unrevealed_safe_locations = int(self.board.total_spaces - self.board.total_bombs)
        self.metrics = Metrics()

    def askInput(self):
        try:
            x, y = input('Enter coordinates for move [x y]: ').split()
            x = int(x)
            y = int(y)
            if x <= 0 or y <= 0:
                print('Move is outside of play space')
            else:
                self.move(x - 1, y - 1)
        except ValueError:
            print('Invalid input for coordinates')
        except IndexError:
            print('Move is outside of play space')

    def move(self, x, y):
        self.metrics.record_move()
        if self.board.layout[x][y] == 0:
            print('Successful Move')
            score_at_location = self.score(x, y)
            self.gameState[x][y] = score_at_location
            if score_at_location == 0:
                self.reveal_near(x,y)
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
            print('Successful Move')
            score_at_location = self.score(x, y)
            self.gameState[x][y] = score_at_location
            move_result = (score_at_location, "Move was successful")

            # Unsure if this should be added here
            if score_at_location == 0:
                self.reveal_near(x,y)
            # ==================================
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

    #INCOMPLETE METHOD
    def flag(self, x, y):
        pass

    def score(self, x, y):
        '''
        Counts bombs found in valid adjacent locations
        '''
        nearby_bombs = 0
        notbomb_locations = []
        bomb_locations = []

        for (dx,dy) in [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]:
            if self.inbounds(x+dx, y+dy):
                if self.board.layout[x+dx][y+dy] == -1:
                    nearby_bombs += 1
                    bomb_locations.append((x+dx,y+dy))
                else:
                    notbomb_locations.append((x+dx,y+dy))

        return nearby_bombs

    def inbounds(self,x,y):
        '''
        Used by score method to check if adjacent locations are within the boards boundaries
        '''
        if x >= 0 and x < self.board.board_length and y >= 0 and y < self.board.board_length:
            return True

        return False

    def reveal_near(self,x,y):
        '''
        recursive method that reveals scores of nearby squares, initially called when a 0 is scored
        Base cases: if out of bounds, if already computed, if bomb, if is greater than 0
        '''
        if self.inbounds(x,y) == False:
            return
        if (x,y) in self.visited:
            return
        if self.board.layout[x][y] == -1:
            return

        self.visited.append((x, y))

        s = self.score(x,y)
        self.gameState[x][y] = s

        if s > 0:
            return

        for (dx, dy) in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            self.reveal_near(x+dx,y+dy)

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
        presets = GamePresets()
        game = Game(8, "easy", False)
        # game = Game(presets.presets[0][0], presets.presets[0][1], False)
        game.displayGameState()
        print('=======================================================')
        while not game.Over:
            game.askInput()

        #game.displayGameState()
        game.metrics.end(log=True)

    @staticmethod
    def agent_game():
        presets = GamePresets()
        game = Game(12, "easy", True)
        # game = Game(presets.presets[0][0], presets.presets[0][1], True)
        game.displayGameState()
        print('=======================================================')
        while not game.Over:
            game.agent_turn()
        game.metrics.register_agent(game.agent)
        game.displayGameState()
        game.metrics.end(log=True)

def main():
    game_mode = input("A or P: ")
    if game_mode == "P":
        Game.human_game()
    elif game_mode == "A":
        Game.agent_game()

if __name__ == '__main__':
    main()


