import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from src.utility import place
from src.ai.function import utility_function, get_all_available_moves

from typing import Tuple, List


class Minimax:
    def __init__(self):
        self.best_score = 0
        self.best_move = None
        self.thinking_time = 3
        self.max_depth = 3

    def minimax(self, state: State, n_player: int, depth: int, isMaximizingPlayer: bool, alpha: int, beta: int):

        # Cek terminal state dengan is win dll

        if (depth == self.max_depth):
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
                child_state = State(state.board, state.players, state.round)
                selected_row = place(child_state, n_player, move[1], move[0])
                value = self.minimax(child_state, n_player, depth+1, False, alpha, beta)
                
                best_val = max(best_val, value)

                if best_val >= self.best_score:
                    self.best_move = move

                alpha = max(alpha, best_val)
                
                if (beta <= alpha):
                    break

            return best_val

        # Minimizing player
        
        else:
            best_val = 999
            available_moves = get_all_available_moves(state, n_player)

            for move in available_moves:
                child_state = State(state.board, state.players, state.round)
                selected_row = place(child_state, n_player, move[1], move[0])
                value = self.minimax(child_state, n_player, depth+1, True, alpha, beta)
                
                best_val = max(best_val, value)

                if best_val >= self.best_score:
                    self.best_move = move

                beta = min(alpha, best_val)
                
                if (beta <= alpha):
                    break

            return best_val

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        self.minimax(state, n_player, 0, True, -999, 999)
        
        return self.best_move
