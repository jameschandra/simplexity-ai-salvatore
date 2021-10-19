from src.utility import *

import random
import math
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.ai.function import utility_function, get_all_available_moves

from typing import Tuple, List

class LocalSearchGroup6:
    def __init__(self):
        self.thinking_time = 3
        self.threshold_time = 0.1

    def generate_random(self, all_available_moves):
        move = random.choice(all_available_moves)
        all_available_moves.remove(move)
        return move

    # def stochastic_hill_climbing(self, state: State, n_player: int):
    #     all_available_moves = get_all_available_moves(state, n_player)
    #     current_move = self.generate_random(all_available_moves)
    #     current_value = utility_function(state, n_player, current_move[0], current_move[1])        
    #     start_time = time()
        
    #     while True:
    #         t = time() - start_time
    #         if (t >= self.thinking_time - self.threshold_time):
    #             return current_move
    #         if (len(all_available_moves) == 0):
    #             return current_move
    #         next_move = self.generate_random(all_available_moves)
    #         next_value = utility_function(state, n_player, next_move[0], next_move[1])
    #         E = next_value - current_value
    #         if (E > 0):
    #             current_move = next_move
    #             current_value = next_value
    
    def find_highest_value_successor(self, state, n_player, all_successors):
        successor_move = all_successors[0]
        highest_value = utility_function(state, n_player, successor_move[0], successor_move[1])
        for i in range(1, len(all_successors)):
            next_value = utility_function(state, n_player, all_successors[i][0], all_successors[i][1])
            if (next_value > highest_value):
                successor_move = all_successors[i]
                highest_value = next_value
        return (successor_move, highest_value)
    

    def hill_climbing(self, state: State, n_player: int):
        start_time = time()
        all_available_moves = get_all_available_moves(state, n_player)
        current_move = self.generate_random(all_available_moves)
        current_value = utility_function(state, n_player, current_move[0], current_move[1])
        while True:
            t = time() - start_time
            if (t >= self.thinking_time - self.threshold_time):
                return current_move
            neighbor_move, neighbor_value = self.find_highest_value_successor(state, n_player, all_available_moves)
            if (neighbor_value <= current_value):
                return current_move
            current_move = neighbor_move
            current_value = neighbor_value

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = thinking_time

        return self.hill_climbing(state, n_player)