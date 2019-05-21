from app import app
from app import db

from flask import render_template, redirect, flash, url_for
from app.forms import LoginForm, RegistrationForm

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Hubert'}
    return render_template('index.html', title='Home', user=user)


@app.route('/hangman', methods=['POST', 'GET'])
@login_required
def create_new_hangman_game():
    return '{ hangman: hangman_string, token: game token }'


@app.route('/hangman', methods=['PUT'])
def update_hangman_game():
    return '{ hangman: hangman_string_updated, token: game token }'


@app.route('/hangman/hint', methods=['GET'])
def get_hint():
    return 'a'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
