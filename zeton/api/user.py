from flask import request, redirect, url_for, abort, g

import zeton.data_access.bans
import zeton.data_access.points
from zeton import auth
from zeton.api import bp
from zeton.data_access import users

@bp.route("/settings/<target_id>/change_password", methods=['POST'])
@auth.login_required
def settings(target_id):
    pass