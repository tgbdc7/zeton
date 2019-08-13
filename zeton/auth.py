import functools

from flask import Blueprint, redirect, render_template, request, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from zeton.data_access.users import add_new_user

bp = Blueprint('auth', __name__)


def get_user_data(login):
    result = db.get_db().execute("SELECT * FROM users WHERE username = ?", [login])
    return result.fetchone()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user_data = get_user_data(login)

        if user_data:

            hashed_password = user_data['password']

            if check_password_hash(hashed_password, password):
                session['user_id'] = user_data['id']
                session['role'] = user_data['role']
                return redirect(url_for('views.index'))

        error = 'Invalid login or username'
    return render_template('login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # password2 = request.form['password2']
        password_hash = generate_password_hash(password)
        role = request.form['role']
        first_name = request.form['first_name']

        data = (username, password_hash, first_name, role)
        add_new_user(data)

        return redirect(url_for('views.index'))

    return render_template('register_form.html')







# login required decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' in session:
            return view(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return wrapped_view
