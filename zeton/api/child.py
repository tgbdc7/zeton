from flask import request, redirect, url_for, abort, g, flash

import zeton.data_access.bans
import zeton.data_access.points
from zeton import auth
from zeton.api import bp
from zeton.data_access import users


@bp.route("/child/<target_id>/points/add", methods=['POST'])
@auth.login_required
def add_points(target_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    if not users.is_child_under_caregiver(target_id, logged_user_id):
        return abort(403)

    try:
        added_points = int(request.form['liczba_punktow'])
    except ValueError as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if added_points > 0:
        zeton.data_access.points.change_points_by(target_id, added_points, logged_user_id)

    return redirect(url_for('views.child', child_id=target_id))


@bp.route("/child/<child_id>/points/use", methods=['POST'])
@auth.login_required
def use_points(child_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    child_id = int(child_id)

    return_url = request.args.get('return_url', '/')

    if not (child_id == logged_user_id or
            users.is_child_under_caregiver(child_id, logged_user_id)):
        return abort(403)

    current_points = zeton.data_access.points.get_points(child_id)

    try:
        used_points = int(request.form['points'])
    except ValueError as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if used_points > 0:
        if used_points <= current_points:
            zeton.data_access.points.change_points_by(child_id, -used_points, logged_user_id)
        else:
            missing_points = abs(current_points - used_points)
            if missing_points == 1:
                points = 'punkta'
            else:
                points = 'punktów'
            flash(f'Do tej nagrody brakuje Ci:  {missing_points} {points}')

    return redirect(return_url)
