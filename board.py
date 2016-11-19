import sys

class Cell:
	N = 0
	W = 1
	B = 2
	C = ['O', 'W', 'B']

class Player:
	WHITE = 1
	BLACK = 2
	PLAYER = ['NONE', 'WHITE', 'BLACK']

class Mark:
	COL = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	IDX = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

class Board:
	def __init__(self, name, size):
		if not size == 8:
			print("Size of the board has to be eight for now")
			sys.exit(1)

		self.name = name
		self.player = []
		self.curr_player = Player.BLACK
		self.board = [[Cell.N for i in range(size)] for i in range(size)]

		self.board[3][3] = Cell.W
		self.board[3][4] = Cell.B
		self.board[4][3] = Cell.B
		self.board[4][4] = Cell.W

	def move(self, row, col):
		self.board[row][col] = self.curr_player
		self.switch_player()

	def switch_player(self):
		if self.curr_player == Player.WHITE:
			self.curr_player = Player.BLACK
		else:
			self.curr_player = Player.WHITE

	def get_player(self):
		return Player.PLAYER[self.curr_player]

	def game_end(self):
		return False

	def get_winner(self):
		return Player.PLAYER[self.curr_player]

	def render(self):
		print("\n  ", end='')
		for i in Mark.COL:
			print(i + " ", end='')
		print()

		row = 1
		for i in self.board:
			print(str(row) + " ", end='')
			row += 1

			for j in i:
				print(Cell.C[j] + " ", end='')

			print()
		print()