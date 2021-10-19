from src.utility import *

import random
import copy
from time import time

from src.constant import ShapeConstant
from src.model import State

from src.utility import place, is_win
from src.ai.function import utility_function, get_all_available_moves

from typing import Tuple, List

class MinimaxGroup6:
    def __init__(self):
        self.max_depth = 5
        self.scores = []
        self.moves = []
        self.best_score = -999
        self.best_move = None
        self.start_time = 0
        self.thinking_time = 3
        self.threshold_time = 0.1

    def minimax(self, state: State, n_player: int, depth: int, isMaximizingPlayer: bool, alpha: int, beta: int):
        t = time() - self.start_time
        if (t >= self.thinking_time - self.threshold_time):
            return 0
        
        winner = is_win(state.board)
        if winner and winner[0] == state.players[n_player].shape and winner[1] == state.players[n_player].color:
            return 99999999
        
        if winner and winner[0] != state.players[n_player].shape and winner[1] != state.players[n_player].color:
            return -99999999

        if (depth == self.max_depth - 1):
            max_value = 0
            
            for col in range(state.board.col):
                for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                    if (state.players[n_player].quota[shape] != 0):
                        current_val = utility_function(state, n_player, col, shape)
                        max_value = max(current_val, max_value)
            
            return max_value
        
        # Maximizing player

        if (isMaximizingPlayer):
            best_val = -999
            available_moves = get_all_available_moves(state, n_player)
            for move in available_moves:
                child_state = copy.deepcopy(state)

                selected_row = place(child_state, n_player, move[1], move[0])
                value = self.minimax(child_state, n_player, depth+1, False, alpha, beta)
                
                best_val = max(best_val, value)

                if best_val >= self.best_score:
                    self.scores.append(best_val)
                    self.moves.append(move)
                    self.best_score = best_val
                    self.best_move = move

                alpha = max(alpha, best_val)
                
                if (beta <= alpha):
                    break

            if n_player == 0:
                n_player = 1
            else:
                n_player = 0

            return best_val

        # Minimizing player
        
        else:
            worst_val = 999
            available_moves = get_all_available_moves(state, n_player)

            for move in available_moves:
                child_state = copy.deepcopy(state)

                selected_row = place(child_state, n_player, move[1], move[0])
                value = self.minimax(child_state, n_player, depth+1, True, alpha, beta)
                
                worst_val = min(worst_val, value)

                beta = min(beta, worst_val)
                
                if (beta <= alpha):
                    break

            if n_player == 0:
                n_player = 1
            else:
                n_player = 0

            return worst_val

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.scores = []
        self.moves = []
        self.best_score = -999
        self.best_move = None

        self.start_time = time()
        self.thinking_time = thinking_time

        self.minimax(state, n_player, 0, True, -999, 999)

        available_moves = []

        for i in range(len(self.scores)):
            if (self.scores[i] == self.best_score):
                available_moves.append(self.moves[i])

        selected_move = available_moves[random.randint(0, len(available_moves)-1)]

        # print(self.best_score)
        # print(selected_move)
        return selected_move
