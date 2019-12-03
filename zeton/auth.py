import functools
import datetime
from flask import Blueprint, redirect, render_template, request, url_for, session, g, abort, get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash
from zeton.data_access import users
from . import db
from zeton.api.send_email import is_pass_rec_email

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

        error = 'Błędny login lub hasło'
    return render_template('base/login.html', error=error)

@bp.route('/pass_rec', methods=['GET', 'POST'])
def pass_rec():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        emial = request.form['email']

        user_data = get_user_data(username)

        if user_data:
            user_data_username = user_data['username']
            user_data_email = user_data['email']
            if user_data_username == username and user_data_email == emial:
                # fix me
                # send mail
                sha = generate_password_hash(str(datetime.datetime.now()), "sha256")
                sha = sha.replace('sha256$', '')
                expire = datetime.datetime.now() + datetime.timedelta(hours=1)
                message = users.pass_rec(username, emial, sha, expire)
                if not is_pass_rec_email(emial,sha):
                    message = "Blad wysylania email, skontaktuj sie z administratorem"

                # file
                f = open("email_test.txt", "a")
                f.write(f"http://127.0.0.1:5000/pass_rec/{sha}\n")
                return render_template('base/login.html', error=message)

        error = 'Invalid login or email'
    return render_template('user/pass_rec_form.html', error=error)


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

@bp.route('/pass_rec/<sha>', methods=['GET'])
def new_pass(sha, messages=None):
    user_name = users.get_user_name_pass_recovery_sha(sha)
    if user_name!=None:
        user_id = users.get_user_id(user_name)
        user_data = users.get_user_data(user_id)

        context = {'user_data': user_data}
        messages = get_flashed_messages()
        return render_template('user/password_recovery.html', **context, sha=sha, messages=messages)
    else:
        message = "Link do odzyskania hasłą jest błędny lub przeterminowany"
        return render_template('base/login.html', error=message)

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
