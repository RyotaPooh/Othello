#!/usr/bin/env python3
from board import Board
from board import Mark
from board import State

def start():
	print("\nGAME START: ")
	print("Input the board position to make your move: ")
	print("Eg: a1, b5, f6")
	print("'q' or 'quit' to end game\n")

# Return a tuple (row, col) of the move to be made, Return None if player input 'q' or 'quit' to end game
def get_move(board):
	while True:
		print(board)
		move = board.get_player().get_move(board)

		# AI
		if board.get_player().is_AI():
			return move

		# Player
		if move.lower() == 'quit' or move.lower() == 'q':
			print("GAME END")
			return None
		else:
			if check_input(move):
				return (int(move[1]) - 1, Mark.IDX[move[0]])
			else:
				print("BAD INPUT!! " + str(board.get_player()) + " try again")


# Return False for bad input and True for correct input
def check_input(move):
	# Check for bad move input
	if not len(move) == 2:
		return False
	try:
		if not move[0] in Mark.COL or int(move[1]) < 1 or int(move[1]) > 8:
			return False
	except ValueError:
		return False
	return True

# For console output when ending the game
def end_game(board):
	print(board)
	print("GAME END, WINNER IS " + str(board.get_winner()))

def main(size, player1, player2):
	# Generate board
	board = Board("Othello", size, player1, player2)
	start()

	# Game loop
	while not board.game_end():
		# Get the move
		move = get_move(board)

		# End game if user quit the game
		if not move:
			return

		# Make the move
		state = board.move(move[0], move[1])

		# Check if move is valid
		if state == State.INVALID_MOVE:
			print("Invalid move, please try again")
		elif state == State.OUT_OF_MOVE:
			print(str(board.get_opponent()) + " out of moves, " + str(board.get_player()) + "'s turn")

	# Ending game with a winner
	end_game(board)
