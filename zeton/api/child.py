from flask import request, redirect, url_for, abort, g

import zeton.data_access.bans
import zeton.data_access.points
from zeton import auth
from zeton.api import bp
from zeton.data_access import data_access
from zeton.data_access.data_access import load_logged_in_user_data


@bp.route("/child/<target_id>/points/add", methods=['POST'])
@auth.login_required
def add_points(target_id):
    load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    if not data_access.is_child_under_caregiver(target_id, logged_user_id):
        return abort(403)

    try:
        nowe_punkty = int(request.form['liczba_punktow'])
    except ValueError as ex:
        print(ex)
    else:
        if nowe_punkty > 0:
            zeton.data_access.points.change_points_by(target_id, nowe_punkty)
    finally:
        return redirect(url_for('views.child', child_id=target_id))


@bp.route("/child/<child_id>/points/use", methods=['POST'])
@auth.login_required
def use_points(child_id):
    load_logged_in_user_data()
    logged_user_id = g.user_data['id']

    child_id = int(child_id)

    return_url = request.args.get('return_url', '/')

    if not (child_id == logged_user_id or
            data_access.is_child_under_caregiver(child_id, logged_user_id)):
        return abort(403)

    current_points = zeton.data_access.points.get_points(child_id)

    try:
        used_points = int(request.form['points'])
        if used_points > 0:
            if used_points <= current_points:
                zeton.data_access.points.change_points_by(child_id, -1 * used_points)
    except ValueError:
        return {'message': 'Bad request'}, 400

    return redirect(return_url)
