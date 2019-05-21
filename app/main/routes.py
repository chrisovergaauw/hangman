from flask import render_template


from flask_login import login_required
from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Hubert'}
    return render_template('index.html', title='Home', user=user)


@bp.route('/hangman', methods=['POST', 'GET'])
@login_required
def create_new_hangman_game():
    return '{ hangman: hangman_string, token: game token }'


@bp.route('/hangman', methods=['PUT'])
def update_hangman_game():
    return '{ hangman: hangman_string_updated, token: game token }'


@bp.route('/hangman/hint', methods=['GET'])
def get_hint():
    return 'a'

