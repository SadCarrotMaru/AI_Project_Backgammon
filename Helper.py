import backgammon as backgammon
import copy

class Virtual_App():
    def __init__(self):
        self.Virtual = backgammon.Application()


    def craft_state(self, state, position, destination):
        crafted_state = copy.deepcopy(state)
        piece_color = crafted_state[position][0]
        if destination != 0 and destination != 25:
            if len(crafted_state[destination]) == 1 and crafted_state[destination][0] != crafted_state[position][0]:
                if crafted_state[destination][0] == 'W':
                    crafted_state[25].append('W')
                else:
                    crafted_state[0].append('B')
                
                crafted_state[destination] = []

        crafted_state[position] = crafted_state[position][:-1]
        if destination > 0 and destination < 25: crafted_state[destination].append(piece_color)
        
        #print(f"{position} --> {destination} --> {state[position][0]} -->  {state} crafted state --> {crafted_state}" )
        return crafted_state

    def get_states_for_move(self, current_state):
        states = []
        for i in range(0,26):
            possible_moves = self.Virtual.get_moves_for_position(i)
            for move in possible_moves:
                future_state = self.craft_state(current_state, i, move)
                states.append(future_state)
        return states
    
    def get_states_for_roll(self, current_state, turn, roll):
        self.Virtual.switch_game_status(current_state, turn, [roll])
        return self.get_states_for_move(current_state)


    def get_all_moves(self, current_state, turn, rolls): ## NEED TO REMOVE DUPLICATES
        if len(rolls) == 4:
            possible_states_initial = [current_state]
            possible_states = []
            for roll in rolls:
                for state in possible_states_initial:
                    possible_states.extend(self.get_states_for_roll(state, turn, roll))
                if len(possible_states) == 0:
                    possible_states = possible_states_initial
                possible_states_initial = possible_states
                possible_states = []
            unique_possible_states = []
            [unique_possible_states.append(x) for x in possible_states_initial if x not in unique_possible_states]
            return unique_possible_states
        else:
            possible_states_initial_1 = [current_state]
            possible_states_initial_2 = [current_state]
            possible_states_2 = []
            possible_states_1 = []
            rolls_used_1 = 0
            rolls_used_2 = 0
            rolls_2 = copy.deepcopy(rolls)
            rolls_2.reverse()
            for roll in rolls:
                for state in possible_states_initial_1:
                    possible_states_1.extend(self.get_states_for_roll(state, turn, roll))
                if len(possible_states_1) == 0:
                    possible_states_1 = possible_states_initial_1
                else:
                    rolls_used_1 += 1
                possible_states_initial_1 = possible_states_1
                possible_states_1 = []
            for roll in rolls_2:
                for state in possible_states_initial_2:
                    possible_states_2.extend(self.get_states_for_roll(state, turn, roll))
                if len(possible_states_2) == 0:
                    possible_states_2 = possible_states_initial_2
                else:
                    rolls_used_2 += 1
                possible_states_initial_2 = possible_states_2
                possible_states_2 = []
            
            if rolls_used_1 == rolls_used_2:
                possible_states_initial_1.extend(possible_states_initial_2)
            elif rolls_used_2 > rolls_used_1:
                possible_states_initial_1 = possible_states_initial_2
            unique_possible_states = []
            [unique_possible_states.append(x) for x in possible_states_initial_1 if x not in unique_possible_states]
            return unique_possible_states

