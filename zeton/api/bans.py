from flask import g, abort, redirect, request

import zeton.data_access
from zeton import auth
from zeton.api import bp
from zeton.data_access import users


@bp.route("/ban/<target_id>")
@auth.login_required
def give_ban(target_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']
    child = users.get_child_data(target_id)

    if not (child['id'] == logged_user_id or
            users.is_child_under_caregiver(target_id, logged_user_id)):
        return abort(403)

    ten_minutes = 10
    zeton.data_access.bans.give_ban(target_id, ten_minutes)
    return redirect(request.referrer)


@bp.route("/warn/<target_id>")
@auth.login_required
def give_warn(target_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']
    child = users.get_child_data(target_id)

    if not (child['id'] == logged_user_id or
            users.is_child_under_caregiver(target_id, logged_user_id)):
        return abort(403)

    zeton.data_access.bans.give_warn(target_id)
    return redirect(request.referrer)


@bp.route("/kick/<target_id>")
@auth.login_required
def give_kick(target_id):
    users.load_logged_in_user_data()
    logged_user_id = g.user_data['id']
    child = users.get_child_data(target_id)

    if not (child['id'] == logged_user_id or
            users.is_child_under_caregiver(target_id, logged_user_id)):
        return abort(403)

    zeton.data_access.bans.give_kick(target_id)
    return redirect(request.referrer)
