import numpy as np
import random
import math

ROWS = 6
COLS = 7
PLAYER1_PIECE = 1
PLAYER2_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROWS,COLS))
    return board

def play(board, row, col, piece):
    board[row][col] = piece

def valid_location(board, col):
    '''Return True if the column is valid to play'''
    if board[0][col] == 0:
        return True
    return False

def row_empty(board, col):
    '''Return the row which the player can drop the piece'''
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def check_victory(board, piece):
    #Check victory in all the rows
    for r in range(ROWS):
        for c in range(COLS-3):
            if board[r][c] == piece and board[r][c] == board[r][c+1] and board[r][c] == board[r][c+2] and board[r][c] == board[r][c+3]:
                return True

    #Check victory in all the cols
    for r in range(ROWS-3):
        for c in range(COLS):
            if board[r][c] == piece and board[r][c] == board[r+1][c] and board[r][c] == board[r+2][c] and board[r][c] == board[r+3][c]:
                return True

    #Check diagonals
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == piece and board[r][c] == board[r+1][c+1] and board[r][c] == board[r+2][c+2] and board[r][c] == board[r+3][c+3]:
                return True
    
    for r in range(3, ROWS):
        for c in range(COLS-3):
            if board[r][c] == piece and board[r][c] == board[r-1][c+1] and board[r][c] == board[r-2][c+2] and board[r][c] == board[r-3][c+3]:
                return True

    return False  

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER1_PIECE
	if piece == PLAYER1_PIECE:
		opp_piece = PLAYER2_PIECE

	if window.count(piece) == 4:
		score += 100
	elif np.logical_and(window.count(piece) == 3, window.count(EMPTY) == 1):
		score += 5
	elif np.logical_and(window.count(piece) == 2, window.count(EMPTY) == 2):
		score += 2

	if np.logical_and(window.count(opp_piece) == 3, window.count(EMPTY) == 1):
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROWS):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLS-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLS):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROWS-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROWS-3):
		for c in range(COLS-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROWS-3):
		for c in range(COLS-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return check_victory(board, PLAYER1_PIECE) or check_victory(board, PLAYER2_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if check_victory(board, PLAYER2_PIECE):
				return (None, 100000000000000)
			elif check_victory(board, PLAYER1_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, PLAYER2_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = row_empty(board, col)
			b_copy = board.copy()
			play(b_copy, row, col, PLAYER2_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = row_empty(board, col)
			b_copy = board.copy()
			play(b_copy, row, col, PLAYER1_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLS):
		if valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = row_empty(board, col)
		temp_board = board.copy()
		play(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col


if __name__ == '__main__':
    board = create_board()

    game_over = False
    while not game_over:

        finish = input("Would you like to know the best move for the PLAYER1? ")
        if finish in 'Yy':
            col, minimax_score = minimax(board, 7, -math.inf, math.inf, False)
            print(f"The best column to you play is {col+1}")
            
        choice = int(input("PLAYER 1 -> Select a column to play (1-7): "))
        choice -= 1
        
        if valid_location(board, choice):
            row = row_empty(board, choice)
            play(board, row, choice, 1)
            print(board)
        
        if check_victory(board, 1):
            game_over = True
            print("PLAYER 1 WINS!!!")
            break


        finish = input("Would you like to know the best move for the PLAYER2? ")
        if finish in 'Yy':
            col, minimax_score = minimax(board, 7, -math.inf, math.inf, True)
            print(f"The best column to you play is {col+1}")

        choice = int(input("PLAYER 2 -> Select a column to play (1-7): "))
        choice -= 1
        

        if valid_location(board, choice):
            row = row_empty(board, choice)
            play(board, row, choice, 2)
            print(board)

        if check_victory(board, 2):
            game_over = True
            print("PLAYER 2 WINS!!!")
            break
