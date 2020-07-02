from boggle import Boggle
from flask import Flask, request, render_template, redirect
from flask import session, make_response, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bogglingsecretswowie'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def home_page():
    """Home page that allow user to choose a board size, and shows current session highscore and number of plays"""
    highscore = session.get('highscore', 0)
    times_played = session.get('times_played', 0)
    return render_template('setup.html', highscore=highscore, times_played=times_played)


@app.route('/board')
def show_board():
    """Creates a boggle board using make_board Boogle method and displays it."""
    size = request.args.get('size-input')
    session['size'] = int(size)
    board = boggle_game.make_board(session['size'])
    session['board'] = board

    return render_template('board.html', board=board)


@app.route('/check-word')
def check_word():
    """Checks user inputed word to see if it is 1) the word exists 2) is on the board, and 3) not already guessed. """
    word = request.args.get('word')
    board = session['board']
    result = boggle_game.check_valid_word(board, word, session['size'])

    return jsonify({'result': result})


@app.route('/save-stats', methods=["POST"])
def save_stats():
    """Updates user's highscore and number of plays. Returns true if new highscore, false if not. """
    score = request.json['score']
    highscore = session.get('highscore', 0)
    times_played = session.get('times_played', 0)

    session['times_played'] = times_played + 1
    session['highscore'] = max(score, highscore)

    return jsonify({'new_highscore': score > highscore})
