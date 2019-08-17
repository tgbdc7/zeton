from flask import Blueprint, render_template, abort, g

from . import auth
from zeton.data_access import users, prizes, tasks

from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('views', __name__)


@bp.route('/')
@auth.login_required
def index():
    users.load_logged_in_user_data()

    role = g.user_data['role']
    logged_user_id = g.user_data['id']

    template = None
    context = {}

    if role == 'caregiver':
        children = users.get_caregivers_children(logged_user_id)
        template = 'index_caregiver.html'
        context.update({"firstname": g.user_data['firstname'],
                        "role": role,
                        "children": children})

    elif role == 'child':
        template = 'index_child.html'
        child = users.get_child_data(logged_user_id)
        childs_tasks = tasks.get_tasks(logged_user_id)
        childs_prizes = prizes.get_prizes(logged_user_id)
        context = {'child': child, 'childs_tasks': childs_tasks, 'childs_prizes': childs_prizes}

    return render_template(template, **context)


@bp.route('/child/<child_id>')
@auth.login_required
def child(child_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    if not users.is_child_under_caregiver(child_id, logged_user_id):
        return abort(403)

    child = users.get_child_data(child_id)
    childs_tasks = tasks.get_tasks(child_id)
    childs_prizes = prizes.get_prizes(child_id)

    context = {'child': child, 'childs_tasks': childs_tasks, 'childs_prizes': childs_prizes}

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