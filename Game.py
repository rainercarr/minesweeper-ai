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

    def __init__(self, board):
        self.board = board
        #self.board.display()
        self.gameState = np.array( [[0 for i in range(0,self.board.row())] for j in range(0,self.board.col()) ] )

    def askInput(self):
        try:
            x,y = input('Enter coordinates for move [x y]: ').split()
            x = int(x)
            y = int(y)
            self.move(x-1,y-1)
        except ValueError:
            x,y = input('Invalid coordinates, try again: ').split()

    def move(self, x, y):
        if self.board.layout[x][y] == 0:
            print('Successful Move')
            self.gameState[x][y] = self.score(x,y)
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
        count = 0;
        length = self.board.row()

        if x == length - 1:
            if y == 1:
                adjacent_tiles = [self.board.layout[x-1][y], self.board.layout[x-1][y+1], self.board.layout[x][y + 1]]
            elif y == length-1:
                adjacent_tiles = [self.board.layout[x-1][y], self.board.layout[x-1][y-1], self.board.layout[x][y-1]]
            else:
                adjacent_tiles = [self.board.layout[x][y-1], self.board.layout[x-1][y-1], self.board.layout[x-1][y],
                                  self.board.layout[x-1][y+1], self.board.layout[x][y+1]]
        elif x == 1:
            if y == 1:
                adjacent_tiles = [self.board.layout[x][y+1], self.board.layout[x+1][y], self.board.layout[x+1][y+1]]
            elif y == length - 1:
                adjacent_tiles = [self.board.layout[x][y-1], self.board.layout[x+1][y-1], self.board.layout[x+1][y]]
            else:
                adjacent_tiles = [self.board.layout[x][y-1], self.board.layout[x+1][y-1], self.board.layout[x+1][y],
                                  self.board.layout[x+1][y+1], self.board.layout[x][y+1]]
        elif y == length - 1:
            if x == length - 1:
                adjacent_tiles = [self.board.layout[x][y-1], self.board.layout[x-1][y-1], self.board.layout[x-1][y]]
            elif x == 1:
                adjacent_tiles = [self.board.layout[x][y-1], self.board.layout[x+1][y-1], self.board.layout[x+1][y]]
            else:
                adjacent_tiles = [self.board.layout[x-1][y], self.board.layout[x-1][y-1], self.board.layout[x][y-1],
                                  self.board.layout[x+1][y-1], self.board.layout[x+1][y]]
        elif y == 1:
            if x == length - 1:
                adjacent_tiles = [self.board.layout[x-1][y], self.board.layout[x-1][y+1], self.board.layout[x][y+1]]
            elif x == 1:
                adjacent_tiles = [self.board.layout[x][y+1], self.board.layout[x+1][y+1], self.board.layout[x+1][y]]
            else:
                adjacent_tiles = [self.board.layout[x-1][y], self.board.layout[x-1][y+1], self.board.layout[x][y+1],
                                  self.board.layout[x+1][y+1], self.board.layout[x+1][y]]
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
    b = Board(8)
    game = Game(b)
    game.displayGameState()
    print('=======================================================')
    while(game.Over != True):
        game.askInput()

    #game.displayGameState()


main()