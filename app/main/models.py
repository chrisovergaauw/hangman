from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from app.main.util import generate_random_solution
import uuid
from datetime import datetime


class Hangman(db.Model):
    token = db.Column(db.String(16), primary_key=True)
    finished = db.Column(db.Boolean, default=False)
    solution = db.Column(db.String(64))
    correct_guesses = db.Column(db.String(32), default='')
    incorrect_guesses = db.Column(db.String(32), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ts_created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, user_id):
        self.token = str(uuid.uuid4())
        self.solution = generate_random_solution()
        self.user_id = user_id

    def get_word(self):
        word = ''
        for char in self.solution:
            word += '_' if char not in self.correct_guesses else char

        if word == self.solution:
            self.finished = True
        return word

    def guess(self, guess):
        if guess in self.solution:
            self.correct_guesses += guess
            return True
        else:
            self.incorrect_guesses += guess
            return False

    def __repr__(self):
      return """ \
      hangman: %s \n
      finished: %r\n
      solution: %s\n
      correct_guesses: %s\n
      incorrect_guesses: %s\n
      user: %s\
      """ % (self.token, self.finished, self.solution, self.correct_guesses, self.incorrect_guesses, self.user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    games = db.relationship('Hangman', backref='player', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))



