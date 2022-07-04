# from connect4 import *
import pygame
import sys
import math
import numpy as np
import pygame_menu
import random

####################                CONSTANTS AND GLOBAL VARIABLES              ####################
ROWS = 6
COLS = 7

BLUE = (0,0,255)
BLACK = (0,0,0)
LAWNGRENN = (124,252,0)
DEEPPINK = (255,20,147)
WHITE = (255, 255, 255)
THISTLE = (216,191,216)
PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

SQUARESIZE = 100

width = COLS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

DIFFICULTY = [5]

####################                AI - ALGORITHM MINIMA               ####################
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

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
    return check_victory(board, PLAYER_PIECE) or check_victory(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if check_victory(board, AI_PIECE):
                return (None, 100000000000000)
            elif check_victory(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = row_empty(board, col)
            b_copy = board.copy()
            play(b_copy, row, col, AI_PIECE)
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
            play(b_copy, row, col, PLAYER_PIECE)
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


####################                FUNCTIONS FOR THE BASIC GAME                ####################
def valid_location(board, col):
    '''Return True if the column is valid to play'''
    #print(col)
    #print(f"{board[0][col]} Verificando")
    if board[0][col] == 0:
        return True
    return False

def row_empty(board, col):
    '''Return the row which the player can drop the piece'''
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def play(board, row, col, piece):
    board[row][col] = piece

def check_victory(board, piece):
    # Check victory in all the rows
	for c in range(COLS-3):
		for r in range(ROWS):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check victory in all the cols
	for c in range(COLS):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check diagonals
	for c in range(COLS-3):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	for c in range(COLS-3):
		for r in range(3, ROWS):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
    
class Game:
    def __init__(self):
        self.initialize_menu()


    ####################                MENU                ####################
    def initialize_menu(self):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 75)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Connect 4")
        self.screen.fill("white")
        self.menu = pygame_menu.Menu('Welcome', 700, 700, theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.text_input('Name: ', default='Monkey')
        self.menu.add.selector('Difficulty: ', [('Normal', 5), ('Hard', 7)], onchange=self.set_difficulty)
        self.menu.add.button('Play vs AI', self.initGameAI)
        self.menu.add.button('Play vs Friend', self.initGameFriend)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.mainloop(self.screen)

    
    def initialize_game(self):
        self.board = np.zeros((ROWS,COLS))
        self.gameOver = False 
        self.turn = 0
        self.drawBoard()

    
    def set_difficulty(self, value, difficulty):
        DIFFICULTY[0] = difficulty


    def initGameAI(self):
        self.initialize_game()
        self.runGameAI()


    def initGameFriend(self):
        self.initialize_game()
        self.runGameFriend()


    #Draws the game board with black circle for empty position
    #                           red circle for player1 chip
    #                           yellow circle for player2 (AI)
    def drawBoard(self):
        for r in range(ROWS):
            for c in range(COLS):
                pygame.draw.rect(self.screen, THISTLE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                # Player chip
                if self.board[r, c] == PLAYER_PIECE:
                    pygame.draw.circle(self.screen, LAWNGRENN, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
                # AI chip
                elif self.board[r, c] == AI_PIECE:
                    pygame.draw.circle(self.screen, DEEPPINK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
                # Empty spot
                else:
                    pygame.draw.circle(self.screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

        pygame.display.update()


    # Displays chip when player moves mouse on mouse position
    def move_chip(self, color, position):
        pygame.draw.rect(self.screen, WHITE, (0,0, width, SQUARESIZE))
        pygame.draw.circle(self.screen, color, (position, int(SQUARESIZE/2)), RADIUS)
        # Refresh only the of the screen (where the chip is moving)
        pygame.display.update(0, 0, width, SQUARESIZE)


    # Checks the position and drop the piece corresponding to the player
    def dropPiece(self, player, column, color):
        if valid_location(self.board, column):
            row = row_empty(self.board, column)
            play(self.board, row, column, player)
            if check_victory(self.board, player):
                self.gameOver = True
                label = self.font.render(f"Player {player} wins!!", 1, color)
                self.screen.blit(label, (40, 10))

            self.turn += 1
            self.turn %= 2

            #print(self.board)
            self.drawBoard()


    def runGameFriend(self):
        count_turns = 0
        while not self.gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    if self.turn == PLAYER:
                        self.move_chip(LAWNGRENN, posx)

                    else:
                        self.move_chip(DEEPPINK, posx)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = int(math.floor(event.pos[0] / SQUARESIZE))
                    if self.turn == PLAYER:
                        self.dropPiece(PLAYER_PIECE, col, LAWNGRENN)
                    else:
                        self.dropPiece(AI_PIECE, col, DEEPPINK)
                    count_turns += 1
                
                if count_turns == 42 and self.gameOver != True:
                    label = self.font.render(f"Match is DRAW!!", 1, BLACK)
                    self.screen.blit(label, (40, 10))
                    self.drawBoard()
                    self.gameOver = True

            if self.gameOver:
                pygame.time.wait(5000)
       

    def runGameAI(self, difficulty=DIFFICULTY[0]):
        count_turns = 0
        while not self.gameOver:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    posx = event.pos[0]
                    if self.turn == PLAYER:
                        self.move_chip(LAWNGRENN, posx)


                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, WHITE, (0,0, width, SQUARESIZE))
                    #print(event.pos)
                    # Ask for Player 1 Input
                    if self.turn == PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        self.dropPiece(PLAYER_PIECE, col, LAWNGRENN)
                        count_turns += 1
                        

            # # Ask for Player 2 Input
            if self.turn == AI and not self.gameOver:               

                #col = random.randint(0, COLUMN_COUNT-1)
                #col = pick_best_move(board, AI_PIECE)
                #print(difficulty)
                col, minimax_score = minimax(self.board, difficulty, -math.inf, math.inf, True)

                self.dropPiece(AI_PIECE, col, DEEPPINK)
                count_turns += 1
                
            if count_turns == 42 and self.gameOver != True:
                    label = self.font.render(f"Match is DRAW!!", 1, BLACK)
                    self.screen.blit(label, (40, 10))
                    self.drawBoard()
                    self.gameOver = True
        
            if self.gameOver:
                pygame.time.wait(5000)
            
game = Game()
