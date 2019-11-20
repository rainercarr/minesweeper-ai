import numpy as np
from main import *

class Game:
    """

    """
    board = ''
    gameState = np.array([])
    Over = False
    Score = 0

    def __init__(self, board):
        self.board = board
        #self.board.display()
        self.gameState = np.array( [[0 for i in range(0,self.board.row())] for j in range(0,self.board.col()) ] )

    def askInput(self):
        try:
            x,y = input('Enter coordinates for move: ').split()
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
        adjacent_tiles = [self.board.layout[x-1][y+1], self.board.layout[x-1][y], self.board.layout[x-1][y-1], self.board.layout[x][y+1],
             self.board.layout[x][y-1], self.board.layout[x+1][y+1], self.board.layout[x+1][y], self.board.layout[x+1][y-1]]

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