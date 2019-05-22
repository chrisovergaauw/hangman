import unittest
from app.main.models import User, Hangman


class HangmanTestCase(unittest.TestCase):

    def setUp(self):
        user = User()
        user.id = 1
        user.username = 'tester'
        user.email = 'a@example.com'
        self.user = user

    def test_generated_solution(self):
        hangman = Hangman(user_id=self.user.id)
        allowed_solutions = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
        self.assertTrue(hangman.solution in allowed_solutions)


if __name__ == '__main__':
    unittest.main()
