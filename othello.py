#!/usr/bin/env python3
from board import Board
from board import Mark

def main():
	# Generate board
	board = Board("Othello", 8)
	board.render()

	print("\nGAME START: ")
	print("Input the board position to make your move: ")
	print("Eg: a1, b5, f6\n")

	# Start game
	while True:
		move = input(board.get_player() + " player's turn: ")

		# Check user input
		if move.lower() == 'quit' or move.lower() == 'q':
			print("GAME END")
			return
		else:
			if not check_input(move, board):
				continue

		# Player make the move
		board.move(int(move[1]) - 1, Mark.IDX[move[0]])
		board.render()

		# End the game
		if board.game_end():
			print("GAME END, WINNER IS PLAYER " + board.get_winner())

# Return False for bad input and True for correct input
def check_input(move, board):
	# Check for bad move input
	if not len(move) == 2:
		print("BAD INPUT!! " + board.get_player() + " try again")
		return False
	try:
		if not move[0] in Mark.COL or int(move[1]) < 1 or int(move[1]) > 8:
			print("BAD INPUT!! " + board.get_player() + " try again")
			return False
	except ValueError:
		print("BAD INPUT!! " + board.get_player() + " try again")
		return False
	return True

if __name__ == '__main__':
	main()