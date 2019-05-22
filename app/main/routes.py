from flask import render_template, request, Response, jsonify


from flask_login import login_required, current_user
from app import csrf
from app.main import bp
from app import db
from app.main.models import User, Hangman


@bp.route('/hangman', methods=['POST'])
@login_required
def create_new_hangman_game():
    hangman = Hangman(user_id=current_user.id)
    db.session.add(hangman)
    db.session.commit()
    return jsonify(hangman=hangman.get_word(), token=hangman.token)



@bp.route('/hangman', methods=['PUT'])
@login_required
@csrf.exempt
def update_hangman_game():
    print(request)
    if 'letter' in request.get_json() and 'token' in request.get_json():
        guess = request.get_json()['letter']
        token = request.get_json()['token']
        hangman = Hangman.query.get(token)
        if guess in hangman.correct_guesses+hangman.incorrect_guesses:
            return Response(status=304)
        correct = hangman.guess(guess)
        db.session.commit()
        return jsonify(hangman=hangman.get_word(), token=hangman.token, correct=correct)


@bp.route('/hangman/', methods=['GET'])
@login_required
def get_hangman_solution():
    token = request.args.get('token')
    hangman = Hangman.query.get(token)
    if hangman is not None:
        return '{ solution: %s, token: %s }' % (hangman.solution, hangman.token)
    else:
        return Response(status=404)

