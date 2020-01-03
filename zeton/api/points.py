from flask import request, redirect, url_for, abort, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

import zeton.data_access.bans
import zeton.data_access.points
import datetime
from zeton import auth
from zeton.api import bp
import datetime
from zeton.data_access import users


def is_limit_reached(child_id, exercise_id, days, max_column):
    now = datetime.datetime.now() - datetime.timedelta(days= days)
    dt_string = datetime.datetime.fromisoformat(str(now))
    history = zeton.data_access.points.get_points_history_limits(child_id, dt_string, exercise_id)
    points_events_count = history.__len__()

    if points_events_count > 0:
        limit = history[0][max_column]
        if points_events_count >= limit:
            return False
    return True

@bp.route("/child/<child_id>/points/add/<points>/<exercise_id>/<is_detail>", methods=['POST'])
@auth.login_required
@auth.logged_child_or_caregiver_only

def add_points(child_id, points, exercise_id,is_detail):
    if is_limit_reached(child_id, exercise_id, 1, 'max_day') and is_limit_reached(child_id, exercise_id, 7, 'max_week'):
        logged_user_id = g.user_data['id']
        return_url = request.args.get('return_url', '/')

        if exercise_id == '0':
            points = request.form['points']
        try:
            added_points = int(points)
        except ValueError as ex:
            print(ex)
            return {'message': 'Bad request'}, 400

        if added_points > 0:
            zeton.data_access.points.change_points_by(child_id, added_points, logged_user_id, exercise_id)
            zeton.data_access.points.add_exp(added_points, child_id)

        role = g.user_data['role']
        if role == 'child':
            return redirect(return_url)
        else:
            if is_detail == "0":
                return redirect(url_for('views.child', child_id=child_id))
            else:
                return redirect(url_for('views.task_detail', child_id=child_id))
    else:
        if not is_limit_reached(child_id, exercise_id, 1, 'max_day'):
            flash(f'W ciągu ostatniej doby został przekroczony limit punktów')

        if not is_limit_reached(child_id, exercise_id, 7, 'max_week'):
            flash(f'W ciągu ostatnich 7 dni został przekroczony limit punktów')


        if is_detail == "0":
            return redirect(url_for('views.child', child_id=child_id))
        else:
            return redirect(url_for('views.task_detail', child_id=child_id))



@bp.route("/child/<child_id>/points/use", methods=['POST'])
@auth.login_required
@auth.logged_child_or_caregiver_only
def use_points(child_id):
    logged_user_id = g.user_data['id']
    child_id = int(child_id)

    return_url = request.args.get('return_url', '/')

    current_points = zeton.data_access.points.get_only_points(child_id)
    try:
        used_points = int(request.form['points'])
    except ValueError as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if used_points > 0:
        if used_points <= current_points:
            zeton.data_access.points.change_points_by(child_id, -used_points, logged_user_id, 0)
        else:
            missing_points = abs(current_points - used_points)
            if missing_points == 1:
                points_word = 'punktu'
            else:
                points_word = 'punktów'
            flash(f'Do tej nagrody brakuje Ci:  {missing_points} {points_word}')

    return redirect(return_url)
