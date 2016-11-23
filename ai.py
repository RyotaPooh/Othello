from random import randint

class AI_Random:
	def __init__(self, name, piece):
		self.name = name
		self.piece = piece

	def get_move(self, board):
		# Tuple (row, col) of all possible moves
		possible_moves = []

		for row in range(board.size):
			for col in range(board.size):
				if board.move_valid(row, col):
					possible_moves += [(row, col)]

		return possible_moves[randint(0, len(possible_moves) - 1)]

	def is_AI(self):
		return True

	def get_piece(self):
		return self.piece

	def __str__(self):
		return self.name