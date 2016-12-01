import sys

class State:
	INVALID_MOVE = -1
	OUT_OF_MOVE = -2

# Cell constants
class Cell:
	N = 0
	W = 1
	B = 2
	C = ['O', 'W', 'B']

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
	def __init__(self, name="Othello", size=8, player1=None, player2=None, board=None):
		if not size == 8:
			print("Size of the board has to be eight for now")
			sys.exit(1)

		if board:
			self.name = board.name
			self.player_black = board.player_black
			self.player_white = board.player_white
			self.curr_player = board.curr_player
			self.curr_opponent = board.curr_opponent
			self.board = [i[:] for i in board.board]
			self.size = board.size
			self.game_ended = board.game_ended
			return

		if not player1 or not player2:
			print("Error: Invalid Player")

		self.name = name
		self.player_black = player1
		self.player_white = player2
		self.curr_player = player1
		self.curr_opponent = player2
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
			self.board[row][col] = self.curr_player.get_piece()

			for i,j in flanked:
				self.board[i][j] = self.curr_player.get_piece()
		else:
			return State.INVALID_MOVE

		self.switch_player()

		if not self.move_exist():
			self.switch_player()
			if not self.move_exist():
				self.game_ended = True
			else:
				return State.OUT_OF_MOVE

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

						while self.board[n_row][n_col] == self.curr_opponent.get_piece():
							n_row = n_row + Direction.ROW[i]
							n_col = n_col + Direction.COL[i]

							if self.out_of_bounds(n_row, n_col):
								break

							# If a valid move exist
							if self.board[n_row][n_col] == self.curr_player.get_piece():
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
			while self.board[n_row][n_col] == self.curr_opponent.get_piece():
				cells_passed += [(n_row, n_col)]
				n_row = n_row + Direction.ROW[i]
				n_col = n_col + Direction.COL[i]

				if self.out_of_bounds(n_row, n_col):
					break

				# If a valid move exist
				if self.board[n_row][n_col] == self.curr_player.get_piece():
					flanked += cells_passed
					break

		# If no valid move exist
		if len(flanked) == 0:
			return None
		else:
			return flanked

	# Return true if move is valid
	def move_valid(self, row, col):
		# Check if cell is occupied
		if self.board[row][col] == Cell.N:
			# Check if move is valid for every direction
			for i in range(8):
				# Get next step
				n_row = row + Direction.ROW[i]
				n_col = col + Direction.COL[i]

				if self.out_of_bounds(n_row, n_col):
					continue

				while self.board[n_row][n_col] == self.curr_opponent.get_piece():
					n_row = n_row + Direction.ROW[i]
					n_col = n_col + Direction.COL[i]

					if self.out_of_bounds(n_row, n_col):
						break

					# If a valid move exist
					if self.board[n_row][n_col] == self.curr_player.get_piece():
						return True

		# If no valid move exist
		return False

	# Return true if out of boundary
	def out_of_bounds(self, row, col):
		return row < 0 or row > self.size - 1 or col < 0 or col > self.size - 1

	# Switch player
	def switch_player(self):
		self.curr_player, self.curr_opponent = self.curr_opponent, self.curr_player

	# Return the current player
	def get_player(self):
		return self.curr_player

	# Return the current opponent
	def get_opponent(self):
		return self.curr_opponent

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
			return self.player_white
		else:
			return self.player_black

	# Return the board
	def get_board(self):
		return self.board

	# For printing out the board
	def __str__(self):
		string = "\n  "

		for i in Mark.COL:
			string += str(i) + " "
		string += "\n"

		row = 1
		for i in self.board:
			string += str(row) + " "
			row += 1

			for j in i:
				string += Cell.C[j] + " "

			string += "\n"
		string += "\n"

		return string