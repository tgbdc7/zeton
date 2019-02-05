import functools

from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from zeton.db import get_db

# bp = Blueprint('auth', __name__, url_prefix='/auth')
bp = Blueprint('auth', __name__)


def validate_credentials(login, password):
    result = get_db().execute("SELECT password FROM users WHERE username = ?", [login])
    try:
        hashed_password = result.fetchone()[0]
    except TypeError:
        return False

    if check_password_hash(hashed_password, password):
        return True
    return False


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if validate_credentials(login, password):
            return redirect(url_for('hello'))
        else:
            error = 'Invalid login or username'
    return render_template('login.html', error=error)
