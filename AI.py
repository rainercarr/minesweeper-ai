import numpy as np
from KnowledgeBase import *


class AI:

    last_seen_result = [0, "Move was successful"]
    next_move = None
    next_uninformed_move = (1, 1)
    know_next_move = False
    made_uninformed_move = False
    board_length = 0

    def __init__(self, length):
        self.next_uninformed_move = (1, 1)
        self.board_length = length
        self.kb = KnowledgeBase(length)


    def make_move(self, game):
        # Ask the KB for a valid move
        # If the KB can't decide, have the uninformed_move work
        # The move is made and a result is given
        # Add the move to the KB
        # Add inferences to the other portion of the KB
        # x = input("Waiting before making a move")
        self.think_of_moves()

        self.made_uninformed_move = False
        self.know_next_move = False
        self.next_move = None

        self.next_move = self.choose_kb_move()
        if self.know_next_move is False:
            self.next_move = self.make_uninformed_move()
        game.agent_input(self.next_move[0], self.next_move[1])

    def choose_kb_move(self):
        possible_move = self.kb.get_move()
        if possible_move is not None:
            self.know_next_move = True
        return possible_move

    def think_of_moves(self):
        self.kb.resolve_inferences()

    def make_uninformed_move(self):
        # If an uninformed move was made last turn and it resulted in leaving the play space,
        # then set the next uniformed move to be the start of the next row
        while self.next_move is None:
            if self.next_uninformed_move in self.kb.known_locations:
                # pick the next uninformed location
                current_row = self.next_uninformed_move[0]
                next_column = self.next_uninformed_move[1] + 1
                self.next_uninformed_move = (current_row, next_column)
            else:
                self.next_move = self.next_uninformed_move
                self.made_uninformed_move = True

        return self.next_move

    def set_last_seen_value(self, result):
        self.last_seen_result = result
        if self.last_seen_result[0] >= 0:
            #self.kb.add_to_locations(self.next_move)
            self.kb.location_value_seen(self.next_move, self.last_seen_result[0])
        elif self.last_seen_result[0] == -1 and self.made_uninformed_move is True:
            next_uninformed_row = self.next_uninformed_move[0] + 1
            first_column = 1
            self.next_uninformed_move = (next_uninformed_row, first_column)

    def get_current_board_length(self):
        return self.board_length
