#!/usr/bin/env python3
import console as cs
from player import Player
from board import Cell
from ai import *

def main():
	print("Othello: ")
	opt = input("Do you want to start first, 'y' or 'n'")

	if opt.lower() == 'y':
		player1 = Player("BLACK", Cell.B)
		player2 = AI_Random("AI_RANDOM", Cell.W)
		cs.main(8, player1, player2)
	elif opt.lower() == 'n':
		player1 = AI_Random("AI_RANDOM", Cell.W)
		player2 = Player("WHITE", Cell.B)
		cs.main(8, player1, player2)
	else:
		print("Wrong input, try again, exiting")

if __name__ == '__main__':
	main()