import functools

from flask import Blueprint, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

# bp = Blueprint('auth', __name__, url_prefix='/auth')
bp = Blueprint('auth', __name__)


def get_user_data(login):
    result = get_db().execute("SELECT id, password FROM users WHERE username = ?", [login])
    user_data = result.fetchone()

    if user_data:
        user_id = user_data['id']
        hashed_password = user_data['password']
        return (user_id, hashed_password)
    return None, None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user_id, hashed_password = get_user_data(login)

        if hashed_password and check_password_hash(hashed_password, password):
            session['user_id'] = user_id
            return redirect(url_for('hello'))
        else:
            error = 'Invalid login or username'
    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))


# login required decorator
def login_required(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return wrap
