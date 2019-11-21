import numpy as np

class AI:
    """

    :var KB: A 2D array the same size of the Game board containing the AI’s knowledge of the board
    """
    KB = np.array([])


    def __init__(self, row, col):
        self.KB = np.array( [[0 for i in range(0,row)] for j in range(0,col) ] )
        print(self.KB)

    def play(self):
        """

        :return:
        """
        pass

    def nextMove(self):
        """

        :return:
        """
        pass


a = AI(8,8)