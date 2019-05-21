from app import db, create_app
from app.main.models import User, Hangman

app = create_app()
app.app_context().push()

users = User.query.all()
for u in users:
    db.session.delete(u)
print('deleted all users...')

hs = Hangman.query.all()
for h in hs:
    db.session.delete(h)
print('deleted all games...')

print('creating new user...')
user = User(username='hangman', email='a@example.com')
user.set_password('3dhubs')
db.session.add(user)
db.session.commit()
print(user)

