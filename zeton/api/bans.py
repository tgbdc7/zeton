from flask import redirect, request, g

import zeton.data_access
from zeton import auth
from zeton.api import bp


@bp.route("/ban/<child_id>/<ban_type>", methods=['POST'])
@auth.login_required
@auth.logged_child_or_caregiver_only
def give_ban(child_id, ban_type):
    logged_user_id = g.user_data['id']
    ten_minutes = 10

    if ban_type == 'warn':
        zeton.data_access.bans.give_warn(child_id, logged_user_id)
    elif ban_type == 'kick':
        zeton.data_access.bans.give_kick(child_id, logged_user_id)
    elif ban_type == 'ban':
        zeton.data_access.bans.give_ban(child_id, ten_minutes, logged_user_id)

    return redirect(request.referrer)
