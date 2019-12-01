from AI import *


class KnowledgeBase:

    board_length = None

    def __init__(self, length):
        self.known_locations = {}
        self.unresolved_inferences = []
        self.board_length = length
        self.possible_moves = []
        self.valid_flag = ("Flag", "Valid")
        self.invalid_flag = ("Flag", "Invalid")
        self.solved_flag = ("Flag", "Solved")

    def add_to_locations(self, location):
        self.known_locations[location] = False

    def add_known_bomb(self, location):
        self.known_locations[location] = True

    def location_value_seen(self, location, value):
        self.add_to_locations(location)
        adjacent_location_values = self.find_adjacent_locations(location)
        permutations = []
        selected = []
        self.generate_permutations(permutations, adjacent_location_values, selected, value)
        self.unresolved_inferences.append(permutations)

        if value == 0:
            self.handle_zero_values(adjacent_location_values)

    def handle_zero_values(self, locations):
        for location in locations:
            if location not in self.known_locations:
                self.possible_moves.append(location)

    def generate_permutations(self, permutations, unselected, selected, depth):
        if len(selected) == depth:
            valid_permutation = selected.copy()
            permutations.append(valid_permutation)
            return
        if len(selected) + len(unselected) < depth:
            return

        temp_unselected = unselected.copy()
        for location in unselected:
            possible_permutation = selected.copy()
            possible_permutation.append(location)

            temp_unselected.remove(location)
            self.generate_permutations(permutations, temp_unselected, possible_permutation, depth)

    def find_adjacent_locations(self, location):
        all_adjacent_locations = []
        temp_location = []
        temp_location.append((location[0], location[1] + 1))
        temp_location.append((location[0] + 1, location[1] + 1))
        temp_location.append((location[0] - 1, location[1] + 1))
        temp_location.append((location[0] + 1, location[1]))
        temp_location.append((location[0] - 1, location[1]))
        temp_location.append((location[0], location[1] - 1))
        temp_location.append((location[0] + 1, location[1] - 1))
        temp_location.append((location[0] - 1, location[1] - 1))

        for location in temp_location:
            if 0 < location[0] <= self.board_length and 0 < location[1] <= self.board_length:
                all_adjacent_locations.append(location)

        return all_adjacent_locations

    def resolve_inferences(self):
        for inference_chain in self.unresolved_inferences:
            for permutation in inference_chain:
                if self.valid_flag not in permutation and self.invalid_flag not in permutation:
                    result = self.resolve_permutation(permutation)
                    if result == "Valid":
                        permutation.insert(0, self.valid_flag)
                        for other_permutation in inference_chain:
                            if self.invalid_flag not in other_permutation:
                                other_permutation.insert(0, self.invalid_flag)
                    elif result == "Invalid":
                        permutation.insert(0, self.invalid_flag)
                        counter = 0
                        possible_only_valid_permutation = None
                        for other_permutation in inference_chain:
                            if self.invalid_flag in other_permutation:
                                counter += 1
                            elif self.valid_flag not in other_permutation:
                                possible_only_valid_permutation = other_permutation

                        if counter == len(inference_chain) - 1:
                            possible_only_valid_permutation.insert(0, self.valid_flag)

        self.resolve_flags()

    def resolve_flags(self):
        for inference_chain in self.unresolved_inferences:
            if self.solved_flag not in inference_chain:
                bomb_permutation = None
                all_current_locations = {}
                for permutation in inference_chain:
                    if self.valid_flag in permutation:
                        bomb_permutation = permutation
                if bomb_permutation is not None:
                    for permutation in inference_chain:
                        for location in permutation:
                            if location is self.valid_flag or location is self.invalid_flag:
                                continue
                            if location not in bomb_permutation and location not in self.known_locations:
                                self.possible_moves.append(location)
                    for location in bomb_permutation:
                        self.add_known_bomb(location)
                    inference_chain.insert(0, self.solved_flag)

    def resolve_permutation(self, permutation):
        result = "None"
        result = self.conjunction_on_permutation(permutation)
        result = self.disjunction_on_permutation(permutation)

        return result

    def conjunction_on_permutation(self, permutation):
        counter = 0
        for location in permutation:
            if location in self.known_locations:
                if self.known_locations[location] is True:
                    counter += 1

        if counter == len(permutation):
            return "Valid"

    def disjunction_on_permutation(self, permutation):
        for location in permutation:
            if location in self.known_locations:
                if self.known_locations[location] is False:
                    return "Invalid"

    def get_move(self):
        if not self.possible_moves:
            return None
        else:
            return self.possible_moves.pop()
