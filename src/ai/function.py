from src.model import Piece, Board, State
from src.constant import ShapeConstant, ColorConstant, GameConstant
from utility import place, is_out

def utility_function(state: State, col: int, shape: str):
    """
    [DESC]
        Function evaluate current board state
    [PARAMS]
        state: State -> current state in the game
        col: int -> column
        shape: shape -> chosen shape to be placed
    [RETURN]
        Arbitrary value of board state, the higher the better
    """
    
    # check current player
    n_player = (state.round - 1) % 2
    if n_player == 1:
        player_shape, player_color = GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR
        # enemy_shape, enemy_color = GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR
    else:
        player_shape, player_color = GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR
        # enemy_shape, enemy_color = GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR

    # Place current shape in the board
    selected_row = place(state, n_player, shape, col)
    
    streak_way = [(-1, 0), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    utility_value = 0
    
    for row_ax, col_ax in streak_way:        
        row_, col_ = selected_row, col
        shape_value = 0
        color_value = 0

        for i in range(GameConstant.N_COMPONENT_STREAK):
            if is_out(state.board, row_, col_):
                break

            if (state.board[row_,col_].shape != ShapeConstant.BLANK):
                if (state.board[row_,col_].shape == player_shape):
                    shape_value += 1
                else:
                    shape_value -= 1
                    
                if (state.board[row_,col_].color == player_color):
                    color_value += 1
                else:
                    color_value -= 1

            row_ += row_ax
            col_ += col_ax

        max_value = max(shape_value, color_value)
        if (utility_value < max_value):
            utility_value = max_value
        
    # Undo the move
    state.board[selected_row, col] = Piece(ShapeConstant.BLANK, ColorConstant.BLACK)
    
    return utility_value