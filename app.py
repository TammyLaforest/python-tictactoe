from flask import Flask, render_template, session, redirect, url_for
from flask_session.__init__ import Session
from tempfile import mkdtemp
 
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
		session["message"] = "Begin!"
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["turn"] = "X"
		session["won"] = False
		session["count"] = 0
		print(session["won"])
		board = session["board"]
		return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )


@app.route("/ai_game")
def ai_game():
		session.clear()
		session["message"] = "new game"
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["turn"] = "X"
		session["won"] = False
		session["count"] = 0
		print(session["won"])
		board = session["board"]
		return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won = session["won"] )

 
@app.route("/play/<int:row>/<int:col>")
def play(row, col):
	session["board"][row][col] = session["turn"]
	turn = session ["turn"]
	board = session["board"]
	session["message"] = score(row, col, turn, board)

	# Change the turn
	if session["turn"] == "X":
		session["turn"] = "Y"
	else: 
		session["turn"] = "X"
	session["count"] += 1
	print(session["count"])
	return render_template("game.html", game=session["board"], turn=session["turn"], message=session["message"], won =session["won"])



def score(row, col, turn, board):
		
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
				print(session["count"])
				return "Draw!"
			else:
				print(session["count"]) 
				if turn == "X":
					return "It's Y's turn."
				else:
					return "It's X's turn."
		else:
			if turn == "X":
				return "It is Y's turn."
			else:
				return "It is X's turn."
