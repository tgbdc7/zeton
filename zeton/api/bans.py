from flask import redirect, request

import zeton.data_access
from zeton import auth
from zeton.api import bp


@bp.route("/ban/<child_id>")
@auth.login_required
@auth.logged_child_or_caregiver_only
def give_ban(child_id):
    ten_minutes = 10
    zeton.data_access.bans.give_ban(child_id, ten_minutes)
    return redirect(request.referrer)


@bp.route("/warn/<child_id>")
@auth.login_required
@auth.logged_child_or_caregiver_only
def give_warn(child_id):
    zeton.data_access.bans.give_warn(child_id)
    return redirect(request.referrer)


@bp.route("/kick/<child_id>")
@auth.login_required
@auth.logged_child_or_caregiver_only
def give_kick(child_id):
    zeton.data_access.bans.give_kick(child_id)
    return redirect(request.referrer)
