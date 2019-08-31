from flask import redirect, request

import zeton.data_access
from zeton import auth
from zeton.api import bp


@bp.route("/ban/<target_id>")
@auth.login_required
@auth.logged_child_or_caregiver_only
def give_ban(target_id):
    ten_minutes = 10
    zeton.data_access.bans.give_ban(target_id, ten_minutes)
    return redirect(request.referrer)


@bp.route("/warn/<target_id>")
@auth.login_required
@auth.logged_child_or_caregiver_only
def give_warn(target_id):
    zeton.data_access.bans.give_warn(target_id)
    return redirect(request.referrer)


@bp.route("/kick/<target_id>")
@auth.login_required
@auth.logged_child_or_caregiver_only
def give_kick(target_id):
    zeton.data_access.bans.give_kick(target_id)
    return redirect(request.referrer)
