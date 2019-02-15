from datetime import datetime

from flask import Blueprint, session, render_template

from . import auth, data_access, db

bp = Blueprint('views', __name__)


@bp.route('/')
@auth.login_required
def index():
    db.get_db()
    USER_ID = session.get('user_id', None)
    user_data = data_access.get_user_data(USER_ID)  # TODO: załadować wszystko do sesji?

    ban = data_access.get_last_active_ban(USER_ID)
    points = data_access.get_points(USER_ID)
    weekly_highscore = data_access.get_weekly_highscore(user_id=1)

    role = user_data['role']

    children = None
    if role == 'caregiver':
        children = data_access.get_caregivers_children(USER_ID)

    context = {"firstname": user_data['firstname'],
               "role": role,
               "points": points,
               "ban": ban,
               "children": children,  # TODO: this should be rectified
               "weekly_highscore": weekly_highscore}
    if ban:
        context["time_ban_stop"] = (ban['end'] - datetime.now()).seconds // 60

    return render_template('index.html', **context)
