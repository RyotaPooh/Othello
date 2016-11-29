#!/usr/bin/env python3
import argparse
import console as cs
from gui import GUI
from player import Player
from board import Cell
from ai import *

def main():
	parser = argparse.ArgumentParser(description='Othello game')
	parser.add_argument('-c', action='store_true', help='Run othello game in the console, if not specified, will run in GUI')
	args = parser.parse_args()

	# Size of the board
	size = 8

	if args.c:
		# Run in console
		print("Othello: ")
		opt = input("Do you want to start first, 'y' or 'n': ")

		if opt.lower() == 'y':
			player1 = Player("BLACK", Cell.B)
			player2 = AI_Random("AI_RANDOM", Cell.W)
			cs.main(size, player1, player2)
		elif opt.lower() == 'n':
			player1 = AI_Random("AI_RANDOM", Cell.B)
			player2 = Player("WHITE", Cell.W)
			cs.main(size, player1, player2)
		else:
			print("Wrong input, try again, exiting")
	else:
		player1 = Player("BLACK", Cell.B)
		player2 = Player("WHITE", Cell.W)
		gui = GUI(size, player1, player2)
		gui.run()

if __name__ == '__main__':
	main()