import numpy as np
from random import randint

class Board:
    """
    Class for our Minesweeper Board, uses numpy 2D array filled with Tiles for structure.

    :var layout:
    :var board_length:
    """
    layout = np.array([])
    board_length = 0

    def __init__(self, length=None):
        if length != None:
            self.board_length = length
            self.layout = np.array( [[0 for i in range(0,self.board_length)] for j in range(0,self.board_length) ] )
        else:
            length = randint(8, 26)
            self.board_length = length
            self.layout = np.array( [ [0 for i in range(0,self.board_length)] for j in range(0,self.board_length) ] )

        bombRatio = ((self.board_length * self.board_length) / 2) - self.board_length
        #print(bombRatio)
        self.fill_bombs(bombRatio)

    def fill_bombs(self, numBombs):
        """
        Used to populate board with bombs, which are represented as -1
        :param board: Board object you wish to fill with bombs.
        :param numBombs: Number of bombs to place on board.
        """
        bomb_count = 0
        while (bomb_count != numBombs):
            # Uses randint to find a random coordinate
            x = randint(0, self.board_length - 1)
            y = randint(0, self.board_length - 1)

            # If random coordinate is empty then populate it with a bomb
            if self.layout[x][y] == 0:
                self.layout[x][y] = -1
                bomb_count += 1
            else:
                pass

    def display(self):
        """
        Used to display the state of Board
        :param board: Board object you wish to display states of
        """
        for row in range(0, self.board_length ):
            for col in range(0, self.board_length):
                print("{:5}".format(self.layout[row][col]), end=" ")
            print("")

    def at(self, row, column):
        return self.layout[row-1][column-1]

    def row(self):
        return self.board_length

    def col(self):
        return self.board_length

def main():
    game_board = Board(length=8)
    game_board.display()

    print(game_board.layout.shape)

if __name__ == '__main__':
    main()

'''
class Tile:
    """ 
    Class for squares in our minesweeper Board.
    Can be empty or have a bomb!
    :var state: Data from a specific square on the board. {0 represents an empty square, -1 represents a square with a bomb}
    """
    state = 0
'''