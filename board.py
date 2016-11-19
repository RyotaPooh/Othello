import sys

# Cell constants
class Cell:
	N = 0
	W = 1
	B = 2
	C = ['O', 'W', 'B']

# Player constants
class Player:
	WHITE = 1
	BLACK = 2
	PLAYER = ['NONE', 'WHITE', 'BLACK']

# Directions
# 0 1 2
# 3 x 4
# 5 6 7
class Direction:
	ROW = [-1, -1, -1, 0, 0, 1, 1, 1]
	COL = [-1, 0, 1, -1, 1, -1, 0, 1]

# Constant for the markings on the board
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
		self.curr_opponent = Player.WHITE
		self.board = [[Cell.N for i in range(size)] for i in range(size)]
		self.size = size
		self.game_ended = False

		self.board[3][3] = Cell.W
		self.board[3][4] = Cell.B
		self.board[4][3] = Cell.B
		self.board[4][4] = Cell.W

	# Make a move
	def move(self, row, col):
		# Make move if move is valid
		flanked = self.get_flanked(row, col)
		if flanked:
			# Update board
			self.board[row][col] = self.curr_player

			for i,j in flanked:
				self.board[i][j] = self.curr_player
		else:
			print("Invalid move, please try again")
			return

		self.switch_player()

		if not self.move_exist():
			self.switch_player()
			if not self.move_exist():
				self.game_ended = True
			else:
				print(self.get_opponent_string() + " player out of moves, " + self.get_player_string() + " player's turn")

	# Return True if a valid move exist, else return False
	def move_exist(self):
		for row in range(self.size):
			for col in range(self.size):
				# Check if cell is occupied
				if self.board[row][col] == Cell.N:
					# Check if move is valid for every direction
					for i in range(8):
						# Get next step
						n_row = row + Direction.ROW[i]
						n_col = col + Direction.COL[i]

						if self.out_of_bounds(n_row, n_col):
							continue

						while self.board[n_row][n_col] == self.curr_opponent:
							n_row = n_row + Direction.ROW[i]
							n_col = n_col + Direction.COL[i]

							if self.out_of_bounds(n_row, n_col):
								break

							# If a valid move exist
							if self.board[n_row][n_col] == self.curr_player:
								return True

		# If no valid move exist
		return False

	# Return flanked cells coordinates if move is valid, else return None
	def get_flanked(self, row, col):
		# Check for boundary
		if self.out_of_bounds(row, col):
			return None

		# Check if cell is occupied
		if not self.board[row][col] == Cell.N:
			return None

		flanked = []
		# Check if move is valid for every direction
		for i in range(8):
			# Get next step
			n_row = row + Direction.ROW[i]
			n_col = col + Direction.COL[i]

			if self.out_of_bounds(n_row, n_col):
				continue

			cells_passed = []
			while self.board[n_row][n_col] == self.curr_opponent:
				cells_passed += [(n_row, n_col)]
				n_row = n_row + Direction.ROW[i]
				n_col = n_col + Direction.COL[i]

				if self.out_of_bounds(n_row, n_col):
					break

				# If a valid move exist
				if self.board[n_row][n_col] == self.curr_player:
					flanked += cells_passed
					break

		# If no valid move exist
		if len(flanked) == 0:
			return None
		else:
			return flanked

	# Return true if out of boundary
	def out_of_bounds(self, row, col):
		return row < 0 or row > self.size - 1 or col < 0 or col > self.size - 1

	# Switch player
	def switch_player(self):
		self.curr_player, self.curr_opponent = self.curr_opponent, self.curr_player

	# Return the current player in string
	def get_player_string(self):
		return Player.PLAYER[self.curr_player]

	# Return the current opponent in string
	def get_opponent_string(self):
		return Player.PLAYER[self.curr_opponent]

	# Return true if game ends
	def game_end(self):
		return self.game_ended

	# Return the winner after game ends, return None if it's a tie
	def get_winner(self):
		num_white = 0
		num_black = 0

		for row in self.board:
			for cell in row:
				if cell == Cell.B:
					num_black += 1
				if cell == Cell.W:
					num_white += 1

		if num_white == num_black:
			return None
		elif num_white > num_black:
			return "WHITE"
		else:
			return "BLACK"

	# Print out the board to the console
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