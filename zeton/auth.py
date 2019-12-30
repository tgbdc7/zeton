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


class Permission:

    def __init__(self, value, label):
        self._value = value
        self._label = label

    def get_value(self):
        return self._value

    def get_label(self):
        return self._label


permissions = {
    'ADD_POINTS': Permission(1, 'dodawanie puntków'),
    'USE_POINTS': Permission(2, 'używanie punktów'),
    'EDIT_TASKS': Permission(4, 'edycja zadań'),
    'EDIT_PRIZES': Permission(8, 'edycja nagród'),
    'ADD_BAN': Permission(16, 'dodanie bana'),
    'EDIT_BAN': Permission(32, 'edytowanie bana'),
    'ADD_SCHOOL_POINTS': Permission(64, 'dodawanie punktów ze szkoły'),
    'EDIT_SCHOOL_POINTS': Permission(128, 'edytowanie punktów ze szkoły'),
    'EDIT_KIDS_SETTINGS': Permission(256, 'edytowanie ustawień dziecka'),
    'EDIT_CAREGIVER_LIST': Permission(512, 'edytowanie listy opiekunów'),
}


def check_permission(user_id, permission):
    if not has_permission(user_id, permission):
        abort(403, 'no authorization')


def has_permission(user_id, permission):
    user_permissions = users.get_individual_permissions(user_id) or \
                       users.get_role_permissions(g.user_data['role'])
    return user_permissions & permission == permission


def grant_permission(user_id, permission):
    if has_permission(user_id, permission):
        print('permission already granted') # TODO: implement better handling
        abort(403)
    users.add_permission(user_id, permission)


def take_permission(user_id, permission):
    if not has_permission(user_id, permission):
        print('user does not have requested permission') # TODO: implement better handling
        abort(403)
    users.remove_permission(user_id, permission)


def get_used_permissions(user_id, permissions):
    result = [permission for permission in permissions.values()
              if has_permission(user_id, permission.get_value())]
    return result


def get_unused_permissions(user_id, permissions):
    result = [permission for permission in permissions.values()
              if not has_permission(user_id, permission.get_value())]
    return result
