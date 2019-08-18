from flask import Blueprint, render_template, abort, g, request, flash, get_flashed_messages, redirect

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

@bp.route('/settings/', methods=['GET'])
@auth.login_required
def user_settings():

    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']
    user_data = users.get_user_data(logged_user_id)

    context = {'user_data': user_data}
    messages = get_flashed_messages()

    return render_template('user_settings.html', **context, messages=messages)

    # if request.method == 'POST':
    #
    #     users.load_logged_in_user_data()
    #     logged_user_id = g.user_data['id']
    #     logged_user_password = g.user_data['password']
    #     user_data = users.get_user_data(logged_user_id)
    #
    #     password = request.form['password']
    #     new_password = request.form['new_password']
    #     repeat_new_password = request.form['repeat_new_password']
    #
    #     hashed_new_password = generate_password_hash(new_password)
    #
    #     if new_password == repeat_new_password:
    #         if user_data:
    #             if check_password_hash(logged_user_password, password):
    #                 users.update_password(logged_user_id, hashed_new_password)
    #                 flash('Nowe hasło wprowadzone poprawnie')
    #             else:
    #                 flash('Aktualne hasło zostało źle wprowadzone. Spróbuj ponownie')
    #     else:
    #         flash('Nowe hasło i powtórzone nowe hasło muszą się zgadzać. Spróbuj ponownie')
    #
    #     return redirect('/settings/')