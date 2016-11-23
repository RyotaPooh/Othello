#!/usr/bin/env python3
import console as cs
from player import Player
from board import Cell
from ai import AI_Random

def main():
	player1 = Player("BLACK", Cell.B)
	# player2 = Player("WHITE", Cell.W)
	player2 = AI_Random("WHITE", Cell.W)
	cs.main(8, player1, player2)

if __name__ == '__main__':
	main()