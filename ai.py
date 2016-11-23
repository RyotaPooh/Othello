from random import randint
from player import Player

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

		return best_moves[randint(0, len(best_moves) - 1)]
