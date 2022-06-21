import numpy

ROWS = 6
COLS = 7

def create_board():
    board = numpy.zeros((ROWS,COLS))
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
            if board[r][c] == piece and board[r][c+1] and board[r][c] == board[r][c+2] and board[r][c] == board[r][c+3]:
                return True

    #Check victory in all the cols
    for r in range(ROWS-3):
        for c in range(COLS):
            if board[r][c] == piece and board[r+1][c] and board[r][c] == board[r+2][c] and board[r][c] == board[r+3][c]:
                return True

    #Check diagonals
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == piece and board[r+1][c+1] and board[r][c] == board[r+2][c+2] and board[r][c] == board[r+3][c+3]:
                return True
    
    for r in range(ROWS-3):
        for c in range(COLS-3):
            if board[r][c] == piece and board[r+1][c] and board[r][c] == board[r+2][c] and board[r][c] == board[r+3][c]:
                return True

    return False 


board = create_board()

game_over = False
turn = 0

while not game_over:
    if turn == 0:
        choice = int(input("PLAYER 1 -> Select a column to play (1-7): "))
        choice -= 1
        turn -= 1

        # print(valid_location(board, choice))
        if valid_location(board, choice):
            row = row_empty(board, choice)
            play(board, row, choice, 1)
        
        if check_victory(board, 1):
            game_over = True
            print("PLAYER 1 WINS!!!")

    else:
        choice = int(input("PLAYER 2 -> Select a column to play (1-7): "))
        choice -= 1
        turn += 1

        # print(valid_location(board, choice))
        if valid_location(board, choice):
            row = row_empty(board, choice)
            # print(row)
            play(board, row, choice, 2)

        if check_victory(board, 2):
            game_over = True
            print("PLAYER 2 WINS!!!")

    print(board)