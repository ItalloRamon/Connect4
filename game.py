from connect4 import *
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)



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


class Game:
	def __init__(self):
		self.initialize()


	def initialize(self):
		self.board = board = np.zeros((ROWS,COLS))
		pygame.init()
		self.screen = pygame.display.set_mode(size)
		self.font = pygame.font.SysFont("monospace", 75)
		self.gameOver = False
		self.drawBoard()
		self.turn = 0

	# Draws the game board with black circle for empty position
	#							red circle for player1 chip
	#							yellow circle for player2 (AI)
	def drawBoard(self):
		for r in range(ROWS):
			for c in range(COLS):
				pygame.draw.rect(self.screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
				# Player chip
				if self.board[r, c] == PLAYER_PIECE:
					pygame.draw.circle(self.screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
				# AI chip
				elif self.board[r, c] == AI_PIECE:
					pygame.draw.circle(self.screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
				# Empty spot
				else:
					pygame.draw.circle(self.screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

		pygame.display.update()


	# Checks the position and drop the piece corresponding to the player
	def dropPiece(self, player, column, color):
		if valid_location(self.board, column):
			row = row_empty(self.board, column)
			play(self.board, row, column, player)
			if check_victory(self.board, player):
				self.game_over = True
				label = self.font.render(f"Player {player} wins!!", 1, color)
				self.screen.blit(label, (40, 10))

			self.turn += 1
			self.turn %= 2

			print(self.board)
			self.drawBoard()


	def runGame(self):
		while not self.gameOver:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					col = int(math.floor(event.pos[0] / SQUARESIZE))
					if self.turn == PLAYER:
						self.dropPiece(PLAYER_PIECE, col, RED)

					else:
						self.dropPiece(AI_PIECE, col, YELLOW)

game = Game()
game.runGame()
