#!/usr/bin/env python3
from tkinter import *
from board import Board
from board import Cell
from board import State
from player import Player
from ai import *
import time
from threading import Thread, Lock, active_count

# Color to used for the canvas
class Fill:
	color = ['', 'white', 'black']

class GUI:
	def __init__(self, size, player1, player2):
		# Temporary initial board to generate starting canvas
		self.size = size
		self.board = Board("Othello", self.size, player1, player2)
		self.cell_size = 50
		self.cell_pad = 5

		# Conditions
		self.player_active = False # True = Player input is active
		self.player_vs_ai = False # True = Player vs ai game has started
		self.ai_vs_ai = False # True = A game is ongoing, can be player game or ai game
		self.ai_lock = Lock() # Lock for ai vs ai game thread
		self.ai_stop = False # True = Stop the AI game

		self.app = Tk()
		self.app.title("Othello")
		self.app.resizable(width=False, height=False)

		# Textbox for displaying messages
		self.bottom_frame = Frame(self.app)
		self.bottom_frame.pack(side=BOTTOM)

		# Menu / Options
		self.left_frame = Frame(self.app, bd=1)
		self.left_frame.pack(side=LEFT)

		# Canvas
		self.right_frame = Frame(self.app)
		self.right_frame.pack(side=LEFT)

	# Pit ai against another ai
	def ai_game(self):
		if not self.ai_vs_ai and not self.player_vs_ai and active_count() <= 1:
			self.ai_vs_ai = True
			self.ai_stop = False
			self.print_text("AI GAME (PIT TWO AI AGAINST EACH OTHER)")

			ai1 = AI_Greedy_Random("AI_GREEDY_RANDOM", Cell.B)
			ai2 = AI_Minimax("AI_MINIMAX", Cell.W)
			self.board = Board("Othello", self.size, ai1, ai2)
			self.update_board()

			ai_thread = Thread(target=self.ai_game_thread, daemon=True)
			ai_thread.start()

	# Use thread to run the ai vs ai game
	def ai_game_thread(self):
		while True:
			with self.ai_lock:
				if self.ai_stop or self.check_game_end():
					self.ai_vs_ai = False
					return

			self.ai_move()

	# Set up the game based on which player start first
	def player_first(self, is_player_first):
		# Destroy popup menu
		self.top_level.destroy()

		if is_player_first:
			# Player goes first
			player1 = Player("PLAYER", Cell.B)
			player2 = AI_Minimax("AI_MINIMAX", Cell.W)
			self.board = Board("Othello", self.size, player1, player2)
			self.update_board()
		else:
			# AI goes first
			player1 = AI_Minimax("AI_MINIMAX", Cell.B)
			player2 = Player("PLAYER", Cell.W)
			self.board = Board("Othello", self.size, player1, player2)
			self.update_board()
			self.print_text("AI thinking...")
			self.ai_move()

		self.player_active = True

	# Ai makes a move
	def ai_move(self):
		curr_player = str(self.board.get_player())
		move = self.board.get_player().get_move(self.board)

		with self.ai_lock:
			if self.ai_stop:
				return

		state = self.board.move(move[0], move[1])

		self.update_board()
		self.print_text(curr_player + ": (" + str(move[0]) + "," + str(move[1]) + ")")

		# If opponent is out of moves, ai moves again
		if state == State.OUT_OF_MOVE:
			self.print_text(str(self.board.get_opponent()) + " OUT OF MOVES, " + str(self.board.get_player()) + "'S TURN")
			self.ai_move()

	# Passive open, player makes a move
	def player_move(self, event):
		move_thread = Thread(target=self.player_move_thread, daemon=True, args=[event])
		move_thread.start()

	def player_move_thread(self, event):
		# player_active allows player click to be read
		if self.player_active:
			self.player_active = False
			x = event.x // self.cell_size
			y = event.y // self.cell_size

			curr_player = str(self.board.get_player())
			state = self.board.move(x, y)

			# If move invalid
			if state == State.INVALID_MOVE:
				self.print_text("INVALID MOVE, PLEASE TRY AGAIN")
				self.player_active = True
				return
			
			# Player move is valid and the player makes a move
			self.update_board()
			self.print_text(curr_player + ": (" + str(x) + "," + str(y) + ")")

			# Check if game ends
			if self.check_game_end():
				self.player_active = False
				return

			# If opponent run out of moves, player move again
			if state == State.OUT_OF_MOVE:
				self.print_text(str(self.board.get_opponent()) + " OUT OF MOVES, " + str(self.board.get_player()) + "'S TURN")
			else:
				# Else, AI's turn to move
				self.print_text("AI thinking...")
				
				self.ai_move()

				with self.ai_lock:
					if self.ai_stop:
						return

				if self.check_game_end():
					self.player_active = False
					return

			self.player_active = True

	# Return True if game ends and False otherwise
	def check_game_end(self):
		if self.board.game_end():
			if self.board.get_winner():
				self.print_text("GAME END, WINNER IS " + str(self.board.get_winner()))
			else:
				self.print_text("IT IS A TIE")
			self.ai_vs_ai = False
			self.player_vs_ai = False
			return True
		return False

	# Start button, start the game
	def start(self):
		if not self.player_vs_ai and not self.ai_vs_ai and active_count() <= 1:
			# Set the conditions
			self.player_vs_ai = True
			self.ai_stop = False
			self.print_text("Start Othello Game")

			self.top_level = Toplevel()

			# Set up the top level popup
			prompt = Label(self.top_level, text='Do you want to start first?', width=20, height=2)
			prompt.pack()
			yes_button = Button(self.top_level, text='Yes', command=lambda : self.player_first(True), width=6, height=1)
			yes_button.pack(side=LEFT)
			no_button = Button(self.top_level, text='No', command=lambda : self.player_first(False), width=6, height=1)
			no_button.pack(side=LEFT)

			# Set the position of the popup
			self.app.update_idletasks()
			x = self.app.winfo_rootx() + (self.app.winfo_width() // 2) - (self.top_level.winfo_width() // 2)
			y = self.app.winfo_rooty() + (self.app.winfo_height() // 3) - (self.top_level.winfo_height() // 2)
			self.top_level.geometry('+{}+{}'.format(x, y))

	# Stop the ai vs ai game
	def stop(self):
		self.player_vs_ai = False
		self.player_active = False
		with self.ai_lock:
			self.ai_stop = True
		self.print_text("GAME STOPPED, START THE GAME AGAIN")

    # Restart the game
	def restart(self):
		if self.player_vs_ai:
			self.player_vs_ai = False
			with self.ai_lock:
				self.ai_stop = True
			self.print_text("RESTART GAME")

			while active_count() > 1:
				time.sleep(1)

			self.start()

	# End the game, destroy whole app
	def end(self):
		self.app.destroy()

	def set_up_menu(self):
		# Set up buttons on the left menu
		start_button = Button(self.left_frame, text='Start', command=self.start, width=5, height=2)
		start_button.pack()
		restart_button = Button(self.left_frame, text='Restart', command=self.restart, width=5, height=2)
		restart_button.pack()
		ai_button = Button(self.left_frame, text='AI', command=self.ai_game, width=5, height=2)
		ai_button.pack()
		stop_button = Button(self.left_frame, text='Stop', command=self.stop, width=5, height=2)
		stop_button.pack()
		end_button = Button(self.left_frame, text='End', command=self.end, width=5, height=2)
		end_button.pack()
		

	def set_up_canvas(self):
		# Set up canvas
		self.canvas_length = self.size * self.cell_size
		self.canvas = Canvas(self.right_frame, width=self.canvas_length, height=self.canvas_length, bd=1, relief=SUNKEN)
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

	# Update changes to the board to the canvas
	def update_board(self):
		board_array = self.board.get_board()

		for i in range(self.size):
			for j in range(self.size):
				self.canvas.itemconfig(self.pieces[i][j], fill=Fill.color[board_array[i][j]])

		self.app.update_idletasks()

	# Set up the text box
	def set_up_text(self):
		self.text_box = Text(self.bottom_frame, width = 66, height = 7, state=DISABLED)
		self.text_box.pack()

	# Print string to textbox
	def print_text(self, string):
		self.text_box.config(state=NORMAL)
		self.text_box.insert(INSERT, string + "\n")
		self.text_box.config(state=DISABLED)
		self.text_box.see(END)
		self.app.update_idletasks()

	# Run the game
	def run(self):
		self.set_up_menu()
		self.set_up_canvas()
		self.set_up_text()
		self.app.mainloop()