from datetime import datetime

from flask import Blueprint, session, render_template, abort

from zeton.data_access import get_child_data
from . import auth, data_access, db

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
        ban = data_access.get_last_active_ban(USER_ID)
        points = data_access.get_points(USER_ID)
        weekly_highscore = data_access.get_weekly_highscore(user_id=1)

        template = 'index_child.html'
        child = get_child_data(USER_ID)
        context.update(**child)
        if child['ban']:
            context["time_ban_stop"] = (child['ban']['end'] - datetime.now()).seconds // 60

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
