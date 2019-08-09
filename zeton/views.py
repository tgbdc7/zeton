from flask import Blueprint, session, render_template, abort, g

from zeton.data_access.data_access import get_child_data, load_logged_in_user_data
from . import auth
from zeton.data_access import data_access

bp = Blueprint('views', __name__)


@bp.route('/')
@auth.login_required
def index():
    load_logged_in_user_data()

    role = g.user_data['role']
    logged_user_id = g.user_data['id']

    template = None
    context = {}

    if role == 'caregiver':
        children = data_access.get_caregivers_children(logged_user_id)
        template = 'index_caregiver.html'
        context.update({"firstname": g.user_data['firstname'],
                        "role": role,
                        "children": children})

    elif role == 'child':
        template = 'index_child.html'
        child = get_child_data(logged_user_id)
        context = {'child': child}

    return render_template(template, **context)


@bp.route('/child/<child_id>')
@auth.login_required
def child(child_id):
    load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    if not data_access.is_child_under_caregiver(child_id, logged_user_id):
        return abort(403)

    child = get_child_data(child_id)

    context = {'child': child}

    return render_template('child_info.html', **context)
