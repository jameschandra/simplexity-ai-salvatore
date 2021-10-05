import random
import math
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.ai.function import utility_function, get_all_available_moves

from typing import Tuple, List

class LocalSearch:
    def __init__(self):
        self.thinking_time = 3
        self.threshold_time = 0.1
        pass

    # def schedule(self, current_thinking_time_elapsed): 
    #     if (self.thinking_time - current_thinking_time_elapsed) < self.remaining_time_threshold:
    #         return 0
    #     return self.max_temp * (self.thinking_time - current_thinking_time_elapsed)

    def generate_random(self, all_available_moves):
        move = random.choice(all_available_moves)
        all_available_moves.remove(move)
        return move

    def stochastic_hill_climbing(self, state: State, n_player: int):
        all_available_moves = get_all_available_moves(state, n_player)
        current_move = self.generate_random(all_available_moves)
        current_value = utility_function(state, n_player, current_move[0], current_move[1])        
        start_time = time()
        
        while True:
            t = time() - start_time
            if (t >= self.thinking_time - self.threshold_time):
                return current_move
            if (len(all_available_moves) == 0):
                return current_move
            next_move = self.generate_random(all_available_moves)
            next_value = utility_function(state, n_player, next_move[0], next_move[1])
            E = next_value - current_value
            if (E > 0):
                current_move = next_move
                current_value = next_value 

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = thinking_time

        return self.stochastic_hill_climbing(state, n_player)