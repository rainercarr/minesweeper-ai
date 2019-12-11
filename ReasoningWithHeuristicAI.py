
import numpy as np
from NeighborReasoningAI import *

class ReasoningWithHeuristicAI(NeighborReasoningAI):

    def __init__(self, length):
        super().__init__(length)

        #records scores for ease of access in a 2d array (in this case, -1 is known bomb, -2 is unknown contents)
        self.score_memory = np.array([[-2 for i in range(self.board_length + 1)] for j in range(self.board_length + 1)])
        #holds a board with the current heuristic value of all cells
        self.heuristic_board = None

    #fills out heuristic board according to known score memory
    def calculate_heuristic(self):
        self.heuristic_board = np.array([[9 for i in range(self.board_length + 1)] for j in range(self.board_length + 1)], dtype='float16')
        for x in range(1, self.board_length + 1):
            for y in range(1, self.board_length + 1):

                #check status of neighbors of square
                bomb_neighbors = 0
                unknown_neighbors = []
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if 0 < i <= self.board_length and 0 < j <= self.board_length:
                            #record unknown neighbors
                            if (i, j) not in self.literal_kb:
                                unknown_neighbors.append((i, j))
                            #if neighbor listed as true in literal KB
                            elif self.literal_kb[(i, j)]:
                                bomb_neighbors += 1

                if len(unknown_neighbors) > 0 and self.score_memory[x][y] > 0:
                    if self.score_memory[x][y] - bomb_neighbors >= 0:
                        heuristic_value = (self.score_memory[x][y] - bomb_neighbors) / len(unknown_neighbors)
                        for neighbor in unknown_neighbors:
                            if self.heuristic_board[neighbor[0]][neighbor[1]] == 9:
                                self.heuristic_board[neighbor[0]][neighbor[1]] = heuristic_value
                            else:
                                self.heuristic_board[neighbor[0]][neighbor[1]] += heuristic_value

    #returns minimum heuristic value and square with its location
    def min_heuristic(self):
        self.calculate_heuristic()
        # once completely updated, get the tuple with coordinates of the lowest square and its value
        min_heuristic_square = (1, 1)
        min_heuristic_value = 9

        for i in range(1, len(self.heuristic_board)):
            for j in range(1, len(self.heuristic_board)):
                if (i, j) not in self.visited:
                    first_not_visited = (i, j)
                if self.heuristic_board[i][j] < min_heuristic_value and (i, j) not in self.visited:
                    min_heuristic_value = self.heuristic_board[i][j]
                    min_heuristic_square = (i, j)
        if min_heuristic_value == 9:
            min_heuristic_square = first_not_visited
        return min_heuristic_square, min_heuristic_value

    def choose_move(self):
        move = None

        # if there are known-safe squares to visit
        known_safe, literal = self.known_safe_to_visit()
        if known_safe:
            move = literal
        else:
            # check the heuristics: if there is a place safer than the threshold, go there
            threshold = 0.14
            min_heuristic_square, min_heuristic_value = self.min_heuristic()
            if min_heuristic_value < threshold and min_heuristic_square not in self.visited:
                move = min_heuristic_square
            else:
                # if no known-safe squares to visit, and the minimum heuristic is above the threshold,
                # but there are squares that have not been reasoned about to visit
                not_reasoned_about, literal = self.not_reasoned_about()
                if not_reasoned_about:
                    move = literal
                else:
                    #lastly, if none of those hold true, go to the heuristic cell even if it is above the threshold
                    move = min_heuristic_square
        return move

    def add_to_kb(self, x, y, truth_value):
        super().add_to_kb(x, y, truth_value)
        if truth_value:
            #record as a known bomb
            self.score_memory[x][y] = -1
        elif self.score_memory[x][y] == -2:
            #1 is the default estimate for an unknown square's score
            self.score_memory[x][y] = 1

    def infer_from_score(self, x, y, n):
        if n == -1:
            return
        else:
            self.score_memory[x][y] = n
            super().infer_from_score(x, y, n)