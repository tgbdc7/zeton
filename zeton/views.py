from flask import Blueprint, render_template, abort, g

from . import auth
from zeton.data_access import users, prizes, tasks

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
    role = g.user_data['role']

    context = {'child': child, 'childs_tasks': childs_tasks, 'childs_prizes': childs_prizes, 'role': role}

    return render_template('caregiver_panel.html', **context)

@bp.route('/prizes_detail/<child_id>')
@auth.login_required
def prizes_detail(child_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    try:
        child = users.get_child_data(child_id)
    except TypeError:
        return abort(403)

    childs_prizes = prizes.get_prizes(child_id)

    if not (child['id'] == logged_user_id or
            users.is_child_under_caregiver(child_id, logged_user_id)):
        return abort(403)


    context = {'child': child, 'childs_prizes': childs_prizes}

    return render_template('prizes_detail.html', **context)