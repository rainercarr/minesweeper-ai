import itertools


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

    def make_move(self, game):
        move = self.choose_move()
        self.last_move = move
        game.agent_input(move[0], move[1])

    def known_safe_to_visit(self):
        for literal in self.literal_kb.keys():
            if (self.literal_kb[literal] is False) and (literal not in self.visited):
                print("Next move: known-safe")
                know_next_move = True
                return True, literal
        else:
            return False, None

    def not_reasoned_about(self):
        for i in range(1, self.board_length + 1):
            for j in range(1, self.board_length + 1):
                literal = (i, j)
                if (literal not in self.visited) and (literal not in self.containing_clauses) and (
                        literal not in self.literal_kb):
                    return True, literal
        else:
            return False, None

    def next_not_visited(self):
        for i in range(1, self.board_length + 1):
            for j in range(1, self.board_length + 1):
                literal = (i, j)
                if (literal not in self.visited) and (literal in self.containing_clauses) and (
                        literal not in self.literal_kb):
                    return literal
        else:
            return None

    def choose_move(self):
        move = None
        # if there are known-safe squares to visit
        known_safe, literal = self.known_safe_to_visit()
        if known_safe:
            move = literal
        # otherwise, if there are squares not reasoned about
        else:
            not_reasoned_about, literal = self.not_reasoned_about()
            if not_reasoned_about:
                move = literal
            # lastly, try the first square not visited
            else:
                move = self.next_not_visited()
        return move

    def set_last_seen_value(self, move_result):
        move_x = self.last_move[0]
        move_y = self.last_move[1]
        move_score = move_result[0]
        self.add_to_kb(move_x, move_y, False)
        self.infer_from_score(move_x, move_y, move_score)

    def add_to_kb(self, x, y, truth_value):
        #add to list of literals
        literal = (x, y)
        self.literal_kb[literal] = truth_value

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
                #remove the clauses in the deletion list
                for clause in deletion_list:
                    index_to_delete = self.compound_clauses[inference_from_square].index(clause)
                    del self.compound_clauses[inference_from_square][index_to_delete]

                #if only one clause is left in the compound clause (one set of possible neighbors remaining to be bombs),
                #it must be true--all must be bombs. Add all literals to KB
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

        if n == 0:
            self.infer_from_zero(x, y)
        else:
        #Rule 1: there exists one n-combination of distinct neighbors of (x, y) that are bombs where n > 0
        #Rule 2: if any neighbor is a known bomb it must be included in all possible combinations
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
