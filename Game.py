import numpy as np
from Board import *

class Game:
    """
    Class for a playing a game of Minesweeper using a Board object
    """
    board = np.array([])
    gameState = np.array([])
    Over = False
    Score = 0

    def __init__(self, length, bomb_preset=None, is_player_agent=False):
        self.board = Board(length, bomb_preset)
        #self.board.display()
        self.hidden_space = u"\u25A1"
        self.gameState = np.array([[self.hidden_space for i in range(0, self.board.row())] for j in range(0, self.board.col())])

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
            # x,y = input('Invalid coordinates, try again: ').split()
            print('Invalid input for coordinates')
        except IndexError:
            # x,y = input('Move is outside of play space, try again: ').split()
            print('Move is outside of play space')

    def move(self, x, y):
        if self.board.layout[x][y] == 0:
            print('Successful Move')
            self.gameState[x][y] = self.score(x, y)
            self.displayGameState()
            print('=================================================================')
            #self.board.display()
        elif self.board.layout[x][y] == -1:
            print('BOOM!!')
            print('Game Over!!')
            print('=================================================================')
            self.board.display()
            print('=================================================================')
            self.Over = True


    def flag(self, x, y):
        self.board.layout == 777



    def score(self, x, y):
        count = 0
        length = self.board.row()

        if x == length - 1:
            if y == 0:
                adjacent_tiles = [self.board.layout[x - 1][y], self.board.layout[x - 1][y + 1], self.board.layout[x][y + 1]]
            elif y == length - 1:
                adjacent_tiles = [self.board.layout[x - 1][y], self.board.layout[x - 1][y - 1], self.board.layout[x][y - 1]]
            else:
                adjacent_tiles = [self.board.layout[x][y - 1], self.board.layout[x - 1][y - 1], self.board.layout[x - 1][y],
                                  self.board.layout[x - 1][y + 1], self.board.layout[x][y + 1]]
        elif x == 0:
            if y == 0:
                adjacent_tiles = [self.board.layout[x][y + 1], self.board.layout[x + 1][y], self.board.layout[x + 1][y + 1]]
            elif y == length - 1:
                adjacent_tiles = [self.board.layout[x][y - 1], self.board.layout[x + 1][y - 1], self.board.layout[x + 1][y]]
            else:
                adjacent_tiles = [self.board.layout[x][y - 1], self.board.layout[x + 1][y - 1], self.board.layout[x + 1][y],
                                  self.board.layout[x + 1][y + 1], self.board.layout[x][y + 1]]
        elif y == length - 1:
            if x == length - 1:
                adjacent_tiles = [self.board.layout[x][y - 1], self.board.layout[x - 1][y - 1], self.board.layout[x - 1][y]]
            elif x == 1:
                adjacent_tiles = [self.board.layout[x][y - 1], self.board.layout[x + 1][y - 1], self.board.layout[x + 1][y]]
            else:
                adjacent_tiles = [self.board.layout[x - 1][y], self.board.layout[x - 1][y - 1], self.board.layout[x][y - 1],
                                  self.board.layout[x + 1][y - 1], self.board.layout[x + 1][y]]
        elif y == 0:
            if x == length - 1:
                adjacent_tiles = [self.board.layout[x - 1][y], self.board.layout[x - 1][y + 1], self.board.layout[x][y + 1]]
            elif x == 0:
                adjacent_tiles = [self.board.layout[x][y + 1], self.board.layout[x + 1][y + 1], self.board.layout[x + 1][y]]
            else:
                adjacent_tiles = [self.board.layout[x - 1][y], self.board.layout[x - 1][y + 1], self.board.layout[x][y + 1],
                                  self.board.layout[x + 1][y + 1], self.board.layout[x + 1][y]]
        else:
            adjacent_tiles = [self.board.layout[x - 1][y + 1], self.board.layout[x - 1][y], self.board.layout[x - 1][y - 1],
                            self.board.layout[x][y + 1], self.board.layout[x][y - 1], self.board.layout[x + 1][y + 1],
                            self.board.layout[x + 1][y], self.board.layout[x + 1][y - 1]]

        for tile in adjacent_tiles:
            if tile == -1:
                count +=1
        return count


    def displayGameState(self):
        for row in range(0, len(self.gameState[0]) ):
            for col in range(0, len(self.gameState)):
                print("{:5}".format(self.gameState[row][col]), end=" ")
            print("")

def main():
    game = Game(8)
    game.displayGameState()
    print('=======================================================')
    while not game.Over:
        game.askInput()

    game.displayGameState()


if __name__ == '__main__':
    main()
