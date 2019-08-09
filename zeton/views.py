from datetime import datetime

from flask import Blueprint, session, render_template, abort, request, get_flashed_messages, flash, g, redirect

from zeton.data_access import get_child_data, get_user_data
from . import auth, data_access, db

from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('views', __name__)


@bp.route('/')
@auth.login_required
def index():
    db.get_db()
    USER_ID = session.get('user_id', None)
    user_data = data_access.get_user_data(USER_ID)  # TODO: załadować wszystko do sesji?

    role = user_data['role']

    template = None
    context = {}

    if role == 'caregiver':
        children = data_access.get_caregivers_children(USER_ID)
        template = 'index_caregiver.html'
        context.update({"firstname": user_data['firstname'],
                        "role": role,
                        "children": children})

    elif role == 'child':
        template = 'index_child.html'
        child = get_child_data(USER_ID)
        context = {'child': child}

    return render_template(template, **context)


@bp.route('/child/<child_id>')
@auth.login_required
def child(child_id):
    db.get_db()
    USER_ID = session.get('user_id', None)

    if not data_access.is_child_under_caregiver(child_id, USER_ID):
        return abort(403)

    child = get_child_data(child_id)

    context = {'child': child}

    return render_template('child_info.html', **context)

@bp.route('/settings', methods=['GET', 'POST'])
@auth.login_required
def user_settings():
    if request.method == 'GET':
        db.get_db()

        USER_ID = session.get('user_id', None)
        user_data = data_access.get_user_data(USER_ID)
        context = {'user_data': user_data}
        messages = get_flashed_messages()

        return render_template('user_settings.html', **context, messages=messages)


    if request.method == 'POST':

        password = request.form['password']
        new_password = request.form['new_password']
        hashed_new_password = generate_password_hash(new_password)
        new_password = hashed_new_password

        db.get_db()
        USER_ID = session.get('user_id', None)
        user_data = get_user_data(USER_ID)

        if user_data:
            password_from_db = user_data['password']
            user_id = user_data['id']

            if check_password_hash(password_from_db, password):
                query = "UPDATE users SET password = ? WHERE id = ?"
                params = (new_password, user_id)
                g.db.cursor().execute(query, params)
                g.db.commit()
                flash('Nowe hasło wprowadzone poprawnie')
            else:
                flash('Aktualne hasło zostało źle wprowadzone. Spróbuj ponownie')

    return redirect('/settings')