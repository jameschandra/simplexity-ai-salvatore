import random
import math
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.ai.function import utility_function, get_all_available_moves

from typing import Tuple, List

class LocalSearch:
    def __init__(self):
        pass

    def schedule(self, current_thinking_time_elapsed):
        max_thinking_time = 3
        max_temp = 50
        remaining_time_threshold = 0.001
        if (max_thinking_time - current_thinking_time_elapsed) < remaining_time_threshold:
            return 0
        
        return max_temp * (max_thinking_time - current_thinking_time_elapsed)

    def generate_random(self, all_available_moves):
        move = random.choice(all_available_moves)
        all_available_moves.remove(move)
        return move

    def simulated_annealing(self, state: State, n_player: int):
        all_available_moves = get_all_available_moves(state, n_player)
        current_move = self.generate_random(all_available_moves)
        current_value = utility_function(state, n_player, current_move[0], current_move[1])        
        start_time = time()
        
        while True:
            t = time() - start_time
            T = self.schedule(t)
            if T == 0:
                return current_move
            next_move = self.generate_random(all_available_moves)
            next_value = utility_function(state, n_player, next_move[0], next_move[1])
            E = next_value - current_value
            if (E > 0):
                current_move = next_move
                current_value = next_value
            else:
                X = 0.5
                if ((math.e ** E) / T) > X:
                    current_move = next_move
                    current_value = next_value   

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        return self.simulated_annealing(state, n_player)

    # function simulated_annealing(problem, schedule) → solution_state
    #     // Mengembalikan solution state berdasarkan problem dan schedule
    #     current ← make_node(problem.initial_state)
    #     start_time ← get_current_time()
    #     while true do
    #         t ← get_current_time() - start_time
    #         T ← schedule(t)
    #         if (T = 0) then
    #             → current
    #         next ← get_random_successor(current)
    #         E ← next.value - current.value
    #         if (E > 0) then
    #             current ← next
    #         else
    #             if (eE/T> X) then
    #                 current ← next

    # function schedule(current_thinking_time_elapsed) → temperature
    #     // Mengembalikan temperatur berdasarkan input waktu
    #     max_thinking_time ← 4
    #     max_temp ← 50
    #     // Mengantisipasi waktu berpikir sudah habis sebelum iterasi berakhir
    #     if (4 - current_thinking_time_elapsed) very close to 0
    #         → 0
    #     → max_temp * (max_thinking_time - current_thinking_time_elapsed)