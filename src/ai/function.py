from src.model import Piece, Board, State
from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.utility import place, is_out

def utility_function(state: State, n_player: int, col: int, shape: str):
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
    
    # store player's shape and color to player_shape and player_color
    if n_player == 0:
        player_shape, player_color = GameConstant.PLAYER1_SHAPE, GameConstant.PLAYER1_COLOR
    else:
        player_shape, player_color = GameConstant.PLAYER2_SHAPE, GameConstant.PLAYER2_COLOR

    # place current shape in the board
    currQuota = state.players[n_player].quota[shape]
    selected_row = place(state, n_player, shape, col)
    
    # streak way is the possible way to obtain a streak
    streak_way = [(-1, 0), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    # initialization of utility function
    utility_value = 0
    
    # check all of the streak in every way possible (min=1 streak and max=4 streak)
    for row_ax, col_ax in streak_way:        
        row_, col_ = selected_row, col
        # shape_value is the value that is deducted form the shape and
        # color_value is the value that is deducted from the color
        shape_value = 0
        color_value = 0

        for i in range(GameConstant.N_COMPONENT_STREAK):
            # place not in the board   
            if is_out(state.board, row_, col_):
                break

            # if spot is not empty
            if (state.board[row_,col_].shape != ShapeConstant.BLANK):
                # +2 if spot is occupied by player's shape
                if (state.board[row_,col_].shape == player_shape):
                    shape_value += 2
                # -2 if spot is occupied by enemy's shape
                else:
                    shape_value -= 2
                    
                # +1 if spot is occupied by player's color
                if (state.board[row_,col_].color == player_color):
                    color_value += 1
                # +1 if spot is occupied by enemy's color
                else:
                    color_value -= 1

            # next element
            row_ += int(row_ax)
            col_ += int(col_ax)

        # current_value is the cummulative value of shape and color value
        current_value = shape_value + color_value
        # takes the maximum value that can be obtained from all the possible streak (max. 4 streak)
        if (utility_value < current_value):
            utility_value = current_value
        
    # Undo the move
    state.board.set_piece(selected_row, col, Piece(ShapeConstant.BLANK, ColorConstant.BLACK))
    state.players[n_player].quota[shape] = currQuota
    
    return utility_value

def get_all_available_moves(state: State, n_player: int):
    """
    Return all possible moves for n_player in list of tuples (col, shape)
    """
    available_moves = []
    available_columns = []
    
    for col in range(state.board.col):
        if (state.board[0,col].shape == ShapeConstant.BLANK):
            available_columns.append(col)
    
    available_shapes = []

    for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
        if (state.players[n_player].quota[shape] != 0):
            available_shapes.append(shape)
    
    for col in available_columns:
        for shape in available_shapes:
            available_moves.append((col, shape))

    return available_moves