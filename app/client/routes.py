from app.client import bp
from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user = current_user
    return render_template('client/index.html', title='Home', user=user)
