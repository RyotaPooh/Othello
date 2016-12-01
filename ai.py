from random import randint
from player import Player
from board import Board
from board import Cell
from board import State
import time

class AI(Player):
	def __init__(self, name, piece):
		Player.__init__(self, name, piece)

	def is_AI(self):
		return True

class AI_Random(AI):
	def __init__(self, name, piece):
		AI.__init__(self, name, piece)

	def get_move(self, board):
		# Tuple (row, col) of all possible moves
		possible_moves = []

		for row in range(board.size):
			for col in range(board.size):
				if board.move_valid(row, col):
					possible_moves += [(row, col)]

		time.sleep(1)
		return possible_moves[randint(0, len(possible_moves) - 1)]

class AI_Greedy_First(AI):
	def __init__(self, name, piece):
		AI.__init__(self, name, piece)

	def get_move(self, board):
		# Tuple (row, col) of all possible moves
		best_move = ()
		max_flanked = 0

		for row in range(board.size):
			for col in range(board.size):
				if board.move_valid(row, col):
					flanked_piece = board.get_flanked(row, col)

					if flanked_piece:
						if max_flanked < len(flanked_piece):
							best_move = (row, col)
							max_flanked = len(flanked_piece)

		time.sleep(1)
		return best_move

class AI_Greedy_Random(AI):
	def __init__(self, name, piece):
		AI.__init__(self, name, piece)

	def get_move(self, board):
		# Array of Tuple (row, col) of all possible moves
		best_moves = []
		max_flanked = 0

		for row in range(board.size):
			for col in range(board.size):
				if board.move_valid(row, col):
					flanked_piece = board.get_flanked(row, col)

					if flanked_piece:
						if max_flanked < len(flanked_piece):
							best_moves = [(row, col)]
							max_flanked = len(flanked_piece)
						elif max_flanked == len(flanked_piece):
							best_moves += [(row, col)]

		time.sleep(1)
		return best_moves[randint(0, len(best_moves) - 1)]

class AI_Minimax(AI):
	def __init__(self, name, piece):
		AI.__init__(self, name, piece)
		self.best_cell = [(0,0), (0,7), (7,0), (7,7)]

	def get_move(self, board):
		best_move = self.first_move(board, 5)

		if not best_move:
			print("Something's wrong")

		return best_move

	def first_move(self, board, max_depth):
		# Loop through all possible moves
		max_score = -10000
		best_move = None

		for row in range(board.size):
			for col in range(board.size):
				if board.move_valid(row, col):
					new_board = Board(board=board)
					state = new_board.move(row, col)

					if state == State.OUT_OF_MOVE:
						score = self.max_move(new_board, max_depth, 1)
					else:
						score = self.min_move(new_board, max_depth, 1)

					if score > max_score:
						max_score = score
						best_move = (row, col)

		return best_move

	def max_move(self, board, max_depth, curr_depth):
		if curr_depth >= max_depth or board.game_end():
			return self.evaluation(board)

		# Loop through all possible moves
		max_score = -10000
		for row in range(board.size):
			for col in range(board.size):
				if board.move_valid(row, col):
					new_board = Board(board=board)
					state = new_board.move(row, col)

					if state == State.OUT_OF_MOVE:
						score = self.max_move(new_board, max_depth, curr_depth + 1)
					else:
						score = self.min_move(new_board, max_depth, curr_depth + 1)

					if score > max_score:
						max_score = score

		return max_score

	def min_move(self, board, max_depth, curr_depth):
		if curr_depth >= max_depth or board.game_end():
			return self.evaluation(board)

		# Loop through all possible moves
		min_score = 10000
		for row in range(board.size):
			for col in range(board.size):
				if board.move_valid(row, col):
					new_board = Board(board=board)
					state = new_board.move(row, col)

					if state == State.OUT_OF_MOVE:
						score = self.min_move(new_board, max_depth, curr_depth + 1)
					else:
						score = self.max_move(new_board, max_depth, curr_depth + 1)

					if score < min_score:
						min_score = score

		return min_score

	def evaluation(self, board):
		score = 0

		for row in board.board:
			for cell in row:
				if cell == self.piece:
					score += 1
				elif cell != Cell.N:
					score -= 1

		for coord in self.best_cell:
			curr_piece = board.board[coord[0]][coord[1]]
			if curr_piece == self.piece:
				score += 15
			elif curr_piece != Cell.N:
				score -= 15

		return score