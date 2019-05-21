from flask import render_template, request, Response


from flask_login import login_required, current_user
from app.main import bp
from app import db
from app.main.models import User, Hangman


@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Hubert'}
    return render_template('index.html', title='Home', user=user)


@bp.route('/hangman', methods=['POST', 'GET'])
@login_required
def create_new_hangman_game():
    hangman = Hangman(user_id=current_user.id)
    db.session.add(hangman)
    db.session.commit()
    return '{ hangman: %s, token: %s }' % (hangman.get_word(), hangman.token)


@bp.route('/hangman', methods=['PUT'])
@login_required
def update_hangman_game():
    if 'letter' in request.get_json() and 'token' in request.get_json():
        guess = request.get_json()['letter']
        token = request.get_json()['token']
        hangman = Hangman.query.get(token)
        if guess in hangman.correct_guesses+hangman.incorrect_guesses:
            return Response(status=304)
        correct = hangman.guess(guess)
        db.session.commit()
    return '{ hangman: %s, token: %s correct: %s}' % (hangman.get_word(), hangman.token, correct)

