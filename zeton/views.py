from datetime import datetime

from flask import Blueprint, session, render_template, abort

from zeton.data_access import get_child_data
from . import auth, data_access, db

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
        context = {'child': child}

    return render_template(template, **context)


@bp.route('/child/<child_id>')
@auth.login_required
def child(child_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    if not users.is_child_under_caregiver(child_id, logged_user_id):
        return abort(403)

    child = users.get_child_data(child_id)
    tasks = users.get_tasks(child_id)
    prizes = users.get_prizes(child_id)

    context = {'child': child, 'tasks': tasks, 'prizes': prizes}

    return render_template('child_info.html', **context)
