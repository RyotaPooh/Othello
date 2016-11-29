#!/usr/bin/env python3
from tkinter import *
from board import Board
from board import Cell
from board import State
from player import Player
from ai import *
import time

class Fill:
	color = ['', 'white', 'black']

class GUI:
	def __init__(self, size, player1, player2):
		self.size = size
		# Temporary initial board to generate starting canvas
		self.board = Board("Othello", self.size, player1, player2)
		self.cell_size = 50
		self.cell_pad = 5
		self.player_turn = False
		self.started = False

		self.app = Tk()
		self.app.title("Othello")
		self.app.resizable(width=False, height=False)

		self.bottom_text = Frame(self.app)
		self.bottom_text.pack(side=BOTTOM)

		self.left_menu = Frame(self.app, bd=1)
		self.left_menu.pack(side=LEFT)

		self.right_canvas = Frame(self.app)
		self.right_canvas.pack(side=LEFT)

	# Start button
	def start(self):
		if not self.started:
			self.started = True
			self.print_text("Start Othello Game")
			self.top_level = Toplevel()
			prompt = Label(self.top_level, text='Do you want to start first?', width=20, height=2)
			prompt.pack()
			yes_button = Button(self.top_level, text='Yes', command=lambda : self.player_first(True), width=6, height=1)
			yes_button.pack(side=LEFT)
			no_button = Button(self.top_level, text='No', command=lambda : self.player_first(False), width=6, height=1)
			no_button.pack(side=LEFT)

	# Set up the game based on which player start first
	def player_first(self, is_player_first):
		self.top_level.destroy()

		if is_player_first:
			player1 = Player("BLACK", Cell.B)
			player2 = AI_Greedy_Random("AI_RANDOM", Cell.W)
			self.board = Board("Othello", self.size, player1, player2)
			self.update_board()
		else:
			player1 = AI_Greedy_Random("AI_RANDOM", Cell.B)
			player2 = Player("WHITE", Cell.W)
			self.board = Board("Othello", self.size, player1, player2)
			self.ai_move()

		self.player_turn = True

	def ai_move(self):
		move = self.board.get_player().get_move(self.board)
		state = self.board.move(move[0], move[1])

		if state == State.OUT_OF_MOVE:
			self.print_text(str(self.board.get_opponent()) + " out of moves, " + str(self.board.get_player()) + "'s turn")

		time.sleep(1)
		self.update_board()
		self.print_text("AI MOVE: (" + str(move[0]) + "," + str(move[1]) + ")")

	def player_move(self, event):
		if self.player_turn:
			self.player_turn = False
			x = int(event.x/self.cell_size)
			y = int(event.y/self.cell_size)

			state = self.board.move(x, y)

			# If move invalid
			if state == State.INVALID_MOVE:
				self.print_text("Invalid move, please try again")
				self.player_turn = True
				return
			
			self.update_board()
			self.print_text("PLAYER MOVE: (" + str(x) + "," + str(y) + ")")

			# If game ends
			if self.check_game_end():
				self.player_turn = False
				return

			# If out of moves for player
			if state == State.OUT_OF_MOVE:
				print(str(self.board.get_opponent()) + " out of moves, " + str(self.board.get_player()) + "'s turn")
			else:
				# Else, AI's turn to move
				self.ai_move()
				if self.check_game_end():
					self.player_turn = False
					return

			self.player_turn = True

	# Return True if game end
	def check_game_end(self):
		if self.board.game_end():
			if self.board.get_winner():
				self.print_text("GAME END, WINNER IS " + str(self.board.get_winner()))
			else:
				self.print_text("IT IS A TIE")
			return True
		return False

    # Restart button
	def restart(self):
		self.started = False
		self.start()

	# End game button
	def end(self):
		self.app.destroy()

	def set_up_menu(self):
		# Set up buttons on the left menu
		start_button = Button(self.left_menu, text='Start', command=self.start, width=5, height=2)
		start_button.pack()
		restart_button = Button(self.left_menu, text='Restart', command=self.restart, width=5, height=2)
		restart_button.pack()
		end_button = Button(self.left_menu, text='End', command=self.end, width=5, height=2)
		end_button.pack()

	def set_up_canvas(self):
		# Set up canvas
		self.canvas_length = self.size * self.cell_size
		self.canvas = Canvas(self.right_canvas, width=self.canvas_length, height=self.canvas_length, bd=1, relief=SUNKEN)
		self.canvas.bind('<Button-1>', self.player_move)
		self.canvas.pack()

		# Draw the lines
		for i in range(1, self.size + 1):
			self.canvas.create_line(0, i * self.cell_size, self.canvas_length, i * self.cell_size)
			self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.canvas_length)

		# Generate pieces
		self.pieces = [[None for i in range(self.size)] for i in range(self.size)]

		for i in range(self.size):
			for j in range(self.size):
				self.pieces[i][j] = self.canvas.create_oval(i * self.cell_size + self.cell_pad, j * self.cell_size + self.cell_pad, 
					(i + 1) * self.cell_size - self.cell_pad, (j + 1) * self.cell_size - self.cell_pad)

		self.update_board()

	def update_board(self):
		board_array = self.board.get_board()

		for i in range(self.size):
			for j in range(self.size):
				self.canvas.itemconfig(self.pieces[i][j], fill=Fill.color[board_array[i][j]])

		self.app.update_idletasks()

	def set_up_text(self):
		self.text_box = Text(self.bottom_text, width = 66, height = 7, state=DISABLED)
		self.text_box.pack()

	# Print string to textbox
	def print_text(self, string):
		self.text_box.config(state=NORMAL)
		self.text_box.insert(INSERT, string + "\n")
		self.text_box.config(state=DISABLED)

	def run(self):
		self.set_up_menu()
		self.set_up_canvas()
		self.set_up_text()
		self.app.mainloop()