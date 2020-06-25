from flask import Flask, request, redirect, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "dogsaregreat2314322222"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()
session["board"] = []


@app.route('/')
def show_board():
    """Show game board."""

    board = boggle_game.make_board()
    session["board"] = board
    high_score = session.get("high_score", 0)
    num_plays = session.get("num_plays", 0)

    return render_template('game.html', board=board, high_score=high_score, num_plays=num_plays)


@app.route('/check-word')
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': reponse})


@app.route('/post-score', methods=["POST"])
def post_score():
    """Grab score, update num_plays, update high score."""

    score = request.json["score"]
    high_score = session.get("high_score", 0)
    num_plays = session.get("num_plays", 0)

    session["num_plays"] = num_plays + 1
    session["high_score"] = max(score, high_score)

    return jsonify(newRecord=score > high_score)
