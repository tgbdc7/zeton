import functools

from flask import Blueprint, redirect, render_template, request, url_for, session, g, abort
from werkzeug.security import check_password_hash

from zeton.data_access import users
from . import db

bp = Blueprint('auth', __name__)


def get_user_data(login):
    result = db.get_db().execute("SELECT * FROM users WHERE username = ?", [login])
    user_data = result.fetchall()
    if len(user_data) == 0:
        return None
    elif len(user_data) == 1:
        return user_data[0]
    else:
        raise Exception("Database error: duplicate username found!")


def password_validation(password):
    if (any(x.isupper() for x in password)
            and any(x.islower() for x in password)
            and any(x.isdigit() for x in password)
            and len(password) >= 8):
        return True
    return False


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['login'].lower()
        password = request.form['password']

        user_data = get_user_data(login)

        if user_data:

            hashed_password = user_data['password']

            if check_password_hash(hashed_password, password):
                session['user_id'] = user_data['id']
                session['role'] = user_data['role']
                return redirect(url_for('views.index'))

        error = 'Invalid login or username'
    return render_template('base/login.html', error=error)


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET'])
def register():
    # redirects already logged in user to the index view
    users.load_logged_in_user_data()
    if g.user_data:
        return redirect(url_for('views.index'))
    prev_url = request.referrer
    return render_template('user/register_form.html', prev_url=prev_url)


@bp.route('/add-person', methods=['GET'])
def add_person():
    prev_url = request.referrer
    return render_template('user/add_person.html', prev_url=prev_url)


# login required decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' in session:
            return view(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))

    return wrapped_view


def caregiver_only(view):
    """
    This decorator allows only requests made by:
    - a caregiver for a resource related to a child under his/hers care

    the decorated view MUST take parameter named 'child_id'
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        logged_user_id = g.user_data['id']
        try:
            child_id = int(kwargs['child_id'])
        except KeyError:
            print(f"The view '{view.__name__}' did not pass 'child_id' parameter")
            return abort(500)

        if not users.is_child_under_caregiver(child_id, logged_user_id):
            return abort(403)

        return view(*args, **kwargs)

    return wrapped_view


def logged_child_or_caregiver_only(view):
    """
    This decorator allows only requests made by:
    - a caregiver for a resource related to a child under his/hers care
    OR
    - a child for a resource related to itself

    the decorated view MUST take parameter named 'child_id'
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        logged_user_id = g.user_data['id']
        try:
            child_id = int(kwargs['child_id'])
        except KeyError:
            print(f"The view '{view.__name__}' did not pass 'child_id' parameter")
            return abort(500)

        if not (child_id == logged_user_id or
                users.is_child_under_caregiver(child_id, logged_user_id)):
            return abort(403)

        return view(*args, **kwargs)

    return wrapped_view


class Permissions:

    ADD_POINTS = 1
    USE_POINTS = 2
    EDIT_TASKS = 4
    EDIT_PRIZES = 8
    ADD_BAN = 16
    EDIT_BAN = 32
    ADD_SCHOOL_POINTS = 64
    EDIT_SCHOOL_POINTS = 128
    EDIT_KIDS_SETTINGS = 256
    EDIT_CAREGIVER_LIST = 512


def can(permission):
    users.load_logged_in_user_data()
    role = g.user_data['role']
    user_permissions = users.get_role_permissions(role)
    return user_permissions & permission == permission


def has_permission(permission):
    if not can(permission):
        abort(400, 'no authorization')
