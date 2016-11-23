#!/usr/bin/env python3
from tkinter import *

def start():
	print("Start game")

def restart():
	print("Restart game")

def end():
	print("End game")

def main():
	app = Tk()
	app.title("Othello")
	app.resizable(width=False, height=False)
	left_side = Frame(app, bd=1)
	left_side.pack(side=LEFT)
	right_side = Frame(app)
	right_side.pack(side=LEFT)

	start_button = Button(left_side, text='Start', command=start, width=5, height=2)
	start_button.pack()
	restart_button = Button(left_side, text='Restart', command=restart, width=5, height=2)
	restart_button.pack()
	end_button = Button(left_side, text='End', command=end, width=5, height=2)
	end_button.pack()


	size = 8
	cell_height = 50
	cell_width = 50

	canvas_width = size*cell_width
	canvas_height = size*cell_height
	w = Canvas(right_side, width=size*cell_width, height=size*cell_height, bd=1, relief=SUNKEN)
	w.pack()

	for i in range(1, size + 1):
		w.create_line(0, i * cell_height, canvas_width, i * cell_height)
		w.create_line(i * cell_width, 0, i * cell_width, canvas_width)

	pad = 5

	for i in range(size):
		for j in range(size):
			w.create_oval(i * cell_height + pad, j * cell_width + pad, (i + 1) * cell_height - pad, (j + 1) * cell_width - pad,
				fill='white')

	app.mainloop()

if __name__ == '__main__':
	main()

