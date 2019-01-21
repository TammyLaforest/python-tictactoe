from flask import Flask, render_template, session, redirect, url_for
from flask_session.__init__ import Session
from tempfile import mkdtemp
import random
# import tictactoeai

app = Flask(__name__)
 
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
		session.clear()
		session["won"] = True
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["turn"] = "X"
		session["message"] = "Start a New Game"

		return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )
 
@app.route("/new_game")
def new_game():
		session.clear()
		session["message"] = "Begin! X goes first."
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["turn"] = "X"
		session["won"] = False
		session["count"] = 0
		# session["save"] = []
		board = session["board"]
		return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )


 
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
	session["board"][row][col] = session["turn"]
	turn = session ["turn"]
	board = session["board"]
	session["message"] = score(row, col)
	if session["message"] == "Draw!":
		return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])

	# Change the turn
	if session["turn"] == "X":
		session["turn"] = "Y"
	else: 
		session["turn"] = "X"
	session["count"] += 1
	print(session["count"])
	return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])


def score(row, col):
		board = session["board"]
		turn = session ["turn"]
		
		if (board[row][0] == board[row][1] == board[row][2] 
			or board[0][col] == board[1][col] == board[2][col]):
			session["won"] = True
			return f"{ turn } wins!"
			
		elif board[1][1] is not None:
			if (board[0][0] == board[1][1] == board[2][2] 
			or board[2][0] == board[1][1] == board[0][2]):
				if board[1][1] == turn:
					session["won"] = True
					return f" {turn } Wins!"
			
			elif session["count"] == 8:
				return "Draw!"
			else:
				return "Try Again!"

		else:
			if turn == "X":
				return "It is Y's turn."
			else:
				return "Your move!"


@app.route("/ai_game")
def ai_game():
		session.clear()
		session["message"] = "New game. Human goes first."
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["scores"] = [[0, 0, 0,], [0, 0, 0], [0, 0, 0]]
		session["turn"] = "X"
		session["won"] = False
		session["count"] = 0
		session["save"] = []
		board = session["board"]
		return render_template("playai.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )


@app.route("/playai/<int:row>/<int:col>")
def playai(row, col):
	
	session["board"][row][col] = session["turn"]
	session["save"] += [row, col]
	session["scores"][row][col] = 1
	session["count"] += 1
	session["message"] = score(row, col)
	if session["message"] == "Draw!":
		return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])

	
	session["turn"] = "Y"
	
	row, col = computer_choice()
	session["board"][row][col] = session["turn"]
	session["scores"][row][col] = -3
	session["count"] += 1
	
	session["message"] = score(row, col)
	if session["message"] == "Draw!":
		return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])

	
	session["turn"] = "X" 
	print(session["save"])
	return render_template("playai.html", game=session["board"], message=session["message"], won =session["won"])



def computer_choice():
	board = session["board"]
	scores = session ["scores"]
	turn = session ["turn"]
	corners = (0, 2)
	

	# If player one doesn't choose the center in their first move, choose the center. Otherwise choose a corner. 
	if session["count"] == 1:
		if board[1][1] is None:
			return 1, 1
		else:
			return random.choice(corners), random.choice(corners)
	
	# If there is a chance of playing a winning move, play that first. 
	# Check for horizontal wins. 
	else:
		for i in range(3):
			if sum(scores[i]) == -6:
				for j in range(3):
					if board[i][j] != "Y":
						return i, j

	# Check for vertical wins.
		for j in range(3):
			if (scores[0][j] + scores[1][j] + scores[2][j]) == -6:
				for i in range(3):
					if board[i][j] != "Y":
						return i, j

	# Check for first diagonal win. 
		if scores[0][0] + scores[1][1] + scores[2][2] == -6:
			if board[0][0] != "Y":
				return  0, 0
			else:
				return 2, 2

	# Check for second diagonal win. 
		elif scores[0][2] + scores[1][1] + scores[2][0] == -6:
			if board[0][2] != "Y":
				return 0, 2
			else:
				return 2, 0		

	# If a win isn't an option, check if there is the immediate threat of defeat.
	# Check for horizontal threats. 
		for i in range(3):
			if sum(scores[i]) == 2:
				for j in range(3):
					if board[i][j] != "X":
						return i, j

	# Check for vertical threats.
		for j in range(3):
			if (scores[0][j] + scores[1][j] + scores[2][j]) == 2:
				for i in range(3):
					if board[i][j] != "X":
						return i, j

	# Check for first diagonal threat. 
		if scores[0][0] + scores[1][1] + scores[2][2] == 2:
			if board[0][0] != "X":
				return  0, 0
			else:
				return 2, 2
	
	# Check for second diagonal threat. 
		elif scores[0][2] + scores[1][1] + scores[2][0] == 2:
			if board[0][2] != "X":
				return 0, 2
			else:
				return 2, 0		

	# Else, find an empty spot and take it. 
		else: 
			for i in range(3):
				for j in range(3):
					if board[i][j] != "X" and board[i][j] != "Y":
						return  i, j
