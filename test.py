from app import db
from app.models import Hangman
h = Hangman(token='somethingUnique', finished=False, solution='3dhubs', correct_guesses='', incorrect_guesses='')
print(h)
