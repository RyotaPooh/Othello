class Player:
	def __init__(self, name, piece):
		self.name = name
		self.piece = piece

	def get_move(self, board):
		return input(self.name + "'s turn: ")

	def get_piece(self):
		return self.piece

	def is_AI(self):
		return False

	def is_this_player(self, name):
		return name == self.name

	def __str__(self):
		return self.name