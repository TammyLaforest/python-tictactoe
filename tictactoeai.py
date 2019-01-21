from flask import Flask, render_template, session, redirect, url_for
from flask_session.__init__ import Session
from tempfile import mkdtemp

def computer_choice(board): 
	if any(board[0] == "X"):
		print("row 0 has an x")
		return "row 0 has an x"


	# if board[1][1] is not None:





	
	# 	if (board[row][0] == board[row][1] == board[row][2] 
	# 		or board[0][col] == board[1][col] == board[2][col]):
	# 		session["won"] = True
	# 		return f"{ turn } wins!"
			
	# 	elif board[1][1] is not None:
	# 		if (board[0][0] == board[1][1] == board[2][2] 
	# 		or board[2][0] == board[1][1] == board[0][2]):
	# 			if board[1][1] == turn:
	# 				session["won"] = True
	# 				return f" {turn } Wins!"
			
	# 		elif session["count"] == 8:
	# 			print(session["count"])
	# 			return "Draw!"
	# 		else:
	# 			print(session["count"]) 
	# 			if turn == "X":
	# 				return "It's Y's turn."
	# 			else:
	# 				return "It's X's turn."
	# 	else:
	# 		if turn == "X":
	# 			return "It is Y's turn."
	# 		else:
	# 			return "It is X's turn."
