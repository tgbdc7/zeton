from flask import request, redirect, url_for, abort, g, flash

import zeton.data_access.bans
import zeton.data_access.points
from zeton import auth
from zeton.api import bp
from zeton.data_access import users


@bp.route("/child/<child_id>/points/add", methods=['POST'])
@auth.login_required
@auth.caregiver_only
def add_points(child_id):
    logged_user_id = g.user_data['id']
    logged_user_firstname = g.user_data['firstname']

    try:
        added_points = int(request.form['liczba_punktow'])
    except ValueError as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if added_points > 0:
        zeton.data_access.points.change_points_by(child_id, added_points, logged_user_id, logged_user_firstname)

    return redirect(url_for('views.child', child_id=child_id))


@bp.route("/child/<child_id>/points/use", methods=['POST'])
@auth.login_required
@auth.logged_child_or_caregiver_only
def use_points(child_id):
    logged_user_id = g.user_data['id']
    logged_user_firstname = g.user_data['firstname']


    child_id = int(child_id)

    return_url = request.args.get('return_url', '/')

    current_points = zeton.data_access.points.get_points(child_id)

    try:
        used_points = int(request.form['points'])
    except ValueError as ex:
        print(ex)
        return {'message': 'Bad request'}, 400

    if used_points > 0:
        if used_points <= current_points:
            zeton.data_access.points.change_points_by(child_id, -used_points, logged_user_id, logged_user_firstname)
        else:
            missing_points = abs(current_points - used_points)
            if missing_points == 1:
                points_word = 'punktu'
            else:
                points_word = 'punktów'
            flash(f'Do tej nagrody brakuje Ci:  {missing_points} {points_word}')

    return redirect(return_url)
