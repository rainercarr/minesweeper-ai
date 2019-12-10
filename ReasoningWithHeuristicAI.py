#AI using forward-chaining

import itertools
import numpy as np


class NeighborReasoningAI():

    def __init__(self, length):
        self.board_length = length
        #a dictionary with keys (x, y) for known literals, and values True/False
        self.literal_kb = dict()
        #squares that have been visited
        self.visited = set()
        #squares that are known safe and have not yet been visited
        self.unvisited = set()
        #each key is a square literal (x, y) and the corresponding value is a set of indices in compound_clauses where that
        #literal may be found
        self.containing_clauses = dict()

        #the keys are square literals, the values a set of clauses inferred from the score of the square
        self.compound_clauses = dict()

        #the last move played by the AI
        self.last_move = None

        #records scores for ease of access in a 2d array (in this case, -1 is known bomb, -2 is unknown contents)
        self.score_memory = np.array([[-2 for i in range(self.board_length + 1)] for j in range(self.board_length + 1)])

    def make_move(self, game):
        move = self.choose_move()
        self.last_move = move
        game.agent_input(move[0], move[1])

    #return a board with the current heuristic value of all cells
    def min_heuristic(self):
        heuristic_board = np.array([[9 for i in range(self.board_length + 1)] for j in range(self.board_length + 1)], dtype='float16')
        print("Score memory: ")
        print(self.score_memory)
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
                            if heuristic_board[neighbor[0]][neighbor[1]] == 9:
                                heuristic_board[neighbor[0]][neighbor[1]] = heuristic_value
                            else:
                                heuristic_board[neighbor[0]][neighbor[1]] += heuristic_value
        #once completely updated, get the tuple with coordinates of the lowest square and its value

        min_heuristic_square = (1, 1)
        min_heuristic_value = 9

        for i in range(1, len(heuristic_board)):
            for j in range(1, len(heuristic_board)):
                if (i, j) not in self.visited:
                    first_not_visited = (i, j)
                if heuristic_board[i][j] < min_heuristic_value and (i, j) not in self.visited:
                    min_heuristic_value = heuristic_board[i][j]
                    min_heuristic_square = (i, j)
        if min_heuristic_value == 9:
            min_heuristic_square = first_not_visited
        print(heuristic_board)
        print("Min heuristic square: ", min_heuristic_square)
        print("Min heuristic value: ", min_heuristic_value)
        return min_heuristic_square, min_heuristic_value



    def choose_move(self):
        know_next_move = False
        move = None

        # if there are known-safe squares to visit
        for literal in self.literal_kb.keys():
            if (self.literal_kb[literal] is False) and (literal not in self.visited):
                print("Next move: known-safe")
                know_next_move = True
                return literal

        # check the heuristics: if there is a place safer than the threshold, go there
        threshold = 0.14
        min_heuristic_square, min_heuristic_value = self.min_heuristic()
        if min_heuristic_value < threshold and min_heuristic_square not in self.visited:
            return min_heuristic_square

        # if no known-safe squares to visit, and the minimum heuristic is above the threshold,
        # but there are squares that have not been reasoned about to visit
        for i in range(1, self.board_length + 1):
            for j in range(1, self.board_length + 1):
                literal = (i, j)
                if (literal not in self.visited) and (literal not in self.containing_clauses) and (literal not in self.literal_kb):
                    print("Next move: not reasoned about")
                    know_next_move = True
                    return literal

        #lastly, if none of those hold true, go to the heuristic cell
        return min_heuristic_square

        '''
        for i in range(1, self.board_length + 1):
            for j in range(1, self.board_length + 1):
                if (literal not in self.visited) and (literal in self.containing_clauses) and (literal not in self.literal_kb):
                    return literal
        '''

    def set_last_seen_value(self, move_result):
        move_x = self.last_move[0]
        move_y = self.last_move[1]
        move_score = move_result[0]
        print("Move score returned from Game:")
        print(move_result[0])
        self.score_memory[move_x][move_y] = move_score
        self.add_to_kb(move_x, move_y, False)
        self.infer_from_score(move_x, move_y, move_score)
        print("Literal KB: ")
        print(self.literal_kb)
        print("Compound clauses: ")
        print(self.compound_clauses)
        print("Containing clauses: ")
        print(self.containing_clauses)

    def add_to_kb(self, x, y, truth_value):
        #add to list of literals
        literal = (x, y)
        self.literal_kb[literal] = truth_value

        #add to score memory

        if truth_value:
            #record as a known bomb
            self.score_memory[x][y] = -1
        elif self.score_memory[x][y] == -2:
            #1 is the default estimate for an unknown square's score
            self.score_memory[x][y] = 1

        #check through all compound clauses in the KB that contain the given literal
        if literal in self.containing_clauses:
            for inference_from_square in self.containing_clauses[literal]:
                deletion_list = []
                #check each clause in the set of clauses (which have an OR relation to one another) inferred from the given square
                for clause in self.compound_clauses[inference_from_square]:
                    #if the truth value in the KB for this literal is true
                    if truth_value is True:
                        #add clauses to the deletion list that do not contain it
                        if literal not in clause:
                            deletion_list.append(clause)
                    #if the truth value in the KB for this literal is false
                    elif truth_value is False:
                        #add clauses to the deletion list that contain it
                        if literal in clause:
                            deletion_list.append(clause)
                for clause in deletion_list:
                    index_to_delete = self.compound_clauses[inference_from_square].index(clause)
                    del self.compound_clauses[inference_from_square][index_to_delete]
                #if only one clause is left in the compound clause (one set of possible neighbors remaining to be bombs),
                #it must be true--all must be bombs. add all literals to KB
                if len(self.compound_clauses[inference_from_square]) == 1:
                    literals_to_add = []
                    for clause in self.compound_clauses[inference_from_square]:
                        if len(clause) > 0:
                            for clause_literal in clause:
                                if len(clause_literal) > 1:
                                    literals_to_add.append((clause_literal[0], clause_literal[1], True))
                    self.compound_clauses[inference_from_square] = []

                    num_literals_to_add = len(literals_to_add)
                    for i in range(num_literals_to_add):
                        l = literals_to_add.pop()
                        self.add_to_kb(l[0], l[1], True)

            #may want to delete more entries from containing_clauses if inefficient
            if truth_value is False:
                self.containing_clauses[literal] = {}

    def add_to_containing_clauses(self, neighbors, literal):
        for neighbor in neighbors:
            if neighbor in self.containing_clauses:
                self.containing_clauses[neighbor].add(literal)
            else:
                self.containing_clauses[neighbor] = {literal}

    def infer_from_score(self, x, y, n):
        self.visited.add((x, y))
        literal = (x, y)
        unknown_neighbors = []
        bomb_neighbors = []

        def create_combinations(neighbors, n):
            compound_clause = list(itertools.combinations(neighbors, n))
            compound_clause = [set(i) for i in compound_clause]
            return compound_clause

        if n == -1:
            return
        if n == 0:
            self.infer_from_zero(x, y)
        else:
        #Rule 1: there exists one n-combination of distinct neighbors of (x, y) that are bombs where n > 0
        #Rule 2: if any neighbor is a known bomb it must be included in all possible combinations

        #check all neighbors
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if 0 < i <= self.board_length and 0 < j <= self.board_length:
                        if not (i == x and j == y):
                            neighbor = (i, j)
                            # neighbor is a known bomb (if neighbor is known safe, we do not add it)
                            if (neighbor in self.literal_kb) and self.literal_kb[neighbor] is True:
                                bomb_neighbors.append(neighbor)
                            #neighbor not in literal KB
                            elif neighbor not in self.literal_kb:
                                unknown_neighbors.append(neighbor)
            print("Unknown neighbors: " + str(unknown_neighbors))
            print("Bomb neighbors: " + str(bomb_neighbors))
            #add all n-combinations of neighbors to the list

            if len(bomb_neighbors) == 0 and n > 0:
                self.compound_clauses[literal] = create_combinations(unknown_neighbors, n)
                # make sure containing_clauses refers to this compound clause for each unknown neighbor
                self.add_to_containing_clauses(unknown_neighbors, literal)

            #if there are bomb neighbors
            else:
                non_bomb = n - len(bomb_neighbors)
                #if the score of (x, y) is n, there are n bomb neighbors
                    #if n neighbors are known bombs, there is no change in the knowledge base
                if non_bomb >= 1:
                    compound_clause = create_combinations(unknown_neighbors, non_bomb)
                    for clause in compound_clause:
                        clause = clause.union(set(bomb_neighbors))
                    self.compound_clauses[literal] = compound_clause
                    # make sure containing_clauses refers to this compound clause for each unknown neighbor
                    self.add_to_containing_clauses(unknown_neighbors + bomb_neighbors, literal)
            #if there ends up being only one clause with n elements, all elements must logically be bombs

            if literal in self.compound_clauses:
                if len(self.compound_clauses[literal]) == 1:
                    for clause in self.compound_clauses[literal]:
                        for clause_literal in clause:
                            self.add_to_kb(clause_literal[0], clause_literal[1], True)
                    self.compound_clauses[literal] = []

    def infer_from_zero(self, x, y):
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 < i <= self.board_length and 0 < j <= self.board_length:
                    literal = (i, j)
                    self.literal_kb[literal] = False

    def run(self):
        x, y, n = input('Please enter x, y, and the number you got out of the game [x y n]: ').split()
        x = int(x)
        y = int(y)
        n = int(n)
        self.add_to_kb(x, y, False)
        self.infer_from_score(x, y, n)
        print("Literal KB: ")
        print(self.literal_kb)
        print("Compound clauses: ")
        print(self.compound_clauses)
        print("Containing clauses: ")
        print(self.containing_clauses)
        #get move from literals
        for literal in self.literal_kb.keys():
            if (self.literal_kb[literal] is False) and (literal not in self.visited):
                print("Next move: " + str(literal))
                break
        #if none available, just get something random:


if __name__ == '__main__':
    ai = NeighborReasoningAI(8)
    while True:
        ai.run()
